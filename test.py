import requests
from bs4 import BeautifulSoup

# URL сторінки входу та адреса, на яку потрібно відправити POST-запит
login_url = 'http://45.44.151.148/'
post_url = 'http://45.44.151.148/cgi-bin/dologin'

# Користувацькі дані
user = ''
paswd = 'admin'

# Створення сесії
session = requests.Session()

# Відправлення POST-запиту для отримання cookies
response_get = session.get(login_url)

form_data = {
    'username': user,
    'password': paswd,
    # Додайте інші параметри форми, якщо вони потрібні
}

# Відправлення POST-запиту з даними форми та cookies
response_post = session.post(post_url, data=form_data)

# Перевірка, чи вдалося увійти (перевірка наявності конкретного елементу на сторінці)
soup = BeautifulSoup(response_post.text, 'html.parser')

if soup.find('<b></b>', class_='l') is not None:
    print('Успішно увійшли на grandstream ht801.')
else:
    print('Try again')
# Закриття сесії
session.close()

