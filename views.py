from flask import Flask, request, Response, make_response
import bus_layer as bl
from models import Node
import jsonpickle

app = Flask(__name__)


@app.route('/')
def hello_world():
    return 'Hello, World!'


@app.route('/fbr')
def flower_bed_route():

    f_bed_route = bl.get_flower_bed_route(request.args['plant'], Node(0, request.args['long'], request.args['lat'], ''))

    # f_bed_route = bl.get_flower_bed_route('72209', Node(0, '-0.8570765', '51.2914787', ''))

    return get_response(f_bed_route)


@app.route('/point_route')
def poi_route():

    route = bl.get_poi_route(request.args['poi_id'], Node(0, request.args['long'], request.args['lat'], ''))
    # route = bl.get_poi_route(2, Node(0, '-0.8570765', '51.2914787', ''))

    return get_response(route)


@app.route('/pnn')
def plant_name_num():
    return 'Plant name num route'\


@app.route('/plants')
def get_plants():
    return 'Get plants route'\


@app.route('/point_int')
def points_of_int():

    points_of_int = bl.get_points_of_interest(Node(0, request.args['long'], request.args['lat'], ''), request.args['n'])

    return get_response(points_of_int)


@app.route('/flower_beds')
def flower_beds():

    flower_beds = bl.get_flower_beds(Node(0, request.args['long'], request.args['lat'], ''),
                                       request.args['plant'], request.args['n'])

    return get_response(flower_beds)


def get_response(resp_obj):

    resp = make_response(jsonpickle.encode(resp_obj))
    resp.mimetype = 'application/json'

    return resp


if __name__ == '__main__':
    app.run()
