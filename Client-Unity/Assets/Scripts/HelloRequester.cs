using AsyncIO;
using NetMQ;
using NetMQ.Sockets;
using System.IO;
using UnityEngine;
/// <summary>
///     Example of requester who only sends Hello. Very nice guy.
///     You can copy this class and modify Run() to suits your needs.
///     To use this class, you just instantiate, call Start() when you want to start and Stop() when you want to stop.
/// </summary>
public class HelloRequester : RunAbleThread
{
    public string serverIP = "tcp://192.168.0.2:5123";
    public string receivedLog;
    public string sentLog;
    public string status = "Stopped";
    public string sendFilePath;
    public string receiveFilePath;
    public string fileName;
    StreamWriter writer;
    protected override void Run()
    {
        ForceDotNet.Force(); // this line is needed to prevent unity freeze after one use, not sure why yet
        using (RequestSocket client = new RequestSocket())
        {
            client.Connect(serverIP);
            
            status = "Not Connect";
            for(;Running;)
            {
                status = "Sending...";
                client.SendFrame("START SEND FILE:" + fileName);
                ReceiveMessage(client);
                var bytes = System.IO.File.ReadAllBytes(sendFilePath + fileName + ".txt");
                client.SendFrame(bytes);
                ReceiveMessage(client);

                client.SendFrame("COMPLETE:" + fileName);
                ReceiveMessage(client);
                if(status.Contains("ERROR"))
                    break;
                status = "COMPLETE: " + fileName;
                break;
            }
        }
        NetMQConfig.Cleanup(); // this line is needed to prevent unity freeze after one use, not sure why yet
        
    }
    void ReceiveMessage(RequestSocket client)
    {
        string message = null;
        bool gotMessage = false;
        var timeout = new System.TimeSpan(0, 0, 5); //1sec

        while (Running)
        {
            gotMessage = client.TryReceiveFrameString(timeout, out message); // this returns true if it's successful
            if (gotMessage) break;
            else{
                status = "Check server ip or server is closed";
                break;
            }
        }

        if (gotMessage) {
            // receivedLog += System.DateTime.Now + ": Received " + message + " \r\n";
            if(message.Contains("ERROR")){
                status = "ERROR(empty room)";
            }
            if(message.Contains("HEATMAP_FILES")){
                string[] content_lines = message.Split(new string[] { "\r\n", "\n" }, System.StringSplitOptions.RemoveEmptyEntries);
                foreach (string s in content_lines)
                {
                    if(s.Contains("HEATMAP_FILES:"))
                    {
                        Debug.Log(receiveFilePath + s.Substring("HEATMAP_FILES:".Length));
                        status = "Writing: " + receiveFilePath + s.Substring("HEATMAP_FILES:".Length);
                        writer = new StreamWriter(receiveFilePath + s.Substring("HEATMAP_FILES:".Length), true);
                    }
                    else if(s.Contains("COMPLETE:"))
                    {
                        writer.Close();
                        status = "Get: " + receiveFilePath + s.Substring("HEATMAP_FILES:".Length);
                    }
                    else{
                        writer.WriteLine(s);
                    }
                receivedLog += s;
                }
            }
        }
    }
}