using System;
using System.Collections;
using System.Collections.Generic;
using UnityEditor;
using UnityEngine;
using UnityEngine.Networking;

public class RobotAgent {
    public List<Vector3> positions;
}

public class RobotData {
    public Vector3 position;
    public int uniqueID;
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
    List<GameObject> boxes;
    GameObject objective;
    RobotAgent robotAgents;
    BoxAgent boxAgents;
    ObjAgent objAgent;

    // Smooth Transitions
    List<Vector3> oldPositionsRobots;
    List<Vector3> newPositionsRobots;
    List<Vector3> oldPositionsBoxes;
    List<Vector3> newPositionsBoxes;

    bool hold = false;
    bool first = true;

    float timer, dt;
    
    // Start is called before the first frame update
    void Start()
    {
        robotAgents = new RobotAgent();
        boxAgents = new BoxAgent();
        objAgent = new ObjAgent();

        robots = new GameObject[numAgents];
        objective = new GameObject();
        boxes = new List<GameObject>();

        oldPositionsRobots = new List<Vector3>();
        newPositionsRobots = new List<Vector3>();
        oldPositionsBoxes = new List<Vector3>();
        newPositionsBoxes = new List<Vector3>();

        objective = Instantiate(objPrefab, Vector3.zero, Quaternion.identity);

        for (int i = 0; i < numAgents; i++) {
            robots[i] = Instantiate(robotPrefab, Vector3.zero, Quaternion.identity);
        }


        StartCoroutine(SendConfiguration()); 
    }

    // Update is called once per frame
    void Update()
    {
        float t = timer/updateDelay;

        dt = t * t * (3f - 2f*t);

        if (timer > updateDelay) {

            timer = 0;
            hold = true;
            StartCoroutine(UpdateSimulation());
        }

        if (!hold) {
            for (int s = 0; s < robots.Length; s++) {
                Vector3 interpolated = Vector3.Lerp(oldPositionsRobots[s], newPositionsRobots[s], dt);
                robots[s].transform.localPosition = interpolated;

                Vector3 dir = oldPositionsRobots[s] - newPositionsRobots[s];
                robots[s].transform.rotation = Quaternion.LookRotation(dir);
            }
            for (int s = 0; s < boxes.Count; s++) {
                if (boxes[s].activeSelf && oldPositionsBoxes.Count == newPositionsBoxes.Count) {
                    Vector3 interpolated = Vector3.Lerp(oldPositionsBoxes[s], newPositionsBoxes[s], dt);

                    boxes[s].transform.localPosition = interpolated;

                    Vector3 dir = oldPositionsBoxes[s] - newPositionsBoxes[s];
                    boxes[s].transform.rotation = Quaternion.LookRotation(dir);
                }
            }

            timer += Time.deltaTime;
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

            oldPositionsRobots = new List<Vector3>(newPositionsRobots);

            newPositionsRobots.Clear();

            foreach(Vector3 v in robotAgents.positions)
            {
                newPositionsRobots.Add(v);
                if (first)
                    oldPositionsRobots.Add(v);
            }

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

            oldPositionsBoxes = new List<Vector3>(newPositionsBoxes);

            newPositionsBoxes.Clear();

            foreach(Vector3 v in boxAgents.positions)
            {
                newPositionsBoxes.Add(v);
                if (first)
                    oldPositionsBoxes.Add(v);
            }

            if (first) {
                for (int i = 0; i < boxAgents.numBoxes; i++) {
                    boxes.Add(Instantiate(boxPrefab, Vector3.zero, Quaternion.identity));
                }
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
                boxes[i].SetActive(false);
            }
        }
        Debug.Log("here");
    }
}
