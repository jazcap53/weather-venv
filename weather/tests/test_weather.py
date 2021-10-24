import pytest

from weather import __version__
from weather.weather import get_response_dict


def test_version():
    assert __version__ == '0.1.0'


@pytest.mark.parametrize('response', [{}, [], '', 0, None])
def test_get_response_dict_raises(response):
    """get_response_dict should raise ValueError on null input"""
    with pytest.raises(ValueError):
        _ = get_response_dict(response)
