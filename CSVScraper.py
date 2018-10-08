import requests
import re

LOGIN_URL = r'https://meet.insuretechconnect.com/login'
USERS_URL = r'https://meet.insuretechconnect.com/user?user_page={}'

csv_file = open('test.csv', 'w', encoding='utf-8')
csv_file.write('Ime i Prezime,Firma,Funkcija')
csv_file.write('\n')

if __name__ == '__main__':
    payload = {
        'user[email]': '<USERNAME>',
        'user[password]': '<PASSWORD>'
    }

    with requests.session() as session:
        session.get(LOGIN_URL)
        session.post(LOGIN_URL, data=payload)
        users = set()
        page_num = 1
        while True:
            response = session.get(USERS_URL.format(page_num))

            usernames = re.findall(
                r'<a class=\"user_link\" href=\"https://meet\.insuretechconnect\.com/profile/member/\d+\">(.+?)</a>',
                response.content.decode('utf-8'))

            companys = re.findall(
                r'<span class="company">(.+?)</span>',
                response.content.decode('utf-8'))

            positions = re.findall(
                r'<span class="position">(.+?)</span>',
                response.content.decode('utf-8'))

            if not usernames:
                break

            for i in range(0, len(usernames)):
                company = ''
                position = ''

                try:
                    company = companys[i]
                except:
                    company = "/"

                try:
                    position = positions[i]
                except:
                    position = "/"

                csv_file.write(usernames[i].replace(",",";") + "," + company.replace(",", ";") + "," + position.replace(",", ";")  + "\n")
                print(usernames[i], company, position)
            users.update(usernames)
            page_num += 1

    print("FINISH!!")
