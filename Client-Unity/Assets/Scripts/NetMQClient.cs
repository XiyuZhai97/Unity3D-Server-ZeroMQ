using UnityEngine;
using UnityEngine.UI;
using System.Collections;

public class NetMQClient : MonoBehaviour
{
    public Text Receiving;
    public Text Sending;
    public Text Status;
    public Button stopConnect;
    public Button startConnect;
    public InputField ipInput;
    public InputField roomNameInput;
    string room;
    private HelloRequester _helloRequester;

    private void Start()
    {
        stopConnect.onClick.AddListener(stopConnectFun);
        startConnect.onClick.AddListener(startConnectFun);
        _helloRequester = new HelloRequester();
    }
    void Update()
    {
        if(_helloRequester != null){
            Receiving.text = _helloRequester.receivedLog;
            Sending.text = _helloRequester.sentLog;
            Status.text = _helloRequester.status;
            if(_helloRequester.status.Contains("COMPLETE") || _helloRequester.status.Contains("ERROR")){
                stopConnectFun();
            }
        }
        room = roomNameInput.text;

    }

    void startConnectFun()
    {
        this.GetComponent<WriteLocation>().saveRoom();
        if(_helloRequester.Running){
            _helloRequester.Stop();
        }
        _helloRequester = new HelloRequester();
        Status.text = _helloRequester.status;
        _helloRequester.serverIP = ipInput.text;
        _helloRequester.sendFilePath = this.GetComponent<RoomManager>().inputFilePath;
        _helloRequester.receiveFilePath = this.GetComponent<RoomManager>().outputFilePath; // change this to your directory

        _helloRequester.fileName = room;
        _helloRequester.Start();
    }
    void stopConnectFun()
    {
        _helloRequester.Stop();
    }
    private void OnDestroy()
    {
        _helloRequester.Stop();
    }
}