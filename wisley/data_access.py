from wisley.models import ProjNode
from wisley.models import GeoNode
from wisley.models import Place
from wisley.models import Plant
from wisley.models import Stage

import configparser


class DAO_Plants(object):


    # Data access class for extracting plant info from XML.  Does not deal with RDBMS.

    def __init__(self):

        # Read in configuration file and set up xml file name
        config = configparser.ConfigParser()
        config.read('config.ini')
        self.xml_file_name = config['XML']['file_path']

    def plant_attributes(self, name_num):

        import xml.etree.ElementTree as etree

        # Searches XML for exact match on name_num and returns fully populated Plant object
        # Arguments:
        # name_num - plant name_num to be found
        # Returns - A Plant objects populated with attributes

        found = False

        for event, elem in etree.iterparse(self.xml_file_name, events=("start", "end")):

            if event == "start" and elem.tag == 'EntityDetailsItems':

                plant_elem = elem

                # Start of a plant - check relevant attributes

                if plant_elem.attrib['Name_Num'] == str(name_num):

                    found = True
                    plant = Plant()
                    plant.populate_xml(plant_elem)

                    if elem.tag == 'CommonName' and elem.text:
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

                        break

                # Clear the element to save memory
                elem.clear()
                plant_elem.clear()

        return plant

    def plants(self, search_string, n):

        import xml.etree.ElementTree as etree

        # Examines the PreferredCommonName, AcceptedBotanicalName, CommonName and Synonyms fields for the search string
        # and returns a list of n Plant objects populated with the attributes of the first n matches
        # Arguments:
        # search_string - string to be matched
        # n - maximum required number of plants, 0 returns all
        # Returns - A list of max n Plant objects, populated with attributes

        s = search_string.lower()
        plants = []
        found = False

        for event, elem in etree.iterparse(self.xml_file_name, events=("start", "end")):

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
                        if elem.tag == 'CommonName' and elem.text:
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


class DAO_Basics(object):

    # Base class for all DAO classes that interact with RDBMS

    def __init__(self):

        import mysql.connector

        # Read db details for configuration file and establish connection to database.
        # Set up location attribute
        config = configparser.ConfigParser()
        config.read('config.ini')

        user = config['MySql']['user']
        host = config['MySql']['host']
        database = config['MySql']['database']
        password = config['MySql']['password']

        self.connection = mysql.connector.connect(user=user, host=host, database=database, password=password)

    def db_close(self):

        # Close database connection

        self.connection.close()

        return

    def _execute_query(self, sql):

        # Returns first result for query defined in sql parameter
        # Arguments:
        # sql - string containing SQL query
        # Returns - a row tuple representing the first row from the query

        cursor = self.connection.cursor()

        cursor.execute(sql)

        row = cursor.fetchone()

        cursor.close()

        return row


class DAO_Location(DAO_Basics):

    # Class adds location attribute for those that need it
    def __init__(self, location):

        DAO_Basics.__init__(self)
        self.location = location


class DAO_GIS(DAO_Location):

    # Data access class for executing spatial queries, inherits from DAO_Location

    def __init__(self, location):

        # Call superclass constructor to set up DB connection
        DAO_Location.__init__(self, location)

    def flower_beds(self, plant, n):

        # Gets the n closest flower beds to location which contain plant (optional), sorted by distance from location
        # Arguments:
        # n - the number of points of interest to be returned (0 returns all)
        # Returns - a list of GeoNode objects representing flower beds

        cursor = self.connection.cursor()

        # If plant has been passed, looking for n nearest containing plant.  If not, just n nearest.
        if plant:

            sql = 'SELECT pb.bed_id, ST_Distance(' + self.location.point_string() + ', fb.polygon) AS dist, ' \
                  'ST_AsText(ST_Centroid(fb.polygon)) ' \
                  'FROM plant_bed pb ' \
                  'JOIN flower_bed fb ' \
                  'ON pb.bed_id = fb.id ' \
                  'WHERE pb.plant_id =' + str(plant) + ' ' \
                  'ORDER BY dist'
        else:

            sql = 'SELECT id, ST_Distance(' + self.location.point_string() + ', polygon) AS dist, ' \
                  'ST_AsText(ST_Centroid(polygon)) ' \
                  'FROM flower_bed ' \
                  'ORDER BY dist'


        # Limit query to n rows if required
        if n != '0':
            sql += ' LIMIT '
            sql += n

        sql += ';'

        cursor.execute(sql)

        flower_beds = []

        # Copy flower bed to ProjNode object and append to list
        # Projected node because result of geometric calculation
        for row in cursor:

            bed = ProjNode.from_db_string(row[2])
            bed.id = row[0]
            bed.name = 'Flower Bed ' + str(bed.id)

            # Will end up back with user, so convert to lat and long
            flower_beds.append(bed.convert())

        cursor.close()

        return flower_beds

    def places(self, n):

        # Gets the n closest places to location, sorted by distance from location
        # Arguments:
        # n - the number of places to be returned (0 returns all)
        # Returns - a list of Place objects representing places

        cursor = self.connection.cursor()

        sql = 'SELECT id, ST_AsText(coordinates), name, description, ' \
              'ST_Distance(' + self.location.point_string() + ', proj_coord) ' \
              'AS dist ' \
              'FROM place ' \
              'ORDER BY dist'

        # Limit query to n rows if required
        if n != '0':
            sql += ' LIMIT '
            sql += n

        sql += ';'

        cursor.execute(sql)

        places = []

        # Copy places to Place object and append to list
        for row in cursor:

            place = Place.from_db_string(row[1])
            place.id = row[0]
            place.name = row[2]
            place.description = row[3]

            places.append(place)

        cursor.close()

        return places


class DAO_PlantLists(DAO_Basics):

    # Data access class for simple plant queries, inherits from DAO_Basics

    def __init__(self):

        # Call superclass constructor to set up DB connection

        DAO_Basics.__init__(self)

    def seasonal_plants(self, month, n):

        # Gets the first n plants of seasonal interest in given month
        # Arguments:
        # n - the number of plants to be returned (0 returns all)
        # month - an integer month when 1=January
        # Returns - a list of populated Plant objects

        cursor = self.connection.cursor()

        sql = 'SELECT plant_id ' \
              'FROM plant_month ' \
              'WHERE month_id = ' + str(month)

        # Limit query to n rows if required
        if n != '0':
            sql += ' LIMIT '
            sql += n

        sql += ';'

        cursor.execute(sql)

        # Need Plant DAO to get plant attributes
        plant_db = DAO_Plants()
        plants = []

        for row in cursor:

            plants.append(plant_db.plant_attributes(row[0]))

        cursor.close()

        return plants

    def bed_plants(self, id, n):

        # Gets the first n plants in bed with bed_id=id
        # Arguments:
        # n - the number of plants to be returned (0 returns all)
        # id - the id of the flower bed
        # Returns - a list of populated Plant objects

        cursor = self.connection.cursor()

        sql = 'SELECT plant_id ' \
              'FROM plant_bed ' \
              'WHERE bed_id = ' + str(id)

        # Limit query to n rows if required
        if n != '0':
            sql += ' LIMIT '
            sql += n

        sql += ';'

        cursor.execute(sql)

        # Need Plant DAO to get plant attributes
        plant_db = DAO_Plants()
        plants = []

        for row in cursor:

            plants.append(plant_db.plant_attributes(row[0]))

        cursor.close()

        return plants


class DAO_Route(DAO_Location):

    # Data access class for executing routing queries, inherits from DAO_Location

    def __init__(self, location):

        # Call superclass constructor to set up DB connection

        DAO_Location.__init__(self, location)

    def setup_graph(self):

        import networkx as nx

        # Populates a NetworkX Graph object using the edge database table
        # Arguments:
        # Returns - a NetworkX Graph object populated with nodes and edges

        cursor = self.connection.cursor()

        query = 'SELECT node1, node2, weight ' \
                'FROM edge'

        cursor.execute(query)

        G = nx.Graph()

        for node1, node2, weight in cursor:
            G.add_edge(node1, node2, weight=weight)

        cursor.close()

        return G

    def nearest_node_id(self):

        # Finds the node nearest to location
        # Arguments:
        # Returns - the id of the closest node to location

        sql = 'SELECT id, ST_Distance(' + self.location.point_string() + ', proj_coord) ' \
              'AS dist ' \
              'FROM node ' \
              'ORDER BY dist ' \
              'LIMIT 1;'

        row = self._execute_query(sql)

        return row[0]

    def place_nearest_node_id(self, place_id):

        # Finds the id of the closest node to place_id
        # Arguments:
        # place_id - the id of the place
        # Returns:
        # The id of the closest node to the given place

        sql = 'SELECT nearest_node ' \
              'FROM place ' \
              'WHERE id =' + str(place_id) + ';'

        row = self._execute_query(sql)

        return row[0]

    def bed_nearest_node_id(self, bed_id):

        # Finds the id of the closest node to bed_id
        # Arguments:
        # bed_id - the id of the flower bed
        # Returns:
        # The id of the closest node to the given flower bed

        sql = 'SELECT nearest_node ' \
              'FROM flower_bed ' \
              'WHERE id =' + str(bed_id) + ';'

        row = self._execute_query(sql)

        return row[0]

    def bed_centre(self, bed_id):

        # Gets the mathematical centroid of the flower bed with id = bed_id
        # Arguments:
        # bed_id - id of the flower bed in question
        # Returns - a GeoNode object representing the centroid of the flower bed polygon

        sql = 'SELECT ST_AsText(ST_Centroid(polygon)) ' \
              'FROM flower_bed ' \
              'WHERE id = ' + str(bed_id)

        row = self._execute_query(sql)

        bed_centre = ProjNode.from_db_string(row[0])

        bed_centre.id = bed_id
        bed_centre.name = 'Centre bed ' + str(bed_id)

        # Convert projected coordinates to lat and long and return
        return bed_centre.convert()

    def node_details(self, node_id):

        # Gets full details from node table for id = node_id
        # Arguments:
        # node_id - a node id
        # Returns - a GeoNode object populated with full node details

        sql = 'SELECT id, ST_AsText(coordinates), name ' \
              'FROM node ' \
              'WHERE id = ' + str(node_id)

        row = self._execute_query(sql)

        return GeoNode.from_db_row(row)

    def place_details(self, place_id):

        # Gets full details from place table for id = place_id
        # Arguments:
        # place_id - a place id
        # Returns - a Place object populated with full place details

        sql = 'SELECT name, ST_AsText(coordinates), description ' \
              'FROM place ' \
              'WHERE id = ' + str(place_id)

        row = self._execute_query(sql)

        place = Place.from_db_string(row[1])

        place.id = place_id
        place.name = row[0]
        place.description = row[2]

        return place

    def directions(self, node1, node2):

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

        row = self._execute_query(sql)

        return Stage(self.node_details(node1), self.node_details(node2), row[1], row[0])
