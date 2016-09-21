from lib.util import get_info_by_url, insert_to_db

__host = "yemeksepeti.com"
__sess = ".ASPXAUTH="


def parse(headers):
    name = get_info_by_url('http://' + headers["Host"] + "/",
    headers, [("function InteractiveFullName() { return '", "'")])[0]
    if name is None:
        return False
    insert_to_db("Yemeksepeti", headers, name,
    "http://" + headers["Host"] + "/")
    return True
