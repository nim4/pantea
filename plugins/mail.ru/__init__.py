from lib.util import get_info_by_url, insert_to_db

__host = "mail.ru"
__sess = "Mpop="


def parse(headers):
    name = get_info_by_url("http://mail.ru/",
    headers, [('class="x-ph__auth__user__text">', '<')])[0]
    if name is None:
        return False
    insert_to_db("Mail.ru", headers, name, "http://e.mail.ru/")
    return True
