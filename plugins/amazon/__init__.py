from lib.util import get_info_by_url, insert_to_db

__host = ".amazon."
__sess = "x-main="


def parse(headers):
    name = get_info_by_url('http://' + headers["Host"] + '/gp/history/',
    headers, [("id='nav-signin-text' class='nav-button-em'>", "<")])[0]
    if name is None:
        return False
    insert_to_db("Amazon", headers, name, "http://" + headers["Host"] + "/")
    return True
