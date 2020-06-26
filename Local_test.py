#!/usr/bin/python3
import time
import computing.SceneGen.SceneGen as SG
fileNAME = "testroom.txt"
newFileFlag = "START SEND FILE:"
feedback = ""
input_dir = r"/Users/xiyuzhai/Workspace/Unity3D-Server-ZeroMQ/"
output_dir = r"/Users/xiyuzhai/Workspace/output/"
model_dir = r"/Users/xiyuzhai/Workspace/Unity3D-Server-ZeroMQ/computing/SceneGen/models/"

# TODO Run ML model and send feedback... as 5 files?
all_add_object_names = SG.augmentScene_getAllResult(fileNAME, input_dir, output_dir, model_dir, False)
for object_name in all_add_object_names:
    outputFileHandler = open(output_dir + "place_" +object_name + "_in_" + fileNAME, "r")
    data = outputFileHandler.read()
    outputFileHandler.close()
    feedback += "HEATMAP_FILES:" + "place_" +object_name + "_in_" + fileNAME + '\n'
    feedback += data
print(feedback)