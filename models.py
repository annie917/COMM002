class Plant(object):

    def __init__(self, plant_name):

        self.name_num = ''
        self.common_name = plant_name
        self.pic = ''
        self.height = ''
        self.hardiness = ''

    def populate_xml(self):

        from lxml import etree

        for event, elem in etree.iterparse('../plantselector.xml', events=("start", "end")):
            if event == "start":
                if elem.tag == 'EntityDetailsItems':
                    if elem.attrib['PreferredCommonName'] == self.common_name:
                        self.name_num = elem.attrib['Name_Num']
                        self.pic = elem.attrib['PlantImagePath']
                        self.height = elem.attrib['Height']
                        self.hardiness = elem.attrib['Hardiness']
                        break

            elem.clear()

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