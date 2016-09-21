from lib.util import get_info_by_url, insert_to_db

__host = "yandex."
__sess = "Session_id="


def parse(headers):
    name = get_info_by_url("http://" + headers["Host"] + "/",
    headers, [('<i class="b-user__provider-ico"></i>', "<")])[0]
    if name is None:
        return False
    insert_to_db("Yandex", headers, name, "http://" + headers["Host"] + "/")
    return True
