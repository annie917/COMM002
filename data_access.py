import mysql.connector
from  mysql.connector import errorcode
from models import Node

def find_nearest_node(cnx, location):

    # Arguments:
    # cnx - a database connection object
    # location - a Node object
    # Returns - a Node object representing the closest node to location

    cursor = cnx.cursor()

    point = node_to_point(location)

    sql = 'SELECT id, ST_AsText(coordinates), name, ST_Distance(' + point + ', coordinates) ' \
                                                                                'as dist from node order by dist;'
    cursor.execute(sql)

    node = row_to_node(cursor.fetchone())

    return node


def find_nearest_plant_bed(cnx, plant, location):

    # Arguments:
    # cnx - a database connection object
    # plant - the plant name number of the desired plant
    # location - the location of the user
    # Returns - a Node object representing the node closest to the closest flower bed containing
    # the desired plant
    # Returns - a Node object representing the centre of the closest flower bed

    cursor = cnx.cursor()

    point = node_to_point(location)


    sql = 'SELECT pb.bed_id, ST_Distance(' + point + ', fb.polygon) as dist, fb.nearest_node from plant_bed pb ' \
        'JOIN flower_bed fb on pb.bed_id = fb.id where pb.plant_id =' + plant + 'order by dist;'

    cursor.execute(sql)

    node = get_node_details(cnx, cursor.fetchone()[3])

    bed_centre = get_bed_centre(cnx, cursor.fetchone()[0])

    return node, bed_centre


def get_graph(cnx):

    # Arguments:
    # cnx - a database connection object
    # Returns - a NetworkX Graph object populated with nodes and edges

    return G


def get_bed_centre(cnx, bed_id):

    # Arguments:
    # cnx - a database connection object
    # bed_id - id of the flower bed in question
    # Returns - a Node object representing the centre of the flower bed

    cursor = cnx.cursor()

    sql = 'SELECT ST_Centroid(polygon) from flower_bed where id = ' + bed_id

    cursor.execute(sql)

    bed_centre = point_to_node(cursor.fetchone()[0])

    return bed_centre


def get_plant_attributes(cnx, plant_name_num):

    # Arguments:
    # cnx - a database connection object
    # plant_name_num - a plant name number
    # Returns - a Plant object populated with available attributes



    return plant


def get_node_details(cnx, node_id):

    # Arguments:
    # cnx - a database connection object
    # node_id - a node id
    # Returns - a Node object populated with full node details

    cursor = cnx.cursor()

    sql = 'SELECT id, ST_AsText(coordinates), name from node where id = ' + node_id

    cursor.execute(sql)

    node = row_to_node(cursor.fetchone())

    return node


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

def row_to_node(row):

    # Arguments:
    # row - a row from a cursor object
    # Returns - a populated Node object

    # Strip out the coordinates from converted POINT string
    x_and_y = row[1].lstrip('POINT(').rstrip(')').split(' ')

    # Create and populate a node object
    node = Node(row[0], float(x_and_y[0]), float(x_and_y[1]), row[2])

    return node


def node_to_point(node):

    # Arguments:
    # node - a Node object
    # Returns - a string representing a POINT as required by MySQL

    point = 'ST_PointFromText(\'POINT(' + node.long + ' ' + node.lat + ')\')'

    return point

def point_to_node(point):

    x_and_y = point.lstrip('POINT(').rstrip(')').split(' ')

    # Create and populate a node object
    node = Node(0, float(x_and_y[0]), float(x_and_y[1]), '')

    return node