import urllib2
from sqlite3 import IntegrityError

def get_info_by_url(url, headers, limits=[None]):
    ret = []
    try:
        opener = urllib2.build_opener(urllib2.HTTPHandler())
        headers["Accept-Encoding"] = "text"
        headers["X-Anti-Pantea"] = "On"
        opener.addheaders = headers.items()
        content = opener.open(url).read()
    except:
        for x in limits:
            ret.append(None)
        return ret
    if limits != [None]:
        for l in limits:
            pos = content.find(l[0])
            if pos == -1:
                ret.append(None)
                continue
            tmp = content[pos + len(l[0]):]
            ret.append(tmp[:tmp.find(l[1])])
    else:
        ret.append(content)
    return ret


def get_info_by_cookie(names, headers):
    ret = []
    cook = headers["Cookie"]
    for s in names:
        s += "="
        pos = cook.find(s)
        if pos == -1:
            ret.append(None)
            continue
        cook = cook[pos + len(s):]
        ret.append(cook[:cook.find(";")])
    return ret


def insert_to_db(title, headers, name, url, image=""):
    if image == "":
        image = "images/" + title + ".jpg"
    con = get_db_connection()
    with con:
        cur = con.cursor()
        try:
            cur.execute("insert into dump values (?,?,?,?,?)",
            (headers["Cookie"], headers["User-Agent"], image,
            '[' + title + ']\n' + name, url))
            return True
        except IntegrityError:
            return False


def get_db_connection():
    return get_db_connection.con


def set_db_connection(con):
    get_db_connection.con = con
