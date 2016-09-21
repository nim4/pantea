from lib.util import get_info_by_url, insert_to_db

__host = "reddit.com"
__sess = "reddit_session="


def parse(headers):
    name = get_info_by_url("http://www.reddit.com/",
    headers, [('"logged": "', '"')])[0]
    if name is None:
        return False
    insert_to_db("Reddit", headers, name, "http://www.reddit.com/")
    return True
