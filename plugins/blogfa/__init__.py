from lib.util import get_info_by_url, insert_to_db

__host = "blogfa.com"
__sess = ".ABF="


def parse(headers):
    name = get_info_by_url("http://www.blogfa.com/Desktop/", headers,
    [('.blogfa.com" target="_blank">', '<')])[0]
    if name is None:
        return False
    insert_to_db("Blogfa", headers, name, "http://www.blogfa.com/Desktop/")
    return True
