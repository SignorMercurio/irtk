# import requests

# from config import config

# yuque = config['yuque']
# namespace = yuque['namespace']
# base_url = 'https://yuque-api.antfin-inc.com'

# def create_doc(title, content):
#     path = f'/api/v2/repos/{namespace}/docs'

#     headers = {
#         'Content-Type': 'application/json',
#         'X-Auth-Token': yuque['ak']
#     }

#     body = {
#         'title': title,
#         'format': 'markdown',
#         'body': content
#     }

#     response = requests.post(base_url + path, headers=headers, json=body)
#     slug = response.json()['data']['slug']

#     return f'https://aliyuque.antfin.com/{namespace}/{slug}'
