from flask import Flask, request, make_response
import jsonpickle
from voluptuous import Schema, MultipleInvalid, Coerce, Required

from wisley.bus_layer import BLO_Plants
from wisley.bus_layer import BLO_PlantLists
from wisley.bus_layer import BLO_GIS
from wisley.bus_layer import BLO_Route
from wisley.models import GeoNode


app = Flask(__name__)


@app.route('/plants')
def get_plants():

    """@app.route('/plants') takes
    name (search string, string)
    n (max number of records required, coercible to int, n=0 returns all
    Searches the Preferred Common Name, Accepted Botanical Name, Synonyms and Common Names fields for the given name
    string (not case sensitive.  Returns a list of populated Plant objects, representing the first n instances found.
    If the name is not found, an empty list is returned.  If n=0, all matches are returned."""

    # Define validation schema
    schema = Schema({
        Required('name'): str,
        Required('n'): Coerce(int)
    })

    # Validate and return a Bad Request error if necessary
    try:
        schema(request.args.to_dict())

    except MultipleInvalid as err:

        resp = _handle_exception(err, '400')

    else:

        # Call business layer method and return an Internal Server Error if anything goes wrong
        try:
            bl = BLO_Plants()
            plants = bl.get_plants(request.args['name'], request.args['n'])
            resp = _get_response(plants)

        except Exception as err:
            resp = _handle_exception(err, '500')

    return resp


@app.route('/plants/seasonal')
def plants_seasonal():

    """@app.route('/plants/seasonal') takes
    month (month, coercible to int, 1=January)
    n (max number of records required, coercible to int, n=0 returns all
    Finds the first n plants of seasonal interest in the given month.
    Returns a list of populated Plant objects.
    If the name is not found, an empty list is returned.  If n=0, all matches are returned."""

    # Define validation schema

    schema = Schema({
        Required('month'): Coerce(int),
        Required('n'): Coerce(int)
    })

    # Validate and return a Bad Request error if necessary
    try:
        schema(request.args.to_dict())

    except MultipleInvalid as err:

        resp = _handle_exception(err, '400')

    else:

        # Call business layer method and return an Internal Server Error if anything goes wrong
        try:

            bl = BLO_PlantLists()

            plants = bl.get_seasonal_plants(request.args['month'], request.args['n'])

            resp = _get_response(plants)

        except Exception as err:

            resp = _handle_exception(err, '500')

    return resp

@app.route('/plants/bed')
def plants_bed():

    """@app.route('/plants/bed') takes
    id (bed id, coercible to int)
    n (max number of records required, coercible to int, n=0 returns all
    Finds the first n plants in the given bed.
    Returns a list of populated Plant objects.
    If the bed is not found or is emmpty, an empty list is returned.  If n=0, all matches are returned."""

    # Define validation schema

    schema = Schema({
        Required('id'): Coerce(int),
        Required('n'): Coerce(int)
    })

    # Validate and return a Bad Request error if necessary
    try:
        schema(request.args.to_dict())

    except MultipleInvalid as err:

        resp = _handle_exception(err, '400')

    else:

        # Call business layer method and return an Internal Server Error if anything goes wrong
        try:

            bl = BLO_PlantLists()

            plants = bl.get_bed_plants(request.args['id'], request.args['n'])

            resp = _get_response(plants)

        except Exception as err:

            resp = _handle_exception(err, '500')

    return resp


@app.route('/beds')
def get_beds():

    """@app.route('/beds') takes
    plant (plant name number, optional, coercible to int)
    lat (latitude, coercible to float)
    long (longitude, coercible to float)
    n (max number of records required, coercible to int, n=0 returns all
    Finds n flower beds containing a given plant (optional), sorted in order of proximity to a position defined by
    lat, long
    Returns a list of populated Node objects.
    If the plant is not found, an empty list is returned.  If n=0, all matches are returned."""

    # Define validation schema

    schema = Schema({
        'plant': Coerce(int),
        Required('lat'): Coerce(float),
        Required('long'): Coerce(float),
        Required('n'): Coerce(int)
    })

    # Validate and return a Bad Request error if necessary
    try:
        schema(request.args.to_dict())

    except MultipleInvalid as err:

        resp = _handle_exception(err, '400')

    else:

        # Call business layer method and return an Internal Server Error if anything goes wrong
        try:
            bl = BLO_GIS(GeoNode(0, '', request.args['long'], request.args['lat']))

            beds = bl.get_flower_beds(request.args.get('plant'), request.args['n'])

            resp = _get_response(beds)

        except Exception as err:

            resp = _handle_exception(err, '500')

    return resp


@app.route('/places')
def get_places():

    """@app.route('/places') takes
    lat (latitude, coercible to float)
    long (longitude, coercible to float)
    n (max number of records required, coercible to int, n=0 returns all
    Finds n places, sorted in order of proximity to a position defined by lat, long
    Returns a list of populated Place objects.
    If none are found, an empty list is returned.  If n=0, all matches are returned."""

    # Define validation schema

    schema = Schema({
        Required('lat'): Coerce(float),
        Required('long'): Coerce(float),
        Required('n'): Coerce(int)
    })

    # Validate and return a Bad Request error if necessary
    try:
        schema(request.args.to_dict())

    except MultipleInvalid as err:

        resp = _handle_exception(err, '400')

    else:

        # Call business layer method and return an Internal Server Error if anything goes wrong
        try:
            bl = BLO_GIS(GeoNode(0, '', request.args['long'], request.args['lat']))

            places = bl.get_places(request.args['n'])

            resp = _get_response(places)

        except Exception as err:

            resp = _handle_exception(err, '500')

    return resp


@app.route('/route/bed')
def route_bed():

    """@app.route('/route/bed') takes
    lat (latitude, coercible to float)
    long (longitude, coercible to float)
    id (id of a flower bed, coercible to int)
    Calculates the shortest route between the given flower bed and a position defined by lat, long
    Returns a Route object.
    If route cannot be calculated, an empty object is returned"""

    # Define validation schema

    schema = Schema({
        Required('lat'): Coerce(float),
        Required('long'): Coerce(float),
        Required('id'): Coerce(int)
    })

    # Validate and return a Bad Request error if necessary
    try:
        schema(request.args.to_dict())

    except MultipleInvalid as err:

        resp = _handle_exception(err, '400')

    else:

        # Call business layer method and return an Internal Server Error if anything goes wrong
        try:
            bl = BLO_Route(GeoNode(0, '', request.args['long'], request.args['lat']))

            route = bl.get_bed_route(request.args['id'])

            resp = _get_response(route)

        except Exception as err:

            resp = _handle_exception(err, '500')

    return resp


@app.route('/route/place')
def route_place():

    """@app.route('/route/place') takes
    lat (latitude, coercible to float)
    long (longitude, coercible to float)
    id (id of a place, coercible to int)
    Calculates the shortest route between the given place and a position defined by lat, long
    Returns a Route object.
    If route cannot be calculated, an empty object is returned"""

    # Define validation schema

    schema = Schema({
        Required('lat'): Coerce(float),
        Required('long'): Coerce(float),
        Required('id'): Coerce(int)
    })

    # Validate and return a Bad Request error if necessary
    try:
        schema(request.args.to_dict())

    except MultipleInvalid as err:

        resp = _handle_exception(err, '400')

    else:

        # Call business layer method and return an Internal Server Error if anything goes wrong
        try:

            bl = BLO_Route(GeoNode(0, '', request.args['long'], request.args['lat']))

            route = bl.get_place_route(request.args['id'])

            resp = _get_response(route)

        except Exception as err:

            resp = _handle_exception(err, '500')

    return resp


def _get_response(resp_obj):

    # Success!  Encode response and set up a Response object
    # Status code will be 200
    resp = make_response(jsonpickle.encode(resp_obj))
    resp.mimetype = 'application/json'

    return resp


def _handle_exception(err, code):

    # Failure! Encode error message and set up status
    print("Exception: ", err)

    resp = make_response(jsonpickle.encode(str(err)))
    resp.mimetype = 'application/json'
    resp.status = code

    return resp


if __name__ == '__main__':
    app.run()
