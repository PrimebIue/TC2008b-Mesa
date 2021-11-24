from flask import Flask, request, jsonify
from model import RobotsAndBoxes
from agents import Robot, Box, Objective

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
        print("desnity ", density)

        robotsModel = RobotsAndBoxes(height, width, density, number_agents)

        return jsonify({'message': 'INIT.'})


@app.route('/getRobots', methods=['GET'])
def getAgents():
    global robotsModel

    robots = []
    robotPositions = []

    for (a, x, z) in robotsModel.grid.coord_iter():
        for b in a:
            if isinstance(b, Robot):
                robots.append(b)

    robots.sort()
    for robot in robots:
        robotPositions.append({"x": robot.pos[0], "y": 0, "z": robot.pos[1]})

    return jsonify({'positions': robotPositions})


@app.route('/getBoxes', methods=['GET'])
def getBoxes():
    global robotsModel

    numBoxes = 0
    boxPositions = []
    boxes = []

    for (a, x, z) in robotsModel.grid.coord_iter():
        for b in a:
            if isinstance(b, Box):
                numBoxes += 1
                boxes.append(b)

    boxes.sort()
    for box in boxes:
        boxPositions.append({"x": box.pos[0], "y": 0, "z": box.pos[1]})

    return jsonify({'positions': boxPositions, "numBoxes": numBoxes})


@app.route('/getObj', methods=['GET'])
def getObj():
    global robotsModel

    objPosition = {"x": 0, "y": 0.05, "z": 0}

    for (a, x, z) in robotsModel.grid.coord_iter():
        for b in a:
            if isinstance(b, Objective):
                objPosition["x"] = x
                objPosition["z"] = z

    return jsonify({'position': objPosition})


@app.route('/update', methods=['GET'])
def updateModel():
    global currentStep, robotsModel
    if request.method == 'GET':
        robotsModel.step()
        currentStep += 1
        return jsonify({'message': f'Model updated to step {currentStep}.', 'currentStep': currentStep})


if __name__ == '__main__':
    app.run(host="localhost", port=8585, debug=True)
