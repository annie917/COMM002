class Plant(object):

    def __init__(self):

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


class Node(object):

    # Represents a row in the node table.  Lat and long are stored as a POINT in db, but must be retrieved as strings
    # As the client will ultimately want them as strings, they are stored here as strings

    def __init__(self, id, long, lat, name):

        self.id = id # int
        self.long = long # string
        self.lat = lat # string
        self.name = name # string


class PointOfInterest(Node):

    def __init__(self, id, lat, long, name, nearest_node):

        Node.__init__(self, id, lat, long, name)

        self.nearest_node = nearest_node


class Route(object):

    def __init__(self):

        self.length = 0.0
        self.nodes = []
        self.destination = Node(0, '0.0', '0.0', '')
