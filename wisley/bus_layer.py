from wisley.data_access import DAO_Plants
from wisley.data_access import DAO_GIS
from wisley.data_access import DAO_Route
from wisley.models import Route


class BL_Plants(object):

    def __init__(self):

        self.db = DAO_Plants()

    def get_plant_list(self, search_string, n):

        # Searches all relevant fields for search_string and returns first n instances as list of Plant objects
        # Arguments:
        # search_string - a string for searching all possible name fields in the plant selector xml
        # n - maximum number of plants to maintain
        # Returns - a list of populated Plant objects, or an empty list if the search string was not found

        plants = self.db.get_plants(search_string, n)

        return plants


class BL_GIS(object):

    def __init__(self, location):

        self.db = DAO_GIS(location)

    def get_flower_beds(self, plant, n):

        # Gets the n closest flower beds to location, which contain plant
        # Arguments:
        # location - a Node Object
        # plant - a plant name number
        # n - maximum number of beds to be returned
        # Returns:
        # A list of Node Objects representing the n flower beds

        flower_beds = self.db.get_flower_beds(plant, n)

        self.db.db_close()

        return flower_beds

    def get_places(self, n):

        # Gets n closest points of interest to location
        # Arguments:
        # location - a Node object
        # n - maximum number of points of interest to return.  0 will return all
        # Returns - a list of n PointOfInterest objects, sorted by distance from location

        places = self.db.get_places(n)

        self.db.db_close()

        return places

    def get_seasonal_plants(self, month, n):

        plants = self.db.get_seasonal_plants(month, n)

        return plants

    def get_seasonal_plants_near_me(self, month, n):

        plants = self.db.get_seasonal_plants_near_me(month, n)

        return plants

class BL_Route():

    def __init__(self, location):

        self.db = DAO_Route(location)

    def get_place_route(self, id):

        route = self.get_route(self.db.find_nearest_place_node(id))
        route.destination = self.db.get_place(id)

        return route

    def get_bed_route(self, id):

        route = self.get_route(self.db.find_nearest_bed_node(id))
        route.destination = self.db.get_bed_centre(id)

        return route

    def get_route(self, dest_node_id):

        import networkx as nx

        # Arguments:
        # cnx - database connection object
        # start_node - a Node object
        # dest_node - a Node object
        # Returns - a Route object populated with the shortest route between start_node and dest_node

        # Read in network from database
        G = self.db.get_graph()
        start_node = self.db.find_nearest_node()

        route = Route()

        # Calculate shortest route and route length
        nodes = nx.astar_path(G, start_node.id, dest_node_id)
        route.length = nx.astar_path_length(G, start_node.id, dest_node_id)

        node1 = 0

        # Loop through nodes getting full details and directions from database

        for node in nodes:

            route.nodes.append(self.db.get_node_details(node))

            node2 = node

            if len(route.nodes) > 1:
                route.directions.append(self.db.get_directions(node1, node2))

            node1 = node

        return route


# def get_flower_bed_route(plant_name_num, location):
#
#     # Arguments:
#     # plant - the plant name number of the desired plant
#     # location - the location of the user
#     # Returns - a list of Node objects representing the shortest route between the user and the plant
#     # Returns - a Node object representing the centre of the closest flower bed
#
#     # Get a new database connection
#
#     cnx = db.db_connect()
#
#     # Get closest node to user
#     user_node = db.find_nearest_node(cnx, location)
#
#     # Get closest flower bed containing plant
#     nearest_node, bed_centre  = db.find_nearest_plant_bed(cnx, plant_name_num, location)
#
#     # Get route between user and flower bed
#     route = get_route(cnx, user_node, nearest_node)
#     route.destination = bed_centre
#
#     # Close database connection
#     db.db_close(cnx)
#
#     return route
#
#
# def get_poi_route(point_of_int, location):
#     # Arguments:
#     # point_of_int - the id of the desired point of interest
#     # location - node object representing users location
#     # Returns - a list of Node objects representing the shortest route between location and POI
#     # Get a new database connection
#
#     cnx = db.db_connect()
#
#     # Get closest node to user
#     user_node = db.find_nearest_node(cnx, location)
#
#     # Get closest node to POI
#     poi_node, nearest_node = db.find_nearest_poi_node(cnx, point_of_int)
#
#     # Get route between user and POI
#     route = get_route(cnx, user_node, nearest_node)
#     route.destination = poi_node
#
#     # Close database connection
#     db.db_close(cnx)
#
#     return route
#
#
#
#
# def get_plant(common_name):
#
#     # Given an (exact) common name, returns a Plant object populated with the corresponding attributes   v bents:
#     # common_name - a string containing the common name of the desired plant
#     # Returns - a populated Plant object
#
#     # plant_name_num = db.get_plant_name_num(common_name)
#
#     plant = db.get_plant_attributes(common_name)
#
#     return plant
