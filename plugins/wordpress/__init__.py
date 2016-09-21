from lib.util import get_info_by_url, insert_to_db
import urllib

__host = "wordpress.com"
__sess = "wordpress_logged_in="


def parse(headers):
    (name, img) = get_info_by_url(
    'http://wordpress.com/#!/read/following/', headers,
    [('"user_login":"', '"'), ('{"avatar":"<img alt=\'\' src=\'', "'")])
    if name is None:
        return False
    img = img.replace("\\/", "/").replace("&amp;", "&").replace("s=96", "s=64")
    img_path = "temp/WP_" + name.replace(" ", "_") + ".jpg"
    open(img_path, 'wb').write(urllib.urlopen(img).read())
    insert_to_db("Wordpress", headers, name, "http://www.wordpress.com",
    img_path)
    return True
