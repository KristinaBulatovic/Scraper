import requests
import re

LOGIN_URL = r'https://meet.insuretechconnect.com/login'
USERS_URL = r'https://meet.insuretechconnect.com/user?user_page={}'


if __name__ == '__main__':
    payload = {
        'user[email]': '<USERNAME>',
        'user[password]': '<PASSWORD>'
    }

    file = open('testfile.txt', 'w',  encoding="utf-8")

    with requests.session() as session:
        session.get(LOGIN_URL)
        session.post(LOGIN_URL, data=payload)
        users = set()
        page_num = 1
        while True:
            file.write("Parsing page: {}".format(page_num))
            file.write("\n")
            print("Parsing page: {}".format(page_num))
            response = session.get(USERS_URL.format(page_num))
            current = re.findall(
                r'<a class=\"user_link\" href=\"https://meet\.insuretechconnect\.com/profile/member/\d+\">(.+?)</a>',
                response.content.decode('utf-8'))
            if not current:
                break
            file.write(str(current))
            file.write("\n")
            print(current)
            users.update(current)
            page_num += 1
        print(users)
