from lib.util import get_info_by_url, insert_to_db

__host = "dailymail.co.uk"
__sess = "authid="


def parse(headers):
    name = get_info_by_url(
    "http://www.dailymail.co.uk/registration/profile.html", headers,
    [('<strong class="homeblue">', '<')])[0]
    if name is None:
        return False
    insert_to_db("Dailymail", headers, name,
    "http://www.dailymail.co.uk/home/index.html")
    return True
