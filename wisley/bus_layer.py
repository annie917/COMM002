import wisley.data_access as db
from wisley.models import Route


def get_flower_bed_route(plant_name_num, location):

    # Arguments:
    # plant - the plant name number of the desired plant
    # location - the location of the user
    # Returns - a list of Node objects representing the shortest route between the user and the plant
    # Returns - a Node object representing the centre of the closest flower bed

    # Get a new database connection

    cnx = db.db_connect()

    # Get closest node to user
    user_node = db.find_nearest_node(cnx, location)

    # Get closest flower bed containing plant
    nearest_node, bed_centre  = db.find_nearest_plant_bed(cnx, plant_name_num, location)

    # Get route between user and flower bed
    route = get_route(cnx, user_node, nearest_node)
    route.destination = bed_centre

    # Close database connection
    db.db_close(cnx)

    return route


def get_poi_route(point_of_int, location):
    # Arguments:
    # point_of_int - the id of the desired point of interest
    # location - node object representing users location
    # Returns - a list of Node objects representing the shortest route between location and POI
    # Get a new database connection

    cnx = db.db_connect()

    # Get closest node to user
    user_node = db.find_nearest_node(cnx, location)

    # Get closest node to POI
    poi_node, nearest_node = db.find_nearest_poi_node(cnx, point_of_int)

    # Get route between user and POI
    route = get_route(cnx, user_node, nearest_node)
    route.destination = poi_node

    # Close database connection
    db.db_close(cnx)

    return route


def get_route(cnx, start_node, dest_node):

    import networkx as nx

    # Arguments:
    # cnx - database connection object
    # start_node - a Node object
    # dest_node - a Node object
    # Returns - a Route object populated with the shortest route between start_node and dest_node

    # Read in network from database
    G = db.get_graph(cnx)

    route = Route()

    # Calculate shortest route and route length
    nodes = nx.astar_path(G, start_node.id, dest_node.id)
    route.length = nx.astar_path_length(G, start_node.id, dest_node.id)

    node1 = 0

    # Loop through nodes getting full details and directions from database

    for node in nodes:

        route.nodes.append(db.get_node_details(cnx, node))

        node2 = node

        if len(route.nodes) > 1:

            route.directions.append(db.get_directions(cnx, node1, node2))

        node1 = node

    return route


def get_plant(common_name):

    # Given an (exact) common name, returns a Plant object populated with the corresponding attributes   v bents:
    # common_name - a string containing the common name of the desired plant
    # Returns - a populated Plant object

    # plant_name_num = db.get_plant_name_num(common_name)

    plant = db.get_plant_attributes(common_name)

    return plant


def get_plant_list(search_string, n):

    # Searches all relevant fields for search_string and returns first n instances as list of Plant objects
    # Arguments:
    # search_string - a string for searching all possible name fields in the plant selector xml
    # n - maximum number of plants to maintain
    # Returns - a collection of populated Plant objects

    plants = db.get_plants(search_string, n)

    return plants


def get_points_of_interest(location, n):

    # Gets n closest points of interest to location
    # Arguments:
    # location - a Node object
    # n - maximum number of points of interest to return.  0 will return all
    # Returns - a list of n PointOfInterest objects, sorted by distance from location

    cnx = db.db_connect()

    points_of_int = db.get_points_of_interest(cnx, location, n)

    db.db_close(cnx)

    return points_of_int

def get_flower_beds(location, plant, n):

    # Gets the n closest flower beds to location, which contain plant
    # Arguments:
    # location - a Node Object
    # plant - a plant name number
    # n - maximum number of beds to be returned
    # Returns:
    # A list of Node Objects representing the n flower beds

    cnx = db.db_connect()

    flower_beds = db.get_flower_beds(cnx, location, plant, n)

    db.db_close(cnx)

    return flower_beds

