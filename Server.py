#!/usr/bin/python3
import time
import zmq
import Computing.SceneGen.SceneGen as SG
context = zmq.Context()
socket = context.socket(zmq.REP)
socket.bind("tcp://*:5123")

while True:
    #  Wait for next request from client
    message = socket.recv().decode('UTF-8')

    newFileFlag = "START SEND FILE:"
    input_dir = r"/home/ubuntu/received_files/"
    output_dir = "output/multipleobjs/"
    print(output_dir)
    if(newFileFlag in message):
        fileNAME = message[len(newFileFlag):]
        inputFileHandler = open(input_dir + fileNAME + ".txt", "w+")

        feedback = "Creat " + fileNAME + ".txt"
        socket.send(feedback.encode('UTF-8'))
        print(feedback)

    elif("COMPLETE:" + fileNAME in message):
        # TODO Run ML model and send feedback... as 5 files?
        SG.augmentScene(fileNAME, input_dir, output_dir)
        feedback = "HEATMAP_FILES: \n xxx.txt\n xxxxx\n"
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