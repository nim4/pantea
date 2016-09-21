from lib.util import get_info_by_url, insert_to_db

__host = "facenama.com"
__sess = "fcccdfacenamacom="


def parse(headers):
    name = get_info_by_url("http://facenama.com/settings/profile",
    headers, [(' name="name"  value="', '"')])[0]
    if name is None:
        return False
    insert_to_db("Facenama", headers, name, "http://www.facenama.com/")
    return True
