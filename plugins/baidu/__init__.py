from lib.util import get_info_by_url, insert_to_db

__host = "baidu.com"
__sess = "BDUSS="


def parse(headers):
    name = get_info_by_url("http://www.baidu.com/", headers,
    [('"username":"', '"')])[0]
    if name is None:
        return False
    insert_to_db("Baidu", headers, name, "http://www.baidu.com/")
    return True
