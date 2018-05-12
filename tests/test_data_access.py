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
    plant.accepted_botanical_name = '<em>Briza</em> <em>maxima</em>'
    plant.description = '<em>B. maxima</em> is an erect annual grass to 60cm, forming a ' \
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

    plant.common_names.append('great quaking grass')
    plant.common_names.append('pearl grass')
    plant.synonyms.append('<em>Briza</em> <em>major</em>')

    return plant


@pytest.fixture()
def plant2():

    plant = Plant()

    plant.name_num = '97224'
    plant.pic = 'http://vsorchard/PlantFinderPlus_Test/PlantEntityImages/WSY0034793_4502.jpg'
    plant.height = '0.5-1 metres'
    plant.hardiness = 'H7 (very hardy)'
    plant.common_name = 'white bachelor\'s buttons'
    plant.spread = '0.1-0.5 metres'
    plant.time_to_full_height = '2-5 years'
    plant.accepted_botanical_name = '<em>Ranunculus</em> <em>aconitifolius</em> \'Flore Pleno\' (d) AGM'
    plant.description = '\'Flore Pleno\' is a vigorous herbaceous perennial to 90cm, with palmately divided dark ' \
                        'green leaves and branched stems bearing long-lasting double, button-like white ' \
                        'flowers 2cm in width'
    plant.soil_type = 'Clay, Loam or Chalk'
    plant.foliage = 'Deciduous'
    plant.uses = 'Cottage/Informal Garden, Flower borders and beds or Cut Flowers'
    plant.aspect = 'South-facing, East-facing or West-facing'
    plant.flower_colour = 'White in Spring and  Summer'
    plant.moisture = 'Moist but well-drained'
    plant.ph = 'Acid, Alkaline or Neutral'
    plant.disease_resistance = 'May be subject to <a ' \
                                       'href=\'http://www.rhs.org.uk/advicesearch/Profile.aspx?pid=253\' >powdery ' \
                                       'mildews</a> in dry conditions'
    plant.sunlight = 'Full Sun, Partial Shade'
    plant.exposure = 'Sheltered'
    plant.cultivation = 'Grow in humus-rich, fertile, moist or moist but well-drained soil in full or partial shade'
    plant.low_maintenance = 'False'

    plant.common_names.append('fair maids of France')
    plant.common_names.append('fair maids of Kent')
    plant.synonyms.append('<em>Ranunculus</em> <em>aconitifolius</em>  <em>'
                          'flore</em>  <em>pleno</em> \'Batchelor\'s Button\'')

    return plant


@pytest.fixture()
def elem1():

    elem = etree.Element(_tag='EntityDetailsItems')

    elem.attrib['Name_Num'] = '76294'
    elem.attrib['PlantImagePath'] = 'http://vsorchard/PlantFinderPlus_Test/PlantEntityImages/WSY0035651_4061.jpg'
    elem.attrib['Height'] = '0.5-1 metres'
    elem.attrib['Hardiness'] = 'H6 (hardy - very cold winter)'
    elem.attrib['PreferredCommonName'] = 'greater quaking grass'
    elem.attrib['Spread'] = '0.1-0.5 metres'
    elem.attrib['TimeToFullHeight'] = '1-2 years'
    elem.attrib['AcceptedBotanicalName'] = '<em>Briza</em> <em>maxima</em>'
    elem.attrib['EntityDescription'] = '<em>B. maxima</em> is an erect annual grass to 60cm, forming a ' \
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


@pytest.fixture()
def elem2():

    elem = etree.Element(_tag='EntityDetailsItems')
    elem.attrib['Name_Num'] = '97224'
    elem.attrib['PreferredCommonName'] = 'white bachelor\'s buttons'
    elem.attrib['PlantImagePath'] = 'http://vsorchard/PlantFinderPlus_Test/PlantEntityImages/WSY0034793_4502.jpg'
    elem.attrib['Height'] = '0.5-1 metres'
    elem.attrib['Hardiness'] = 'H7 (very hardy)'
    elem.attrib['Spread'] = '0.1-0.5 metres'
    elem.attrib['TimeToFullHeight'] = '2-5 years'
    elem.attrib['AcceptedBotanicalName'] = '<em>Ranunculus</em> <em>aconitifolius</em> \'Flore Pleno\' (d) AGM'
    elem.attrib['EntityDescription'] = '\'Flore Pleno\' is a vigorous herbaceous perennial to 90cm, with palmately ' \
                                       'divided dark green leaves and branched stems bearing long-lasting double, ' \
                                       'button-like white flowers 2cm in width'
    elem.attrib['SoilType'] = 'Clay, Loam or Chalk'
    elem.attrib['Foliage'] = 'Deciduous'
    elem.attrib['SuggestedPlantUses'] = 'Cottage/Informal Garden, Flower borders and beds or Cut Flowers'
    elem.attrib['Aspect'] = 'South-facing, East-facing or West-facing'
    elem.attrib['Flower'] = 'White in Spring and  Summer'
    elem.attrib['Moisture'] = 'Moist but well-drained'
    elem.attrib['PH'] = 'Acid, Alkaline or Neutral'
    elem.attrib['DiseaseResistance'] = 'May be subject to <a ' \
                                       'href=\'http://www.rhs.org.uk/advicesearch/Profile.aspx?pid=253\' >powdery ' \
                                       'mildews</a> in dry conditions'
    elem.attrib['Sunlight'] = 'Full Sun, Partial Shade'
    elem.attrib['Exposure'] = 'Sheltered'
    elem.attrib['Cultivation'] = 'Grow in humus-rich, fertile, moist or moist but well-drained soil in full or ' \
                                 'partial shade'
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

    assert len(plant1.common_names) == len(plant2.common_names)

    for i in range(len(plant1.common_names)):
        assert plant1.common_names[i] == plant2.common_names[i]

    assert len(plant1.synonyms) == len(plant2.synonyms)

    for i in range(len(plant1.synonyms)):
        assert plant1.synonyms[i] == plant2.synonyms[i]

    return


@pytest.mark.parametrize("pcn_input, exp_name_num", [
    ('white bachelor\'s buttons', '97224'),
    ('cranesbill \'Czakor\'', '97811'),
    ('greater quaking grass', '76294'),
    ('not a real plant', ''),
    ('', '')
])


def test_get_plant_name_num(pcn_input, exp_name_num):

    # Tests data access layer method get_plant_name_num
    # This test uses the real xml file

    act_plant_name_num = db.get_plant_name_num(pcn_input)

    assert act_plant_name_num == exp_name_num

    return


def test_get_plant_attributes(plant1, plant2):

    # Tests data access layer method get_plant_attributes
    # This test uses the real xml file

    act_plant = db.get_plant_attributes('greater quaking grass')

    assert_plant(act_plant, plant1)

    act_plant = db.get_plant_attributes('white bachelor\'s buttons')

    assert_plant(act_plant, plant2)

    act_plant = db.get_plant_attributes('not a real plant')

    assert_plant(act_plant, Plant())

    return