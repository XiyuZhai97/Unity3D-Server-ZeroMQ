using UnityEngine;
using UnityEngine.UI;
using System.Collections;

public class HelloClient : MonoBehaviour
{
    public Text Receiving;
    public Text Sending;
    public Text Status;
    public Button stopConnect;
    public Button startConnect;
    public InputField ipInput;
    public InputField roomNameInput;

    private HelloRequester _helloRequester;

    private void Start()
    {
        // _helloRequester = new HelloRequester();
        Status.text = "Stopped";
        stopConnect.onClick.AddListener(stopConnectFun);
        startConnect.onClick.AddListener(startConnectFun);

    }
    void Update()
    {
        if(_helloRequester != null){

            Receiving.text = _helloRequester.received;
            Sending.text = _helloRequester.sended;
        }
        // Status.text = _helloRequester.status;
    }

    void startConnectFun()
    {
        
        Status.text = "Stop Connect ...";
        if(_helloRequester != null){
            _helloRequester.Stop();
        }

        Status.text = "Start Connect ...";
        _helloRequester = new HelloRequester();
        _helloRequester.serverIP = ipInput.text;
        _helloRequester.Start();
    }
    void stopConnectFun()
    {
        Status.text = "Stop Connect ...";
        _helloRequester.Stop();
    }
    private void OnDestroy()
    {
        _helloRequester.Stop();
    }
}