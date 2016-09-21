from lib.util import get_info_by_cookie, insert_to_db

__host = "instagram.com"
__sess = "igls="


def parse(headers):
    name = get_info_by_cookie(["igls"], headers)[0]
    if name is None:
        return False
    insert_to_db("Instagram", headers, name, "http://instagram.com/")
    return True
