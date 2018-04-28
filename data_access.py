import mysql.connector
from models import Node

def find_nearest_node(cnx, location):

    # Finds the node nearest to location
    # Arguments:
    # cnx - a database connection object
    # location - a Node object
    # Returns - a Node object representing the closest node to location

    point = _node_to_point(location)

    sql = 'SELECT id, ST_AsText(coordinates), name, ST_Distance(' + point + ', coordinates) AS dist ' \
          'FROM node ' \
          'ORDER BY dist ' \
          'LIMIT 1;'

    row = _execute_query_one(cnx, sql)

    node = _row_to_node(row)

    return node


def find_nearest_plant_bed(cnx, plant, location):

    # Finds the closest flower bed to location that contains the plant
    # Arguments:
    # cnx - a database connection object
    # plant - the plant name number of the desired plant
    # location - the location of the user
    # Returns - a Node object representing the node closest to the closest flower bed containing
    # the desired plant
    # Returns - a Node object representing the centre of the closest flower bed

    point = _node_to_point(location)

    sql = 'SELECT pb.bed_id, ST_Distance(' + point + ', fb.polygon) AS dist, fb.nearest_node ' \
          'FROM plant_bed pb ' \
          'JOIN flower_bed fb ' \
          'ON pb.bed_id = fb.id ' \
          'WHERE pb.plant_id =' + plant + ' ' \
          'ORDER BY dist ' \
          'LIMIT 1;'

    row = _execute_query_one(cnx, sql)

    nearest_node = get_node_details(cnx, row[2])

    bed_centre = get_bed_centre(cnx, row[0])

    return bed_centre, nearest_node


def find_nearest_poi_node(cnx, poi_id):

    # Finds the closest node to poi_id, and also gets details of the point of interest
    # Arguments:
    # cnx - a database connection object
    # poi_id - the id of the point of interest
    # Returns:
    # A Node object representing the location of the point of interest
    # A Node object representing the nearest node to the point of interest

    sql = 'SELECT name, ST_AsText(coordinates), nearest_node ' \
          'FROM point_of_interest ' \
          'WHERE id =' + str(poi_id) + ';'

    row = _execute_query_one(cnx, sql)

    # Get the full details of the nearest node
    nearest_node = get_node_details(cnx, row[2])

    point_of_int = _point_to_node(row[1])
    point_of_int.name = row[0]

    return point_of_int, nearest_node


def get_graph(cnx):

    import networkx as nx

    # Populates a NetworkX Graph object using the edge database table
    # Arguments:
    # cnx - a database connection object
    # Returns - a NetworkX Graph object populated with nodes and edges

    cursor = cnx.cursor()

    query = 'SELECT node1, node2, weight ' \
            'FROM edge'

    cursor.execute(query)

    G = nx.Graph()

    for node1, node2, weight in cursor:
        G.add_edge(node1, node2, weight=weight)

    cursor.close()

    return G


def get_bed_centre(cnx, bed_id):

    # Gets the mathematical centroid of the flower bed with id = bed_id
    # Arguments:
    # cnx - a database connection object
    # bed_id - id of the flower bed in question
    # Returns - a Node object representing the centroid of the flower bed polygon

    sql = 'SELECT ST_AsText(ST_Centroid(polygon)) ' \
          'FROM flower_bed ' \
          'WHERE id = ' + str(bed_id)

    row = _execute_query_one(cnx, sql)

    bed_centre = _point_to_node(row[0])

    bed_centre.name = 'Centre bed ' + str(bed_id)

    return bed_centre


def get_plant_attributes(cnx, plant_name_num):

    # Arguments:
    # cnx - a database connection object
    # plant_name_num - a plant name number
    # Returns - a Plant object populated with available attributes



    return plant


def get_points_of_interest(cnx, location, n):

    # Gets the n closest points of interest to location, sorted by distance from location
    # Arguments:
    # cnx - a database connection object
    # location - a Node object with the current location
    # n - the number of points of interest to be returned (0 returns all)
    # Returns - a list of Node objects representing points of interest

    cursor = cnx.cursor()

    point = _node_to_point(location)

    sql = 'SELECT id, ST_AsText(coordinates), name, ST_Distance(' + point + ', coordinates) AS dist ' \
          'FROM point_of_interest ' \
          'ORDER BY dist'

    # Limit query to n rows if required
    if n != '0':
        sql += ' LIMIT '
        sql += n

    sql += ';'

    cursor.execute(sql)

    points_of_int = []

    # Copy points of interest to Node object and append to list
    for row in cursor:

        node = _point_to_node(row[1])

        node.id = row[0]
        node.name = row[2]

        points_of_int.append(node)

    cursor.close()

    return points_of_int


def get_node_details(cnx, node_id):

    # Gets full details from node table for id = node_id
    # Arguments:
    # cnx - a database connection object
    # node_id - a node id
    # Returns - a Node object populated with full node details

    sql = 'SELECT id, ST_AsText(coordinates), name ' \
          'FROM node ' \
          'WHERE id = ' + str(node_id)

    row = _execute_query_one(cnx, sql)

    return _row_to_node(row)


def db_connect():

    # Arguments - None
    # Returns connection object

    cnx = mysql.connector.connect(user='root', host='localhost', database='wisley')

    return cnx


def db_close(cnx):

    # Arguments:
    # cnx - connection object
    # Returns - Nothing

    cnx.close()

    return


def _execute_query_one(cnx, sql):

    # Returns first result for query defined in sql parameter
    # Arguments:
    # sql - string containing SQL query
    # Returns - a row tuple representing the first row from the query

    cursor = cnx.cursor()

    cursor.execute(sql)

    row = cursor.fetchone()

    cursor.close()

    return row


def _row_to_node(row):

    # Converts a node table row tuple to a Node object
    # Arguments:
    # row - a row (Node table) from a cursor object
    # Returns - a populated Node object

    # Strip out the coordinates from converted POINT string
    long_and_lat = row[1].lstrip('POINT(').rstrip(')').split(' ')

    # Create and populate a node object
    node = Node(row[0], long_and_lat[0], long_and_lat[1], row[2])

    return node


def _node_to_point(node):

    # Converts a Node object to POINT format required in SQL
    # Arguments:
    # node - a Node object
    # Returns - a string representing a POINT as required by MySQL

    point = 'ST_PointFromText(\'POINT(' + node.long + ' ' + node.lat + ')\')'

    return point

def _point_to_node(point):

    # Converts a POINT MySQL string to a node object
    # Arguments:
    # point - a string representing a MySQL POINT data type
    # Returns a populated Node object, with lat and long from point, id=0 and blank name

    long_and_lat = point.lstrip('POINT(').rstrip(')').split(' ')

    # Create and populate a node object
    node = Node(0, long_and_lat[0], long_and_lat[1], '')

    return node