import wisley.data_access as db
from wisley.models import Node
from wisley.models import Plant

import pytest
import lxml.etree as etree

@pytest.fixture()
def node1():
    return Node(0, '-0.84571884220576', '51.2945043901003', '')


@pytest.fixture()
def point1():
    return 'POINT(-0.84571884220576 51.2945043901003)'


@pytest.fixture()
def plant1():

    plant = Plant()

    plant.name_num = '76294'
    plant.pic = 'http://vsorchard/PlantFinderPlus_Test/PlantEntityImages/WSY0035651_4061.jpg'
    plant.height = '0.5-1 metres'
    plant.hardiness = 'H6 (hardy - very cold winter)'
    plant.common_name = 'greater quaking grass'
    plant.spread = '0.1-0.5 metres'
    plant.time_to_full_height = '1-2 years'
    plant.accepted_botanical_name = '&lt;em&gt;Briza&lt;/em&gt; &lt;em&gt;maxima&lt;/em&gt;'
    plant.description = '&lt;em&gt;B. maxima&lt;/em&gt; is an erect annual grass to 60cm, forming a ' \
                                       'tuft of flat, linear leaves, with panicles of large, flat, ovate, pale yellow' \
                                       ' spikelets which dangle from slender branches'
    plant.soil_type = 'Loam, Chalk, Sand or Clay'
    plant.foliage = 'Deciduous'
    plant.uses = 'City/Courtyard Gardens, Cottage/Informal Garden, Flower borders and beds, ' \
                                        'Cut Flowers or Low Maintenance'
    plant.aspect = 'South-facing, North-facing, West-facing or East-facing'
    plant.flower_colour = 'Pale Yellow in Summer'
    plant.moisture = 'Well-drained or Moist but well-drained'
    plant.ph = 'Acid, Alkaline or Neutral'
    plant.disease_resistance = 'Generally disease free'
    plant.sunlight = 'Full Sun'
    plant.exposure = 'Exposed or Sheltered'
    plant.cultivation = 'Easy to grow in most well-drained fertile soils in a sunny position'
    plant.low_maintenance = 'False'

    return plant


@pytest.fixture()
def elem1():

    elem = etree.Element(_tag='EntityDetailItems')

    elem.attrib['Name_Num'] = '76294'
    elem.attrib['PlantImagePath'] = 'http://vsorchard/PlantFinderPlus_Test/PlantEntityImages/WSY0035651_4061.jpg'
    elem.attrib['Height'] = '0.5-1 metres'
    elem.attrib['Hardiness'] = 'H6 (hardy - very cold winter)'
    elem.attrib['PreferredCommonName'] = 'greater quaking grass'
    elem.attrib['Spread'] = '0.1-0.5 metres'
    elem.attrib['TimeToFullHeight'] = '1-2 years'
    elem.attrib['AcceptedBotanicalName'] = '&lt;em&gt;Briza&lt;/em&gt; &lt;em&gt;maxima&lt;/em&gt;'
    elem.attrib['EntityDescription'] = '&lt;em&gt;B. maxima&lt;/em&gt; is an erect annual grass to 60cm, forming a ' \
                                       'tuft of flat, linear leaves, with panicles of large, flat, ovate, pale yellow' \
                                       ' spikelets which dangle from slender branches'
    elem.attrib['SoilType'] = 'Loam, Chalk, Sand or Clay'
    elem.attrib['Foliage'] = 'Deciduous'
    elem.attrib['SuggestedPlantUses'] = 'City/Courtyard Gardens, Cottage/Informal Garden, Flower borders and beds, ' \
                                        'Cut Flowers or Low Maintenance'
    elem.attrib['Aspect'] = 'South-facing, North-facing, West-facing or East-facing'
    elem.attrib['Flower'] = 'Pale Yellow in Summer'
    elem.attrib['Moisture'] = 'Well-drained or Moist but well-drained'
    elem.attrib['PH']= 'Acid, Alkaline or Neutral'
    elem.attrib['DiseaseResistance'] = 'Generally disease free'
    elem.attrib['Sunlight'] = 'Full Sun'
    elem.attrib['Exposure'] = 'Exposed or Sheltered'
    elem.attrib['Cultivation'] = 'Easy to grow in most well-drained fertile soils in a sunny position'
    elem.attrib['LowMaintenance'] = 'False'

    return elem


def assert_node(node1, node2):

    assert type(node1) == type(node2)
    assert node1.id == node2.id
    assert node1.lat == node2.lat
    assert node1.long == node2.long
    assert node1.name == node2.name

    return


def assert_plant(plant1, plant2):

    assert type(plant1) == type(plant2)
    assert plant1.name_num == plant2.name_num
    assert plant1.common_name == plant2.common_name
    assert plant1.pic == plant2.pic
    assert plant1.height == plant2.height
    assert plant1.spread == plant2.spread
    assert plant1.time_to_full_height == plant2.time_to_full_height
    assert plant1.hardiness == plant2.hardiness
    assert plant1.accepted_botanical_name == plant2.accepted_botanical_name
    assert plant1.description == plant2.description
    assert plant1.soil_type == plant2.soil_type
    assert plant1.foliage == plant2.foliage
    assert plant1.uses == plant2.uses
    assert plant1.aspect == plant2.aspect
    assert plant1.flower_colour == plant2.flower_colour
    assert plant1.moisture == plant2.moisture
    assert plant1.ph == plant2.ph
    assert plant1.disease_resistance == plant2.disease_resistance
    assert plant1.sunlight == plant2.sunlight
    assert plant1.exposure == plant2.exposure
    assert plant1.cultivation == plant2.cultivation
    assert plant1.low_maintenance == plant2.low_maintenance

    return


@pytest.mark.parametrize("pcn_input, exp_name_num", [
    ('white bachelor\'s buttons', '97224'),
    ('cranesbill \'Czakor\'', '97811'),
    ('greater quaking grass', '76294'),
    ('not a real plant', '')
])


def test_get_plant_name_num(pcn_input, exp_name_num):

    # Tests data access layer method get_plant_name_num
    # This test uses the real xml file

    act_plant_name_num = db.get_plant_name_num(pcn_input)

    assert act_plant_name_num == exp_name_num

    return
