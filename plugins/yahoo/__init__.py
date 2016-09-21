from lib.util import get_info_by_url, insert_to_db

__host = "yahoo.com"
__sess = "Y=v="


def parse(headers):
    name = get_info_by_url("http://my.yahoo.com/",
    headers, [('<span class="yuhead-yid">', "<")])[0]
    if name is None:
        return False
    insert_to_db("Yahoo", headers, name, "http://my.yahoo.com/")
    return True
