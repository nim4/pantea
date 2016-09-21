from lib.util import get_info_by_url, insert_to_db
import json

__host = "fizy.com"
__sess = "fizyuser="


def parse(headers):
    info = get_info_by_url("http://fizy.com/userdata", headers)[0]
    try:
        name = json.loads(info)["username"]
    except:
        return False
    insert_to_db("Fizy", headers, name, "http://fizy.com/")
    return True
