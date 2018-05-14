from flask import Flask, request, make_response

import wisley.bus_layer as bl
from wisley.models import Node

import jsonpickle

from voluptuous import Schema, MultipleInvalid, Coerce, Required


app = Flask(__name__)

@app.route('/fbr')
def flower_bed_route():

    """Route takes
    plant (plant name number, coercible to integer)
    lat (latitude, coercible to float)
    long (longitude, coercible to float)
    Returns a Route object containing information about the route from the location given in
    the lat and long parameters to the closest instance of the plant given in the plant parameter"""

    # Define validation schema
    schema = Schema({
        Required('plant'): Coerce(int),
        Required('lat'): Coerce(float),
        Required('long'): Coerce(float),
    })

    # Validate and return a Bad Request error if necessary
    try:
        schema(request.args.to_dict())

    except MultipleInvalid as err:

        resp = handle_exception(err, '400')

    else:

        # Call business layer method and return an Internal Server Error if anything goes wrong
        try:
            f_bed_route = bl.get_flower_bed_route(request.args['plant'], Node(0, request.args['long'],
                                                                              request.args['lat'], ''))
            resp = get_response(f_bed_route)

        except Exception as err:
            resp = handle_exception(err, '500')

    return resp


@app.route('/point_route')
def poi_route():

    try:
        route = bl.get_poi_route(request.args['poi_id'], Node(0, request.args['long'], request.args['lat'], ''))
        resp = get_response(route)
    # route = bl.get_poi_route(2, Node(0, '-0.8570765', '51.2914787', ''))
    except Exception as err:
        resp = handle_exception(err)

    return resp


@app.route('/plant')
def get_plant():

    try:
        plant = bl.get_plant(request.args['name'])
        resp = get_response(plant)

    except Exception as err:
        resp = handle_exception(err)

    return resp


@app.route('/plants')
def get_plants():

    try:
        plants = bl.get_plant_list(request.args['string'], request.args['n'])
        resp = get_response(plants)

    except Exception as err:
        resp = handle_exception(err)

    return resp


@app.route('/point_int')
def points_of_int():

    try:
        points_of_int = bl.get_points_of_interest(Node(0, request.args['long'], request.args['lat'], ''),
                                                  request.args['n'])
        resp = get_response(points_of_int)

    except Exception as err:
        resp = handle_exception(err)

    return resp


@app.route('/flower_beds')
def flower_beds():

    try:
        flower_beds = bl.get_flower_beds(Node(0, request.args['long'], request.args['lat'], ''),
                                       request.args['plant'], request.args['n'])
        resp = get_response(flower_beds)

    except Exception as err:
        resp = handle_exception(err)

    return resp


def get_response(resp_obj):

    resp = make_response(jsonpickle.encode(resp_obj))
    resp.mimetype = 'application/json'

    return resp


def handle_exception(err, code):

    print("Exception: ", err)

    resp = make_response(jsonpickle.encode(str(err)))
    resp.mimetype = 'application/json'
    resp.status = code

    return resp


if __name__ == '__main__':
    app.run()
