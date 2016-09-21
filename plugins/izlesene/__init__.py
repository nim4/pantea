from lib.util import get_info_by_url, insert_to_db
import urllib

__host = "izlesene.com"
__sess = "PHPSESSID="


def parse(headers):
    (name, img) = get_info_by_url(
    "http://www.izlesene.com/ajax/ajaxCommon/getNewUserBox",
    headers, [('width="16" height="16">', "\n"), ('<img src="', '"')])
    if name is None:
        return False
    img_path = "temp/IZ_" + name.replace(" ", "_") + ".jpg"
    open(img_path, 'wb').write(urllib.urlopen(img).read())
    insert_to_db("Izlesene", headers, name, "http://www.izlesene.com/",
    img_path)
    return True
