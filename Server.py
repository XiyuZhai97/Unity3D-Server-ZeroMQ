#!/usr/bin/python3
import time
import zmq
import computing.SceneGen.SceneGen as SG
context = zmq.Context()
socket = context.socket(zmq.REP)
socket.bind("tcp://*:5123")
newFileFlag = "START SEND FILE:"
input_dir = r"/home/ubuntu/received_files/"
output_dir = r"/home/ubuntu/output/"
model_dir = r"/home/ubuntu/workspace/Unity3D-Server-ZeroMQ/computing/SceneGen/models/"
print(output_dir)

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
        feedback = ""
        all_add_object_names = SG.augmentScene_getAllResult(fileNAME, input_dir, output_dir, model_dir, False)
        for object_name in all_add_object_names:
            outputFileHandler = open(output_dir + "place_" +object_name + "_in_" + fileNAME, "r")
            data = outputFileHandler.read()
            outputFileHandler.close()
            feedback += "HEATMAP_FILES:" + "place_" +object_name + "_in_" + fileNAME + '\n'
            feedback += data
        socket.send(feedback.encode('UTF-8'))
        print("Complete " + fileNAME + ".txt")
        inputFileHandler.close()

    elif(not inputFileHandler.closed):
        feedback = "Received Content"
        socket.send(feedback.encode('UTF-8'))
        print(feedback)
        inputFileHandler.write(message + "\n")

    else:
        socket.send(b"Hi from AWS")