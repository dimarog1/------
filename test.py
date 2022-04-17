from requests import delete, get
from pprint import pprint

review_data = get('http://localhost:5000/api/review').json()['review']
user_data = get('http://localhost:5000/api/users').json()['user']
id_nickname = dict()
for data_elem in user_data:
    id_nickname[data_elem['id']] = data_elem['nickname']
review_info = []
for data_elem in review_data:
    if data_elem['film'] == 1:
        data_block = {
            'username': id_nickname[data_elem['user']],
            'mark': str(data_elem['mark']),
            'text': data_elem['text'],
        }
        review_info.append(data_block)
