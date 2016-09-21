from lib.util import get_info_by_url, insert_to_db
import urllib

__host = "persianblog.ir"
__sess = ".PBFORMSAUTH="


def parse(headers):
    (name, img) = get_info_by_url(
    'http://persianblog.ir/EditAvatar.aspx', headers,
    [('aspx" style="font-weight:bold;">', '<'),
    ('id="imgAvatarForChange" src="', '"')])
    if name is None:
        return False
    img_path = "temp/PB_" + name.replace(" ", "_") + ".jpg"
    open(img_path, 'wb').write(urllib.urlopen(img).read())
    insert_to_db("Persianblog", headers, name, "http://persianblog.ir/",
    img_path)
    return True
