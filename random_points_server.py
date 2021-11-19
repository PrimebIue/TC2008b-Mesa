from random import uniform
from flask import Flask, request, jsonify

num_agents = 0
limit = 10


# Create the flask service
app = Flask("Coordinate server")


def random_point():
    """ Generate a new 3D Coordinate """
    return {"x": uniform(-limit, limit),
            "y": uniform(-limit, limit),
            "z": uniform(-limit, limit),
            }


@app.route("/")
def default():
    """ Test function for flask """
    print("Recieved a request at /")
    return "This is working!!"


@app.route("/config", methods=['POST'])
def configure():
    """ Set up the simulation """
    global num_agents
    num_agents = int(request.form.get("numAgents"))
    print(f"Received num_agents = {num_agents}")
    return jsonify({"OK": num_agents})


@app.route("/update", methods=['GET'])
def update_positions():
    # Create list of 3D points
    points = [random_point() for _ in range(num_agents)]
    print(f"Positions: {points}")
    return jsonify({"positions": points})


app.run()
