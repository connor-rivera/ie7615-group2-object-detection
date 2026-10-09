# IE7615 Milestone 2 - YOLOv8 Object Detection for Group 2

This portion of the project detects the objects in multi-object images using a YOLOv8 model
that was trained on synthetic scenes built from the class dataset

## How This Works
- All code runs on Google Colab (utilizing GPU runtime for training)
- This repo is the single source for the code. Notebooks import shared functions from 'src/'
- The original dataset (shared via a Google Drive folder) is read-only and was never modified. A copy of the data was made to be manipulated for the needs of the project
- Generated images, labels and model weights are saved to a shared Drive folder named 'ie7615-m2-outputs'
- Random steps use a fixed seed '7615' so the results can be reproduced


## Dataset Generation Rules
- Every photo in the dataset belongs to one split, and each scene only uses photos from its own split:

| Split | Object photos | Background photos |
| --- | --- | --- |
| Train | 4,886 | 229 |
| Val | 1,028 | 72 |
| Test | 1,028 | 72 |

- Each photo's split is listed in the 'records/manifest_v1.csv' (This manifest was made for milestone 1, so we are just maintaining the uniformity of our split from that)
- Each scene starts from a background photo, resized to 640x640
- Each scene also contains from 2 to 5 randomly selected object photos
- The same photo is never used twice in one scene
- Objects must not overlap. Each object is tried in random spots and if one overlaps an object photo that is already placed then a new spot is tried. If there is no free spot after several tries, the photo is skipped
- Object photos will additionally be scaled down if they are too big to fit, minimizing the potential that a photo will not be included in the frame
- The YOLO class designation also needs to be addressed as the counting will begin at 0, so YOLO class = (Object ID - 1), so Object 10 will be recognized as class 9

## Reproducibility
To re-run this project and get the same results:

**Before starting**
- The shared drive folder 'ie7615-m2-outputs' must contain 'cleaned_v1.tar' (The cleaned dataset)
- Open each notebook in colab
- The first cell of every notebook mounts Google Drive, clones the repo and installs the requirements.txt file

**Run the notebooks in the following order**
- 'notebooks/generate_dataset.ipynb' - This notebook builds the 640x640 multi-object scenes and their YOLO labels, using the splits in 'records/manifest_v1.csv', then saves the generated dataset to the drive folder
- 'notebooks/train_yolov8.ipynb' - Trains the YOLOv8 model on the generated dataset, then saves the model weights to the drive folder (The training would be run on colab's GPU)
- 'notebooks/evaluate.ipynb' - Scores the trained model on the test scenes and saves sample detections to the 'reports/figures/' folder

**Matching results**
- All of the steps based on randomness utilize the seed '7615' so the same inputs reproduce the same scenes
- Each result in 'records/experiments.csv' also lists the commit and dataset version it came from

## Generated dataset (scenes_v1)
- Built by `notebooks/generate_dataset.ipynb` at commit `bff0862` with seed 7615
- Saved in the shared Drive folder as `ie7615-m2-outputs/scenes_v1.tar`
- 1,400 train / 300 val / 300 test scenes, each 640x640 with 2-5 objects (objects 100-224 px)
- Layout inside the tar: `scenes_v1/images/{train,val,test}/*.jpg`, `scenes_v1/labels/{train,val,test}/*.txt`, `scenes_v1/data.yaml`
- Each label line is `class x_center y_center width height`, scaled to 0-1. Class names are OBJ001-OBJ073 (YOLO class 0 = OBJ001)
- Sample scenes with their labels drawn on: `reports/figures/sample_scenes.png` (the green boxes are only drawn for the figure, the dataset images are clean)

**To use it in a training notebook**, unpack it to `/content/data` so the paths in `data.yaml` are correct:
```python
from src import config
from src.data import unpack_cleaned
scenes_dir = unpack_cleaned(os.path.join(config.OUTPUTS, "scenes_v1.tar"), config.LOCAL)
data_yaml = os.path.join(scenes_dir, "data.yaml")
```

**Running notebooks:** use Colab in the browser (File → Open notebook → GitHub). The `ie7615-m2-outputs` folder must be in your My Drive; if it is only under "Shared with me", right-click it → Organize → Add shortcut → My Drive.