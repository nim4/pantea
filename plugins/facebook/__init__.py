import urllib
from lib.util import get_info_by_cookie, insert_to_db
import json

__host = ".facebook.com"
__sess = "c_user="


def parse(headers):
    c_user = get_info_by_cookie(["c_user"], headers)[0]
    if c_user is None or c_user == "":
        return False
    try:
        info = urllib.urlopen('http://graph.facebook.com/' + c_user).read()
        img = urllib.urlopen('http://graph.facebook.com/' + c_user +
        '/picture').read()
        j = json.loads(info)
        name = j["name"]
        open("temp/FB_" + c_user + ".jpg", 'wb').write(img)
    except:
        return False
    if name == "":
        return False
    insert_to_db("Facebook", headers, name, "http://www.facebook.com",
    "temp/FB_" + c_user + ".jpg")
    return True
