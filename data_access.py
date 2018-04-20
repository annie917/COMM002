def find_nearest_node(location):

    # Arguments:
    # location - a Node object
    # Returns - a Node object representing the closest node to location

    return node_id


def find_nearest_plant_bed(plant, location):

    # Arguments:
    # plant - the plant name number of the desired plant
    # location - the location of the user
    # Returns - a Node object representing the node closest to the closest flower bed containing
    # the desired plant
    # Returns - a Node object representing the centre of the closest flower bed

    sql = '''SELECT pb.bed_id, st_distance(ST_PointFromText('POINT(-0.8550134 51.2907038)'), fb.polygon) as res, fb.nearest_node
    from plant_bed pb JOIN flower_bed fb on pb.bed_id = fb.id where pb.plant_id = 72209
    order by res;'''

    return node_id, bed_centre


def get_graph():

    # Arguments - None
    # Returns - a NetworkX Graph object populated with nodes and edges

    return G


def get_bed_centre(bed_id):

    # Arguments:
    # bed_id - id of the flower bed in question
    # Returns - a Node object representing the centre of the flower bed

    return bed_centre


def get_plant_attributes(plant_name_num):

    # Arguments:
    # plant_name_num - a plant name number
    # Returns - a Plant object populated with available attributes


    return plant

def db_connect():

    # Arguments - None
    # Returns connection object

    return cnx


def db_close(cnx):

    # Arguments:
    # cnx - connection object
    # Returns - Nothing

    return