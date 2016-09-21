from lib.util import get_info_by_cookie, insert_to_db

__host = "gittigidiyor.com"
__sess = "PHPSESSID="


def parse(headers):
    name = get_info_by_cookie(["signin[hp_nick]"], headers)[0]
    if name is None:
        return False
    insert_to_db("Gittigidiyor", headers, name, "http://www.gittigidiyor.com/")
    return True
