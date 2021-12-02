// TC2008B. Sistemas Multiagentes y Gráficas Computacionales
// C# client to interact with Python. Based on the code provided by Sergio Ruiz.
// Octavio Navarro. October 2021

using System;
using System.Collections;
using System.Collections.Generic;
using UnityEditor;
using UnityEngine;
using UnityEngine.Networking;

public class CarData
{
    //public int uniqueID;
    public Vector3 position;
}

public class TLData
{
    //public int uniqueID;
    public List<Vector3> positions;
    public List<bool> states;
}

public class AgentData
{
    public List<Vector3> positions;
}

public class AgentController : MonoBehaviour
{
    // private string url = "https://boids.us-south.cf.appdomain.cloud/";
    public string serverUrl;
    string getCarsEndpoint = "/getCars";
    string getTlEndpoint = "/getTL";
    string getObstaclesEndpoint = "/getObstacle";
    string sendConfigEndpoint = "/init";
    string updateEndpoint = "/update";
    AgentData carsData, obstacleData;
    TLData tlData;
    GameObject[] agents;
    List<GameObject> tlAgents;
    List<Vector3> oldPositions;
    List<Vector3> newPositions;
    // Pause the simulation while we get the update from the server
    bool hold = false;
    bool first = true;

    public GameObject carPrefab, obstaclePrefab, floor, tlPrefab;
    public int NAgents, width, height;
    public float timeToUpdate = 5.0f, timer, dt;

    void Start()
    {
        // agent[i].GetComponent<Renderer>().material.color = Color.red; 
        carsData = new AgentData();
        obstacleData = new AgentData();
        tlData = new TLData();
        oldPositions = new List<Vector3>();
        newPositions = new List<Vector3>();
        tlAgents = new List<GameObject>();
        agents = new GameObject[NAgents];

        //floor.transform.localScale = new Vector3((float)width/10, 1, (float)height/10);
        //floor.transform.localPosition = new Vector3((float)width/2-0.5f, 0, (float)height/2-0.5f);
        
        for (int i = 0; i < NAgents; i++) {
            agents[i] = Instantiate(carPrefab, Vector3.zero, Quaternion.identity);
        }

            
        StartCoroutine(SendConfiguration());
    }

    void Update() 
    {
        float t = timer/timeToUpdate;
        // Smooth out the transition at start and end
        dt = t * t * ( 3f - 2f*t);

        Debug.Log("timer: " + timer);
        if(timer >= timeToUpdate)
        {
            timer = 0;
            hold = true;
            StartCoroutine(UpdateSimulation());
        }

        else if (!hold)
        {
            Debug.Log("oldPositionsLen: " + oldPositions.Count);
            Debug.Log("newPositionsLen: " + newPositions.Count);
            if (oldPositions.Count >= agents.Length) {
                for (int s = 0; s < agents.Length; s++)
                {
                    Debug.Log("s: " + s);
                    Vector3 interpolated = Vector3.Lerp(oldPositions[s], newPositions[s], dt);
                    agents[s].transform.localPosition = interpolated;
                    
                    Vector3 dir = oldPositions[s] - newPositions[s];
                    agents[s].transform.rotation = Quaternion.LookRotation(dir);
                }
            }
            timer += Time.deltaTime;
        }
    }
 
    IEnumerator UpdateSimulation()
    {
        UnityWebRequest www = UnityWebRequest.Get(serverUrl + updateEndpoint);
        yield return www.SendWebRequest();
 
        if (www.result != UnityWebRequest.Result.Success)
            Debug.Log(www.error);
        else 
        {
            yield return GetCarsData();
        }
    }

    IEnumerator SendConfiguration()
    {
        WWWForm form = new WWWForm();

        form.AddField("NAgents", NAgents.ToString());
        form.AddField("width", width.ToString());
        form.AddField("height", height.ToString());

        UnityWebRequest www = UnityWebRequest.Post(serverUrl + sendConfigEndpoint, form);
        www.SetRequestHeader("Content-Type", "application/x-www-form-urlencoded");

        yield return www.SendWebRequest();

        if (www.result != UnityWebRequest.Result.Success)
        {
            Debug.Log(www.error);
        }
        else
        {
            Debug.Log("Configuration upload complete!");
            Debug.Log("Getting Agents positions");
            yield return GetCarsData();
            yield return GetObstacleData();
            yield return GetTLData();
        }
    }

    IEnumerator GetCarsData() 
    {
        UnityWebRequest www = UnityWebRequest.Get(serverUrl + getCarsEndpoint);
        yield return www.SendWebRequest();
 
        if (www.result != UnityWebRequest.Result.Success)
            Debug.Log(www.error);
        else 
        {
            carsData = JsonUtility.FromJson<AgentData>(www.downloadHandler.text);

            // Store the old positions for each agent
            oldPositions = new List<Vector3>(newPositions);

            newPositions.Clear();

            foreach(Vector3 v in carsData.positions){
                newPositions.Add(v);
                if (first)
                    oldPositions.Add(v);
            }
        }
        yield return GetTLData();
    }

    IEnumerator GetObstacleData() 
    {
        UnityWebRequest www = UnityWebRequest.Get(serverUrl + getObstaclesEndpoint);
        yield return www.SendWebRequest();
 
        if (www.result != UnityWebRequest.Result.Success)
            Debug.Log(www.error);
        else 
        {
            obstacleData = JsonUtility.FromJson<AgentData>(www.downloadHandler.text);

            Debug.Log(obstacleData.positions);

            foreach(Vector3 position in obstacleData.positions)
            {
                Instantiate(obstaclePrefab, position, Quaternion.identity);
            }
        }
    }

    IEnumerator GetTLData()
    {
        UnityWebRequest www = UnityWebRequest.Get(serverUrl + getTlEndpoint);
        yield return www.SendWebRequest();

        if (www.result != UnityWebRequest.Result. Success)
            Debug.Log(www.error);
        else
        {
            tlData = JsonUtility.FromJson<TLData>(www.downloadHandler.text);

            if (first) {
                foreach(Vector3 position in tlData.positions)
                {
                    tlAgents.Add(Instantiate(tlPrefab , position, Quaternion.identity));
                }
            }

            for (int i = 0; i < tlData.positions.Count; i++) {
                if (!tlData.states[i])
                    tlAgents[i].GetComponent<Renderer>().material.SetColor("_Color", Color.red);
                else if (tlData.states[i])
                    tlAgents[i].GetComponent<Renderer>().material.SetColor("_Color", Color.green);
            }


            
            first = false; 
            hold = false;

        }
    }
}
