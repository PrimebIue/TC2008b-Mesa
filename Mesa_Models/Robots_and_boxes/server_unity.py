from flask import Flask, request, jsonify
from model import RobotsAndBoxes
from agents import Robot, Box

# Board
number_agents = 4
width = 10
height = 10
robotsModel = None
density = 0
currentStep = 0

app = Flask("Robots and Boxes")


@app.route('/init', methods=['Post', 'GET'])
def initModel():
    global currentStep, robotsModel, number_agents, width, height, density

    if request.method == 'POST':
        number_agents = int(request.form.get('numAgents'))
        width = int(request.form.get('width'))
        height = int(request.form.get('height'))
        density = float(request.form.get('density'))
        currentStep = 0

        robotsModel = RobotsAndBoxes(height, width, density, number_agents)

        numBoxes = 0
        boxPositions = []

        for (a, x, z) in robotsModel.grid.coord_iter():
            numBoxes += 1
            if isinstance(a, Robot):
                boxPositions.append({"x": x, "y": 1, "z": z})

        return jsonify({'message': 'INIT.'})


@app.route('/getAgents', methods=['GET'])
def getAgents():
    global robotsModel

    if request.method == 'GET':
        robotPositions = [{"x": x, "y": 1, "z": z} for (
            a, x, z) in robotsModel.grid.coord_iter() if isinstance(a, Robot)]

        return jsonify({"positions": robotPositions})


@app.route('/getBoxes', methods=['GET'])
def getBoxes():
    global robotsModel

    numBoxes = 0
    boxPositions = []

    for (a, x, z) in robotsModel.grid.coord_iter():
        numBoxes += 1
        if isinstance(a, Robot):
            boxPositions.append({"x": x, "y": 1, "z": z})

        return jsonify({'positions': boxPositions, "numBoxes": numBoxes})


@app.route('/update', methods=['GET'])
def updateModel():
    global currentStep, robotsModel
    if request.method == 'GET':
        robotsModel.step()
        currentStep += 1
        return jsonify({'message': f'Model updated to step {currentStep}.', 'currentStep': currentStep})


if __name__ == '__main__':
    app.run(host="localhost", port=8585, debug=True)
