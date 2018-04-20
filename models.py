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

    def __init__(self, id, lat, long, name):

        self.id = id
        self.lat = lat
        self.long = long
        self.name = name


class PointOfInterest(Node):

    def __init__(self, id, lat, long, name, nearest_node):

        Node.__init__(self, id, lat, long, name)

        self.nearest_node = nearest_node