from lib.util import get_info_by_url, insert_to_db

__host = "bing.com"
__sess = "KievRPSAuth="


def parse(headers):
    name = get_info_by_url("http://www.bing.com/", headers,
    [('<span id="id_n">', '<')])[0]
    if name is None:
        return False
    insert_to_db("Bing", headers, name, "http://www.bing.com")
    return True
