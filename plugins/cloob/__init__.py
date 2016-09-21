from lib.util import get_info_by_cookie, insert_to_db

__host = "cloob.com"
__sess = "s_id="


def parse(headers):
    name = str(get_info_by_cookie(["s_id"], headers)[0]).split("|")[0]
    if name is None:
        return False
    insert_to_db("Cloob", headers, name, "http://www.cloob.com/")
    return True
