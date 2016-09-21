from lib.util import get_info_by_url, insert_to_db

__host = "pinterest.com"
__sess = "_pinterest_sess="


def parse(headers):
    name = get_info_by_url('http://pinterest.com/',
    headers, [('" alt="img" />', "<")])[0]
    if name is None:
        return False
    insert_to_db("Pinterest", headers, name, 'http://pinterest.com/')
    return True
