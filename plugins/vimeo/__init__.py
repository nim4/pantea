from lib.util import get_info_by_url, insert_to_db

__host = "vimeo.com"
__sess = "has_logged_in=1"


def parse(headers):
    name = get_info_by_url('https://vimeo.com/home/discover',
    headers, [('"display_name":"', '"')])[0]
    if name is None:
        return False
    insert_to_db("Vimeo", headers, name, 'https://vimeo.com/')
    return True
