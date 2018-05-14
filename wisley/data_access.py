import mysql.connector
from wisley.models import Node
from wisley.models import Plant
from wisley.models import Direction

def find_nearest_node(cnx, location):

    # Finds the node nearest to location
    # Arguments:
    # cnx - a database connection object
    # location - a Node object
    # Returns - a Node object representing the closest node to location

    sql = 'SELECT id, ST_AsText(coordinates), name, ST_Distance(' + location.point_str() + ', coordinates) AS dist ' \
          'FROM node ' \
          'ORDER BY dist ' \
          'LIMIT 1;'

    row = _execute_query_one(cnx, sql)

    return Node.from_db_row(row)


def find_nearest_plant_bed(cnx, plant, location):

    # Finds the closest flower bed to location that contains the plant
    # Arguments:
    # cnx - a database connection object
    # plant - the plant name number of the desired plant
    # location - the location of the user
    # Returns - a Node object representing the node closest to the closest flower bed containing
    # the desired plant
    # Returns - a Node object representing the centre of the closest flower bed

    sql = 'SELECT pb.bed_id, ST_Distance(' + location.point_str() + ', fb.polygon) AS dist, fb.nearest_node ' \
          'FROM plant_bed pb ' \
          'JOIN flower_bed fb ' \
          'ON pb.bed_id = fb.id ' \
          'WHERE pb.plant_id =' + plant + ' ' \
          'ORDER BY dist ' \
          'LIMIT 1;'

    row = _execute_query_one(cnx, sql)

    nearest_node = get_node_details(cnx, row[2])

    bed_centre = get_bed_centre(cnx, row[0])

    return nearest_node, bed_centre


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

    point_of_int = Node.from_point_string(row[1])
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

    bed_centre = Node.from_point_string(row[0])

    bed_centre.name = 'Centre bed ' + str(bed_id)

    return bed_centre


def get_plant_name_num(common_name):

    import lxml.etree as etree
    import configparser

    config = configparser.ConfigParser()
    config.read('config.ini')
    xml_file_name = config['XML']['file_path']

    plant_name_num = ''

    for event, elem in etree.iterparse(xml_file_name, events=("start", "end")):
        if event == "start":
            if elem.tag == 'EntityDetailsItems':
                if elem.attrib['PreferredCommonName'] == common_name:
                    plant_name_num = elem.attrib['Name_Num']
                    break

        elem.clear()

    return plant_name_num


def get_plant_attributes(pref_common_name):

    # Populates and returns a plant object for the given (exact) pref_common_name
    # Arguments:
    # pref_common_name - preferred common name (string)
    # Returns - a Plant object populated with available attributes

    import lxml.etree as etree
    import configparser

    config = configparser.ConfigParser()
    config.read('config.ini')
    xml_file_name = config['XML']['file_path']

    plant = Plant()

    for event, elem in etree.iterparse(xml_file_name, events=("start", "end")):

        if event == "start" and elem.tag == 'EntityDetailsItems':
            # Start of a plant - check if correct one then populate object with attributes
            if elem.attrib['PreferredCommonName'] == pref_common_name:
                plant.populate_xml(elem)

        elif event == 'end':

            # Add any common names or synonyms to the plant object
            if (elem.tag == 'CommonName' or elem.tag == 'Synonyms') and plant.common_name == pref_common_name:

                    if elem.tag == 'CommonName' and elem.text:
                        plant.common_names.append(elem.text)
                    elif elem.tag == 'Synonyms' and elem.text:
                        plant.synonyms.append(elem.text)

            elif elem.tag == 'EntityDetailsItems':

                # Plant finished - delete extra synonym caused by extra XML tag, then break
                if plant.common_name == pref_common_name:
                    elem.clear()
                    if plant.synonyms:
                        del plant.synonyms[-1]
                        break

            # Clear element when finished with it to save memory
            elem.clear()

    return plant


def get_plants(search_string, n):

    # Examines the PreferredCommonName, AcceptedBotanicalName, CommonName and Synonyms fields for the search string
    # and returns a list of n Plant objects populated with the attributes of the first n matches
    # Arguments:
    # search_string - string to be matched
    # n - maximum required number of plants, 0 returns all
    # Returns - A list of max n Plant objects, populated with attributes

    import lxml.etree as etree
    import configparser

    config = configparser.ConfigParser()
    config.read('config.ini')
    xml_file_name = config['XML']['file_path']

    s = search_string.lower()
    plants = []
    found = False

    for event, elem in etree.iterparse(xml_file_name, events=("start", "end")):

        if event == "start" and elem.tag == 'EntityDetailsItems':

                plant_elem = elem

                # Start of a plant - check relevant attributes

                if s in plant_elem.attrib['PreferredCommonName'].lower() or \
                        s in plant_elem.attrib['AcceptedBotanicalName'].lower():

                    plant = Plant()
                    plant.populate_xml(plant_elem)

                    found = True

        elif event == 'end':

            if elem.tag == 'CommonName' or elem.tag == 'Synonyms':

                # Only check common names and synonyms if attributes didn't match
                if not found:
                     if elem.text:
                        if s in elem.text.lower():
                            plant = Plant()
                            plant.populate_xml(plant_elem)
                            found = True

                # If plant has been stored, add any common names and synonyms
                if found:
                    if elem.tag =='CommonName' and elem.text:
                        plant.common_names.append(elem.text)
                    elif elem.tag == 'Synonyms' and elem.text:
                        plant.synonyms.append(elem.text)

            elif elem.tag == 'EntityDetailsItems':

                # End of a plant
                # Break if we have enough records, else reset found
                if found:
                    if plant.synonyms:
                        # Delete extra synonym generated by extra XML tag
                        del plant.synonyms[-1]

                    plants.append(plant)

                    if (len(plants) >= int(n)) and (n != '0'):
                        break
                    else:
                        found = False

            # Clear the element to save memory
            elem.clear()
            plant_elem.clear()

    return plants


def get_points_of_interest(cnx, location, n):

    # Gets the n closest points of interest to location, sorted by distance from location
    # Arguments:
    # cnx - a database connection object
    # location - a Node object with the current location
    # n - the number of points of interest to be returned (0 returns all)
    # Returns - a list of Node objects representing points of interest

    cursor = cnx.cursor()

    sql = 'SELECT id, ST_AsText(coordinates), name, ST_Distance(' + location.point_str() + ', coordinates) AS dist ' \
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

        node = Node.from_point_string(row[1])

        node.id = row[0]
        node.name = row[2]

        points_of_int.append(node)

    cursor.close()

    return points_of_int


def get_flower_beds(cnx, location, plant, n):

    # Gets the n closest flower beds to location which contain plant, sorted by distance from location
    # Arguments:
    # cnx - a database connection object
    # location - a Node object with the current location
    # n - the number of points of interest to be returned (0 returns all)
    # Returns - a list of Node objects representing points of interest

    cursor = cnx.cursor()

    sql = 'SELECT pb.bed_id, ST_Distance(' + location.point_str() + ', fb.polygon) AS dist, ' \
                                                                    'ST_AsText(ST_Centroid(polygon)) ' \
          'FROM plant_bed pb ' \
          'JOIN flower_bed fb ' \
          'ON pb.bed_id = fb.id ' \
          'WHERE pb.plant_id =' + plant + ' ' \
          'ORDER BY dist'

    # Limit query to n rows if required
    if n != '0':
        sql += ' LIMIT '
        sql += n

    sql += ';'

    cursor.execute(sql)

    flower_beds = []

    # Copy flower bed to Node object and append to list
    for row in cursor:

        node = Node.from_point_string(row[2])

        node.id = row[0]
        node.name = 'Flower Bed ' + str(node.id)

        flower_beds.append(node)

    cursor.close()

    return flower_beds


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

    return Node.from_db_row(row)


def get_directions(cnx, node1, node2):

    # Gets directions from node1 --> node2
    # Arguments:
    # node1 - id of origin node
    # node2 - id of destination node
    # Returns a populated Direction object

    # Edges are stored such that node1 < node2, swap nodes over if needed

    if node1 < node2:
        query_node1 = node1
        query_node2 = node2
        column = 'direction_1_to_2'
    else:
        query_node1 = node2
        query_node2 = node1
        column = 'direction_2_to_1'

    sql = 'SELECT ' + column + ', weight ' \
          'FROM edge ' \
          'WHERE node1 = ' + str(query_node1) + ' AND node2 = ' + str(query_node2)

    row = _execute_query_one(cnx, sql)

    return Direction(node1, node2, row[1], row[0])


def db_connect():

    import configparser

    # Arguments - None
    # Returns connection object

    config = configparser.ConfigParser()
    config.read('config.ini')

    user = config['MySql']['user']
    host = config['MySql']['host']
    database = config['MySql']['database']

    cnx = mysql.connector.connect(user=user, host=host, database=database)

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
