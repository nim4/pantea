from lib.util import get_info_by_url, insert_to_db

__host = "blogger.com"
__sess = "blogger_SID="


def parse(headers):
    name = get_info_by_url("http://www.blogger.com/home", headers,
    [('{\\x221\\x22:{\\x221\\x22:\\x22', '\\x')])[0]
    if name is None:
        return False
    insert_to_db("Blogger", headers, name, "http://www.blogger.com/content.g")
    return True
