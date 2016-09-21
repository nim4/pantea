from lib.util import get_info_by_url, insert_to_db

__host = "flickr.com"
__sess = "cookie_session="


def parse(headers):
    name = get_info_by_url("http://www.flickr.com/", headers, [('","name":"',
    '"')])[0]
    if name is None:
        return False
    insert_to_db("Flickr", headers, name, "http://www.flickr.com/")
    return True
