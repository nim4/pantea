from lib.util import get_info_by_url, insert_to_db
import urllib
import json

__host = "vk.com"
__sess = "remixsid="


def parse(headers):
    vkid = get_info_by_url(
    'http://vk.com/feed', headers,
    [('"id":', ',')])[0]
    if vkid is None:
        return False
    img_path = "temp/VK_" + vkid + ".jpg"
    try:
        info = urllib.urlopen(
        'http://api.vkontakte.ru/method/getProfiles?fields=photo&uid=' +
        vkid).read()
        data = json.loads(info)
        img = urllib.urlopen(data["response"][0]["photo"]).read()
        open(img_path, 'wb').write(img)
        name = data["response"][0]["first_name"] + " " + \
        data["response"][0]["last_name"]
    except:
        return False
    insert_to_db("VKontakte", headers, name, "http://vk.com/",
    img_path)
    return True
