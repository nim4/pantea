from lib.util import get_info_by_url, insert_to_db

__host = "sahibinden.com"
__sess = "auction_session="


def parse(headers):
    name = get_info_by_url('http://www.sahibinden.com/xml_username.php',
    headers, [("index.php?a=1004'>", "<")])[0]
    if name is None:
        return False
    insert_to_db("Sahibinden", headers, name, "http://www.sahibinden.com/")
    return True
