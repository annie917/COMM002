import wisley.data_access as db
from wisley.models import Node
import pytest

@pytest.fixture()
def node1():
    return Node(0, '-0.84571884220576', '51.2945043901003', '')


@pytest.fixture()
def point1():
    return 'POINT(-0.84571884220576 51.2945043901003)'


def assert_node(node1, node2):

    assert type(node1) == type(node2)
    assert node1.id == node2.id
    assert node1.lat == node2.lat
    assert node1.long == node2.long
    assert node1.name == node2.name

    return


def test__point_to_node(node1, point1):

    act_ret_val = db._point_to_node(point1)

    assert_node(node1, act_ret_val)

    return


def test__node_to_point(node1, point1):

    exp_ret_val = 'ST_PointFromText(\'' + point1 + '\')'

    act_ret_val = db._node_to_point(node1)

    assert act_ret_val == exp_ret_val

    return



