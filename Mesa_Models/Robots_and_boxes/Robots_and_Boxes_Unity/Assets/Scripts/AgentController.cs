using System;
using System.Collections;
using System.Collections.Generic;
using UnityEditor;
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
    [SerializeField] string getRobotsEP = "/getRobots";
    [SerializeField] string getBoxesEP = "/getBoxes";
    [SerializeField] string getObjEP = "/getObj";

    [SerializeField] string updateEP = "/update";
    [SerializeField] string sendConfigEndpoint = "/init";
    [SerializeField] int numAgents;
    [SerializeField] float updateDelay;
    [SerializeField] float density;

    [SerializeField] GameObject robotPrefab;
    [SerializeField] GameObject boxPrefab;
    [SerializeField] GameObject objPrefab;

    GameObject[] robots;
    GameObject[] boxes;
    GameObject objective;
    RobotAgent robotAgents;
    BoxAgent boxAgents;
    ObjAgent objAgent;

    bool hold = false;
    bool first = true;

    float updateTime = 5.0f;
    
    // Start is called before the first frame update
    void Start()
    {
        robotAgents = new RobotAgent();
        boxAgents = new BoxAgent();
        objAgent = new ObjAgent();

        robots = new GameObject[numAgents];
        objective = new GameObject();

        objective = Instantiate(objPrefab, Vector3.zero, Quaternion.identity);

        for (int i = 0; i < numAgents; i++) {
            robots[i] = Instantiate(robotPrefab, Vector3.zero, Quaternion.identity);
        }

        StartCoroutine(SendConfiguration()); 
    }

    // Update is called once per frame
    void Update()
    {

        if (updateTime > updateDelay) {
            updateTime = 0;
            hold = true;
            StartCoroutine(UpdateSimulation());
        }

        if (!hold) {
            updateTime += Time.deltaTime;
        }
    }

    IEnumerator UpdateSimulation() {
        UnityWebRequest www = UnityWebRequest.Get(url + updateEP);
        yield return www.SendWebRequest();

        if (www.result != UnityWebRequest.Result.Success) {
            Debug.Log(www.error);
        }
        else {
            Debug.Log("update");

            yield return GetRobotsData();
        }

    }

    IEnumerator SendConfiguration() {
        WWWForm form = new WWWForm();

        form.AddField("numAgents", numAgents.ToString());
        form.AddField("width", 10);
        form.AddField("height", 10);
        form.AddField("density", density.ToString());

        UnityWebRequest www = UnityWebRequest.Post(url + sendConfigEndpoint, form);

        yield return www.SendWebRequest();

        if (www.result != UnityWebRequest.Result.Success) {
            Debug.Log(www.error);
        } else {
            Debug.Log("Configuration upload complete!");
            Debug.Log("Getting Agents positions");
            StartCoroutine(GetRobotsData());
            StartCoroutine(GetObjData());
        }
    }

    IEnumerator GetRobotsData() {
        UnityWebRequest www = UnityWebRequest.Get(url + getRobotsEP);
        yield return www.SendWebRequest();

        if (www.result == UnityWebRequest.Result.Success) {
            Debug.Log(www.downloadHandler.text);
            robotAgents = JsonUtility.FromJson<RobotAgent>(www.downloadHandler.text);
            yield return GetBoxesData();
        } else {
            Debug.Log(www.error);
        }
    }

    IEnumerator GetBoxesData() {
        UnityWebRequest www = UnityWebRequest.Get(url + getBoxesEP);
        yield return www.SendWebRequest();

        if (www.result == UnityWebRequest.Result.Success) {
            Debug.Log(www.downloadHandler.text);
            boxAgents = JsonUtility.FromJson<BoxAgent>(www.downloadHandler.text);

            if (!first) {
                for (int i = 0; i < boxes.Length; i++)
                    Destroy(boxes[i]);
            }
            boxes = new GameObject[boxAgents.numBoxes];
            for (int i = 0; i < boxAgents.numBoxes; i++) {
                boxes[i] = Instantiate(boxPrefab, Vector3.zero, Quaternion.identity);
            }

            first = false;
            hold = false;
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
            objAgent = JsonUtility.FromJson<ObjAgent>(www.downloadHandler.text);
            objective.transform.position = objAgent.position;
        } else {
            Debug.Log(www.error);
        }
    }

    void MoveAgents() {
        for (int i = 0; i < numAgents; i++) {
            robots[i].transform.position = robotAgents.positions[i];
        }
        for (int i = 0; i < boxAgents.positions.Count; i++) {
            boxes[i].transform.position = boxAgents.positions[i];
            if (boxAgents.positions[i] == objAgent.position){
                Debug.Log("Destroy");
                Destroy(boxes[i]);
            }
        }
        Debug.Log("here");
    }
}
