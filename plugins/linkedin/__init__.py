from lib.util import get_info_by_url, insert_to_db
import urllib

__host = "linkedin.com"
__sess = "leo_auth_token="


def parse(headers):
    (name, img) = get_info_by_url(
    "http://www.linkedin.com/", headers,
    [('alt="', '"'), (' <img class="member-photo" src="', '"')])
    if name is None or img is None:
        return False
    img_path = "temp/LI_" + name.replace(" ", "_") + ".jpg"
    open(img_path, 'wb').write(urllib.urlopen(img).read())
    insert_to_db("LinkedIn", headers, name, "http://www.linkedin.com/",
    img_path)
    return True
