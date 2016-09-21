from lib.util import get_info_by_url, insert_to_db

__host = "stackoverflow.com"
__sess = "__qca="


def parse(headers):
    name = get_info_by_url("http://www.stackoverflow.com/",
    headers, [('class="profile-link">', "<")])[0]
    if name is None:
        return False
    insert_to_db("Stackoverflow", headers, name,
    "http://www.stackoverflow.com/")
    return True
