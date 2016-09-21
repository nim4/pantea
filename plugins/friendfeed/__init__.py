from lib.util import get_info_by_url, insert_to_db
import urllib

__host = "friendfeed.com"
__sess = "U="


def parse(headers):
    (name, img) = get_info_by_url(
    "http://friendfeed.com/", headers,
    [('"friends":"', '"'), ('class="l_profile"><img src="', '"')])
    if name is None or img is None:
        return False
    img = "http://friendfeed.com" + img
    img_path = "temp/FF_" + name.replace(" ", "_") + ".jpg"
    open(img_path, 'wb').write(urllib.urlopen(img).read())
    insert_to_db("Friendfeed", headers, name, "http://friendfeed.com/",
    img_path)
    return True
