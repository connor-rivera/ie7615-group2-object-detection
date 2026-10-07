"""Paths and settings shared by every notebook"""
import os

# The shared milestone 2 folder in drive. This is the only drive folder that any code will write to
OUTPUTS = "/content/drive/MyDrive/ie7615-m2-outputs"
CLEANED_TAR = os.path.join(OUTPUTS, "cleaned_v1.tar")

# Temporary space of the colab server
LOCAL = "/content/data"

# Scene generation
seed = 7615
canvas = 640 # The scene that we are setting as the backdrop for item pictures will be 640x640 pixels
min_objects, max_objects = 2, 5 # Number of objects per scene
min_size, max_size = 100, 224 # Minimum and maximum size of objects in the scene with the original being the larger end
max_tries = 50 # Number of attempts to place objects in a scene with no overlap
scenes = {"train": 1400, "val": 300, "test": 300} # Allows for possibility of each object being used about once
