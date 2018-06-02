class Plant(object):

    # Class for representing a plant record from XML

    def __init__(self):


        # Instantiate an empty plant object

        self.name_num = ''
        self.common_name = ''
        self.pic = ''
        self.height = ''
        self.spread = ''
        self.time_to_full_height = ''
        self.hardiness = ''
        self.accepted_botanical_name = ''
        self.description = ''
        self.soil_type = ''
        self.foliage = ''
        self.uses = ''
        self.aspect = ''
        self.flower_colour = ''
        self.moisture = ''
        self.ph = ''
        self.disease_resistance = ''
        self.sunlight = ''
        self.exposure = ''
        self.cultivation = ''
        self.low_maintenance = ''
        self.common_names = []
        self.synonyms = []


    def populate_xml(self, elem):

        # Populate properties with attributes from xml element, elem
        self.name_num = elem.attrib['Name_Num']
        self.pic = elem.attrib['PlantImagePath']
        self.height = elem.attrib['Height']
        self.hardiness = elem.attrib['Hardiness']
        self.common_name = elem.attrib['PreferredCommonName']
        self.spread = elem.attrib['Spread']
        self.time_to_full_height = elem.attrib['TimeToFullHeight']
        self.accepted_botanical_name = elem.attrib['AcceptedBotanicalName']
        self.description = elem.attrib['EntityDescription']
        self.soil_type = elem.attrib['SoilType']
        self.foliage = elem.attrib['Foliage']
        self.uses = elem.attrib['SuggestedPlantUses']
        self.aspect = elem.attrib['Aspect']
        self.flower_colour = elem.attrib['Flower']
        self.moisture = elem.attrib['Moisture']
        self.ph = elem.attrib['PH']
        self.disease_resistance = elem.attrib['DiseaseResistance']
        self.sunlight = elem.attrib['Sunlight']
        self.exposure = elem.attrib['Exposure']
        self.cultivation = elem.attrib['Cultivation']
        self.low_maintenance = elem.attrib['LowMaintenance']

        return


class Node(object):

    # Represents a row in the node table.  Lat and long are stored as a POINT in db, but must be retrieved as strings
    # As the client will ultimately want them as strings, they are stored here as strings
    # Also used to represent flower beds, with id = bed id, and lat and long being mathematical centroid of bed

    def __init__(self, id, long, lat, name):

        self.id = id # int
        self.long = long # string
        self.lat = lat # string
        self.name = name # string

    @classmethod
    def from_point_string(cls, point_string):

        # Alternative constructor - populates Node from a point string
        long_and_lat = point_string.lstrip('POINT(').rstrip(')').split(' ')

        return cls(0, long_and_lat[0], long_and_lat[1], '')

    @classmethod
    def from_db_row(cls, db_row):

        # Alternative constructor - populates Node from a database row tuple
        long_and_lat = db_row[1].lstrip('POINT(').rstrip(')').split(' ')

        return cls(db_row[0], long_and_lat[0], long_and_lat[1], db_row[2])

    def point_str(self):

        return 'ST_PointFromText(\'POINT(' + self.long + ' ' + self.lat + ')\')'


class Place(Node):

    # Extension of Node to store a place

    def __init__(self, id, lat, long, name):

        Node.__init__(self, id, lat, long, name)

        self.description = ''


class Route(object):

    # Holds all the information required to pass a route back to client.  Not directly related to a db table

    def __init__(self):

        self.length = 0.0 # Total route length in metres
        self.destination = Node(0, '0.0', '0.0', '') # Information about the destination
        self.stages = [] # List of  Stages


class Stage(object):

    # Holds information about how to navigate between two nodes

    def __init__(self, node1, node2, length, instruction):

        self.node1 = node1 # First node (Node)
        self.node2 = node2 # Second node (Node)
        self.length = length # Length of stage in metres
        self.instruction = instruction # Direction node1 --> node2 (string)
