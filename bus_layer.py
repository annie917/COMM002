import data_access as db
from models import Route

def get_flower_bed_route(plant, location):
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
    bed_centre, nearest_node = db.find_nearest_plant_bed(cnx, plant, location)

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


def get_route(cnx, node1, node2):

    import networkx as nx

    # Arguments:
    # cnx - database connection object
    # node1 - a Node object
    # node2 - a Node object
    # Returns - a list of Node objects representing the shortest route between node1 and node2

    G = db.get_graph(cnx)

    nodes = nx.astar_path(G, node1.id, node2.id)

    route = Route()

    route.length = nx.astar_path_length(G, node1.id, node2.id)

    for node in nodes:
        route.nodes.append(db.get_node_details(cnx, node))

    return route


def get_plant_name_num(common_name):
    # Arguments:
    # common_name - a string containing the common name of the desired plant
    # Returns - a string containing the plant name num if found, otherwise an empty string

    return plant_name_num


def get_plant_list(search_string, n):
    # Arguments:
    # search_string - a string for searching all possible name fields in the plant selector xml
    # n - maximum number of plants to maintain
    # Returns - a collection of populated Plant objects

    return plants


def get_points_of_interest(location, n):
    # Arguments:
    # location - a Node object
    # n - maximum number of points of interest to return.  0 will return all
    # Returns - a list of n PointOfInterest objects, sorted by distance from location

    return points_of_int

