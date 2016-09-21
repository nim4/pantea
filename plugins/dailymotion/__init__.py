import urllib
from lib.util import get_info_by_url, insert_to_db

__host = "dailymotion.com"
__sess = "login_infos="


def parse(headers):
    (name, img) = get_info_by_url(
    'http://www.dailymotion.com/profile', headers,
    [('<a class="image_border" title="', '"'), ('<img src="', '"')])
    if name is None:
        return False
    img_path = "temp/DM_" + name.replace(" ", "_") + ".jpg"
    open(img_path, 'wb').write(urllib.urlopen(img).read())
    insert_to_db("Dailymotion", headers, name,
    "http://www.dailymotion.com/", img_path)
    return True
