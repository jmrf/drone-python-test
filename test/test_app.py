import pytest
from demo_app.app import func

@pytest.mark.parametrize('tup', [(1, 2, 3), (3, 4, 7), (5, 6, 11)])
def test_app(tup):
    a, b, r = tup
    assert func(a, b) == r


