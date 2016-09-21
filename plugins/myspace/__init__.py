from lib.util import get_info_by_url, insert_to_db
import urllib

__host = "myspace.com"
__sess = "USER="


def parse(headers):
    (name, img) = get_info_by_url(
    "http://www.myspace.com/home", headers,
    [('"displayName":"\\"', '\\"'), (',"imageUrl":"', '"')])
    if name is None or img is None:
        return False
    img_path = "temp/MyS_" + name.replace(" ", "_") + ".jpg"
    open(img_path, 'wb').write(urllib.urlopen(img).read())
    insert_to_db("MySpace", headers, name, "http://www.myspace.com/",
    img_path)
    return True
