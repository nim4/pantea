from lib.util import get_info_by_url, insert_to_db
import urllib

__host = "tumblr.com"
__sess = "pfp="


def parse(headers):
    (name, img) = get_info_by_url(
    'http://www.tumblr.com/dashboard', headers,
    [('data-blog-url="http://', '.tumblr.com/"'),
    ('data-user-avatar-url="', '"')])
    if name is None:
        return False
    print (name, img)
    img_path = "temp/TR_" + name.replace(" ", "_") + ".jpg"
    open(img_path, 'wb').write(urllib.urlopen(img).read())
    insert_to_db("Tumblr", headers, name, "http://www.tumblr.com/dashboard",
    img_path)
    return True
