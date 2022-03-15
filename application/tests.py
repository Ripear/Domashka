from utils import format_url
from utils import counter


def test_format_url():
    url = "http://google.com"
    assert format_url(url) == "http://google.com"

def test_counter():
    url1 = "http://google.com"
    url2 = "http://yandex.ru"
    assert counter(url1) is not None and counter(url1) is not counter(url2)
