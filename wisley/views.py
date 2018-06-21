from flask import Flask, request, make_response
import jsonpickle
from voluptuous import Schema, MultipleInvalid, Coerce, Required, All, Length, Range

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
    {Searches the Preferred Common Name, Accepted Botanical Name, Synonyms and Common Names fields for the given name
    string (not case sensitive.} OR
    month (month, coercible to int, 1=January)
    {Finds the first n plants of seasonal interest in the given month.} OR
    id (bed id, coercible to int)
    {Finds the first n plants in the given bed.}
    n (max number of records required, coercible to int, n=0 (default) returns all
    Returns a list of populated Plant objects, representing the first n instances found.
    If plants matching criteria are not found, an empty list is returned.  """

    # Define validation schema
    schema = Schema({
        'name': All(str, Length(min=1)),
        'month': All(Coerce(int), Range(min=1, max=12)),
        'id': Coerce(int),
        'n': Coerce(int)
    })

    # Validate and return a Bad Request error if necessary
    try:
        schema(request.args.to_dict())

    except MultipleInvalid as err:

        resp = _handle_exception(err, '400')

    else:

        # Call business layer method and return an Internal Server Error if anything goes wrong
        try:

            # Default n to 0
            if request.args.get('n'):
                n = request.args['n']
            else:
                n = '0'

            # Check which argument we have and set up appropriate BLO
            if request.args.get('month'):

                bl = BLO_PlantLists()
                plants = bl.get_seasonal_plants(request.args['month'], n)
                resp = _get_response(plants)

            elif request.args.get('id'):

                bl = BLO_PlantLists()
                plants = bl.get_bed_plants(request.args['id'], n)
                resp = _get_response(plants)

            elif request.args.get('name'):

                bl = BLO_Plants()
                plants = bl.get_plants(request.args['name'], n)
                resp = _get_response(plants)

            else:

                # No arguments provided, return bad request error
                resp = _handle_exception('Provide either name, month or id', '400')

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
        'n': Coerce(int)
    })

    # Validate and return a Bad Request error if necessary
    try:
        schema(request.args.to_dict())

    except MultipleInvalid as err:

        resp = _handle_exception(err, '400')

    else:

        # Call business layer method and return an Internal Server Error if anything goes wrong
        try:

            # Default n to 0
            if request.args.get('n'):
                n = request.args['n']
            else:
                n = '0'

            bl = BLO_GIS(GeoNode(0, '', request.args['long'], request.args['lat']))

            beds = bl.get_flower_beds(request.args.get('plant'), n)

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
        'n': Coerce(int)
    })

    # Validate and return a Bad Request error if necessary
    try:
        schema(request.args.to_dict())

    except MultipleInvalid as err:

        resp = _handle_exception(err, '400')

    else:

        # Call business layer method and return an Internal Server Error if anything goes wrong
        try:

            # Default n to 0
            if request.args.get('n'):
                n = request.args['n']
            else:
                n = '0'

            bl = BLO_GIS(GeoNode(0, '', request.args['long'], request.args['lat']))

            places = bl.get_places(n)

            resp = _get_response(places)

        except Exception as err:

            resp = _handle_exception(err, '500')

    return resp


@app.route('/routes/bed/<int:id>')
def route_bed(id):

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
        Required('long'): Coerce(float)
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

            route = bl.get_bed_route(id)

            resp = _get_response(route)

        except Exception as err:

            resp = _handle_exception(err, '500')

    return resp


@app.route('/routes/place/<int:id>')
def route_place(id):

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
        Required('long'): Coerce(float)
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

            route = bl.get_place_route(id)

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
