from flask import Flask, request
import bus_layer as bl
from models import Node
import json

app = Flask(__name__)


@app.route('/')
def hello_world():
    return 'Hello, World!'

@app.route('/fbr')
def flower_bed_route():

    # bl.get_flower_bed_route(request.args['plant'], Node(0, request.args['lat'], request.args['long'], ''))

    f_bed_route = bl.get_flower_bed_route('72209', Node(0, '-0.8570765', '51.2914787', ''))


    return 'Flower bed route'

@app.route('/point_route')
def poi_route():
    return 'Point of interest route'

@app.route('/pnn')
def plant_name_num():
    return 'Plant name num route'\

@app.route('/plants')
def get_plants():
    return 'Get plants route'\

@app.route('/point_int')
def points_of_int():
    return 'Get points of interest route'\

if __name__ == '__main__':
    app.run()
