from lib.util import get_info_by_cookie, insert_to_db
import json
import urllib

__host = ".qq.com"
__sess = "skey="


def parse(headers):
    (o_cookie, skey) = get_info_by_cookie(["o_cookie", "skey"], headers)
    if o_cookie is None or skey is None:
        return False
    info = urllib.urlopen("http://qfwd.qq.com/?uin=" + o_cookie +
    "&skey=" + skey + "&func=loginAll").read()[9:-2]
    try:
        data = json.loads(info)
        name = data['nick']
        img_path = "temp/" + o_cookie + ".jpg"
        img = urllib.urlopen(data["Face"]).read()
        open(img_path, 'wb').write(img)
    except:
        return False
    insert_to_db("QQ", headers, name, "http://www.qq.com/", img_path)
    return True
