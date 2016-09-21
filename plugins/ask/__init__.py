from lib.util import get_info_by_cookie, insert_to_db

__host = "ask.com"
__sess = "cp="


def parse(headers):
    tmp = get_info_by_cookie(["cp"], headers)[0]
    if tmp is None:
        return False
    cont = tmp.split("|")
    if len(cont) != 10:
        return False
    name = cont[-2]
    insert_to_db("Ask", headers, name, "http://www.ask.com/")
    return True
