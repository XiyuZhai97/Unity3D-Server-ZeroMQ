[toc]

# Unity3D-Server-ZeroMQ
Unity3D on IOS Client - Python Server based on ZeroMQ

## Server

1. Receive have ‘.txt’ create new room txt file; Receive have ‘Done’ close the filehandler
2. Run model get **5 txt files** for all potential furniture(table, tv, sofa, chair, bed)
3. Send those 5 txt files name and content, line by line ending with “Done”

## Unity

Different UI or Different Scene?

### UI1(Scene Room Builder)

1. Create floor based on image or plane detection?
2. Choose furniture type
3. add bounding box for real furniture
4. move rotate scale boxes
   1. Scale? or determine size of each kind of furniture in advance?
   2. also scale when adding new furniture in Scene16?
5. input room name
6. save 
   1. save room txt file
   2. save all bounding box as **a object transfer between scenes?** Or **new scrips that read txt file to create bbox** how

7. switch to UI2

### UI2(Scene AR Scene G) choose existing room. --- send txt to server

1. Create floor based on image 
2. Read existing room files. add those names as dropdown's options.
3. Choose room 
   1. be able to show bounding box
   2. When turn on SceneG 
      1. input server ip: 
      2. show ‘connecting server’
         1. Start connect --- send room file to server line by line
         2. Receive result txt files of all furnitures
         3. Show 'completed’
4. ? after add one furniture. Keep the same results or have **save button** to make it as a new room?
5. need save the new room with new added furniture?

after add and move one furniture --- send again?

when to connect with server? When SceneG on or **when click ShowHeatmap and add**
