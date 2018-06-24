class Node(object):

    # Base Node class for GeoNode and ProjNode.  Abstract.
    def __init__(self, id, name):

        self.id = id  # int
        self.name = name  # string

        return


class GeoNode(Node):

    # Sub class for storing nodes in geographic coordinate systems - lat, long
    def __init__(self, id, name, long, lat):

        Node.__init__(self, id, name)
        self.long = long  #String
        self.lat = lat   #String

    @classmethod
    # Alternative constructor - populates GeoNode from MySQL POINT string
    def from_db_string(cls, db_string):

        long_and_lat = db_string.lstrip('POINT(').rstrip(')').split(' ')

        return cls(0, '', long_and_lat[0], long_and_lat[1])

    @classmethod
    def from_db_row(cls, db_row):

        # Alternative constructor - populates Node from a database row tuple
        long_and_lat = db_row[1].lstrip('POINT(').rstrip(')').split(' ')

        return cls(db_row[0], db_row[2], long_and_lat[0], long_and_lat[1])

    def point_string(self):
        # Returns node in format for putting into db as POINT, with srid=4326 (GPS)
        return 'ST_PointFromText(\'POINT(' + self.long + ' ' + self.lat + ')\', 4326)'

    def convert(self):

        # Produces a projected node object from this object
        from pyproj import Proj, transform
        import configparser

        config = configparser.ConfigParser()
        config.read('config.ini')
        geo_string = config['Projections']['geographic']
        proj_string = config['Projections']['projected']

        p1 = Proj(geo_string)
        p2 = Proj(proj_string)

        x, y = transform(p1, p2, float(self.long), float(self.lat))

        return ProjNode(self.id, self.name, x, y)


class ProjNode(Node):

    # Sub class for storing node in projected coordinate system
    def __init__(self, id, name, x, y):

        Node.__init__(self, id, name)
        self.x = x   #float
        self.y = y   #float

    @classmethod
    # Alternative constructor - populates ProjNode from MySQL POINT string
    def from_db_string(cls, db_string):
        x_and_y = db_string.lstrip('POINT(').rstrip(')').split(' ')

        return cls(0, '', float(x_and_y[0]), float(x_and_y[1]))

    @classmethod
    def from_db_row(cls, db_row):

        # Alternative constructor - populates Node from a database row tuple
        x_and_y = db_row[1].lstrip('POINT(').rstrip(')').split(' ')

        return cls(db_row[0], db_row[2], float(x_and_y[0]), float(x_and_y[1]))

    def point_string(self):

        # Returns node in format for putting into db as POINT, with srid=0 (cartesian)
        return 'ST_PointFromText(\'POINT(' + str(self.x) + ' ' + str(self.y) + ')\')'

    def convert(self):

        # Produces a node object with geographic coordinates (lat/long)
        # Should only be done to convert the result of a geometric calculation as accuracy will be lost
        from pyproj import Proj, transform
        import configparser

        config = configparser.ConfigParser()
        config.read('config.ini')
        geo_string = config['Projections']['geographic']
        proj_string = config['Projections']['projected']

        p1 = Proj(proj_string)
        p2 = Proj(geo_string)

        long, lat = transform(p1, p2, self.x, self.y)

        return GeoNode(self.id, self.name, str(long), str(lat))


class Place(GeoNode):

    # Extension of GeoNode to store a place

    def __init__(self, id, lat, long, name):

        GeoNode.__init__(self, id, lat, long, name)

        self.description = ''


class Route(object):

    # Holds all the information required to pass a route back to client.  Not directly related to a db table

    def __init__(self):

        self.length = 0.0 # Total route length in metres
        self.destination = GeoNode(0, '', '0.0', '0.0') # Information about the destination
        self.stages = [] # List of  Stages


class Stage(object):

    # Holds information about how to navigate between two nodes

    def __init__(self, node1, node2, length, instruction):

        self.node1 = node1 # First node (Node)
        self.node2 = node2 # Second node (Node)
        self.length = length # Length of stage in metres
        self.instruction = instruction # Direction node1 --> node2 (string)


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
