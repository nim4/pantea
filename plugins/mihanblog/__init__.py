from lib.util import get_info_by_cookie, insert_to_db

__host = "mihanblog.com"
__sess = "s_id="


def parse(headers):
    tmp = get_info_by_cookie(["s_id"], headers)[0]
    name = str(tmp[:tmp.find("%7C")])
    if name is None:
        return False
    insert_to_db("Mihanblog", headers, name,
    "http://mihanblog.com/web/index/dashboard")
    return True
