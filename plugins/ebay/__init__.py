from lib.util import get_info_by_url, insert_to_db

__host = "ebay.com"
__sess = "cid="


def parse(headers):
    name = get_info_by_url(
    'http://my.ebay.com/ws/eBayISAPI.dll?MyeBay', headers,
    [('="mbg-nw">', '<')])[0]
    if name is None:
        return False
    insert_to_db("Ebay", headers, name, "http://www.ebay.com")
    return True
