from lib.util import get_info_by_url, insert_to_db
import urllib

__host = "youtube.com"
__sess = "HSID="


def parse(headers):
    (name, img) = get_info_by_url(
    'http://www.youtube.com/dashboard', headers,
    [(' class="email-only">\n      <p>', '<'),
    ('<img alt="Thumbnail" src="', '"')])
    if name is None or img is None:
        return False
    img_path = "temp/YT_" + name.replace(" ", "_") + ".jpg"
    try:
        open(img_path, 'wb').write(urllib.urlopen(img).read())
    except:
        return False
    insert_to_db("YouTube", headers, name, "http://www.youtube.com/",
    img_path)
    return True
