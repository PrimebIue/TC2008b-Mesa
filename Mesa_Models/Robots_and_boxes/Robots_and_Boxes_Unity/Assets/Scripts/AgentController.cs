using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.Networking;

public class RobotAgent {
    public List<Vector3> positions;
}

public class BoxAgent {
    public List<Vector3> positions;
    public int numBoxes;
}

public class ObjAgent {
    public Vector3 position;
}

public class AgentController : MonoBehaviour
{

    [SerializeField] string url;
    [SerializeField] string initEP;
    [SerializeField] string getRobotsEP;
    [SerializeField] string getBoxesEP;
    [SerializeField] string getObjEP;
    [SerializeField] string updateEP;
    [SerializeField] string sendConfigEndpoint;
    [SerializeField] int numAgents;
    [SerializeField] float updateDelay;
    [SerializeField] float density;
    [SerializeField] GameObject robotPrefab;
    [SerializeField] GameObject boxPrefab;
    [SerializeField] GameObject objPrefab;

    GameObject[] robots;
    RobotAgent robotAgents;
    GameObject[] boxes;
    RobotAgent boxAgents;
    GameObject objective;
    ObjAgent objAgent;
    float updateTime = 0;
    

    // Start is called before the first frame update
    void Start()
    {
        robots = new GameObject[numAgents]
        for (int i = 0; i < numAgents; i++) {
            robots[i] = Instantiate(robotPrefab, Vector3.zero, Quaternion.identity)
        }

        
        
    }

    // Update is called once per frame
    void Update()
    {
        UnityWebRequest www = UnityWebRequest.Get(url + updateEP);
        yield return www.SendWebRequest();

        if (www.result != UnityWebRequest.Result.Success)
            Debug.Log(www.error);
        else {
            StartCoroutine(GetRobotsData);
            StartCoroutine(GetBoxesData);
            StartCoroutine(GetObjData);
        }

    }

    IEnumerator SendConfiguration() {
        WWWForm form = new WWWForm();

        form.AddField("numAgents", numAgents.ToString());
        form.AddField("width", width.ToString());
        form.AddField("height", height.ToString());
        form.AddField("desity", density.ToString());

        UnityWebRequest www = UnityWebRequest.Post(url + sendConfigEndpoint, form);
        www.SendRequestHeader("Content-Type", "application/x-www-form-urlencoded");

        yield return www.SendWebRequest();

        if (www.result != UnityWebRequest.Result.Success) {
            Debug.Log(www.error);
        } else {
            
        }
    }

    IEnumerator GetRobotsData() {
        UnityWebRequest www = UnityWebRequest.Get(url + getRobotsEP);
        yield return www.SendWebRequest();

        if (www.result == UnityWebRequest.Result.Success) {
            Debug.Log(www.downloadHandler.text);
            robots = JsonUtility.FromJson<RobotAgent>(www.downloadHandler.text);
            MoveAgents();
        } else {
            Debug.Log(www.error);
        }
    }

    IEnumerator GetBoxesData() {
        UnityWebRequest www = UnityWebRequest.Get(url + getBoxesEP);
        yield return www.SendWebRequest();

        if (www.result == UnityWebRequest.Result.Success) {
            Debug.Log(www.downloadHandler.text);
            boxes = JsonUtility.FromJson<BoxAgent>(www.downloadHandler.text);
            MoveAgents();
        } else {
            Debug.Log(www.error);
        }
    }

    IEnumerator GetObjData() {
        UnityWebRequest www = UnityWebRequest.Get(url + getObjEP);
        yield return www.SendWebRequest();

        if (www.result == UnityWebRequest.Result.Success) {
            Debug.Log(www.downloadHandler.text);
            objective = JsonUtility.FromJson<RobotAgent>(www.downloadHandler.text);
            MoveAgents();
        } else {
            Debug.Log(www.error);
        }
    }

    void MoveAgents() {
        for (int i = 0; i < numAgents; i++) {
            robots[i].transform.position = agents.positions[i];
        }
    }
}
