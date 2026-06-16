import requests


def make_request(url, data):
    token = ''  # need token
    headers = {'Authorization': f"Token {token}"
               }

    response = requests.post(url=url,
                             headers=headers,
                             json=data)

    if response.ok:
        print("Успешно\n", response.text)\

    else:
        print(response.status_code, response.text)
