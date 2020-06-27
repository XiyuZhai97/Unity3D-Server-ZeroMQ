#!/usr/bin/python3
import time
import zmq
import os
import computing.SceneGen.SceneGen as SG
context = zmq.Context()
socket = context.socket(zmq.REP)
socket.bind("tcp://*:5123")
newFileFlag = "START SEND FILE:"
input_dir = r"/home/ubuntu/received_files/"
output_dir = r"/home/ubuntu/output/"
model_dir = r"/home/ubuntu/workspace/Unity3D-Server-ZeroMQ/computing/SceneGen/models/"
print("Start Server")

while True:
    #  Wait for next request from client
    message = socket.recv().decode('UTF-8')


    if(newFileFlag in message):
        fileNAME = message[len(newFileFlag):]
        inputFileHandler = open(input_dir + fileNAME + ".txt", "w+")

        feedback = "Creat " + fileNAME + ".txt"
        socket.send(feedback.encode('UTF-8'))
        print(feedback)

    elif("COMPLETE:" + fileNAME in message):
        # Run ML model and send heatmap files as one feedback
        print("Complete " + fileNAME + ".txt")
        inputFileHandler.close()

        feedback = ""
        all_add_object_names = SG.augmentScene_getAllResult(fileNAME + ".txt", input_dir, output_dir, model_dir, False)
        for object_name in all_add_object_names:
            outputFileHandler = open(output_dir + "place_" +object_name + "_in_" + fileNAME + ".txt", "r")
            data = outputFileHandler.read()
            outputFileHandler.close()
            feedback += '\n' + "HEATMAP_FILES:" + "place_" +object_name + "_in_" + fileNAME + ".txt" + '\n'
            feedback += data
            feedback += "COMPLETE:" + "place_" +object_name + "_in_" + fileNAME + ".txt" + '\n'
        socket.send(feedback.encode('UTF-8'))
        print("Get results for " + fileNAME + ".txt")

        print("Delete received file and results")
        
        if os.path.exists(input_dir + fileNAME + ".txt"):
            os.remove(input_dir + fileNAME + ".txt")
        else:
            print(input_dir + fileNAME + ".txt" + " does not exist")
            
        for object_name in all_add_object_names:
            if os.path.exists(output_dir + "place_" +object_name + "_in_" + fileNAME + ".txt"):
                os.remove(output_dir + "place_" +object_name + "_in_" + fileNAME + ".txt")
            else:
                print(input_dir + fileNAME + ".txt" + " does not exist")

    elif(not inputFileHandler.closed):
        feedback = "Received Content"
        socket.send(feedback.encode('UTF-8'))
        print(feedback)
        inputFileHandler.write(message + "\n")

    else:
        socket.send(b"Hi from AWS")