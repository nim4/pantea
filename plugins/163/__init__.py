from lib.util import get_info_by_cookie, insert_to_db

__host = "163.com"
__sess = "S_INFO="


def parse(headers):
    name = str(get_info_by_cookie(["S_INFO"], headers)[0]).split("|")[-1]
    if name is None:
        return False
    insert_to_db("163", headers, name, "http://www.163.com/")
    return True
