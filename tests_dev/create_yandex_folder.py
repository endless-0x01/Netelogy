import string
from time import sleep
import requests
from requests import Session
import os
import random



def init_session() -> Session:
    session = requests.Session()
    session.headers.update(
        {
            "Authorization": f"OAuth {os.getenv('YANDEX_TOKEN')}",
            "Content-Type": "application/json",
            "Accept": "application/json",
        }
    )
    return session


def create_folder(session: Session, folder_path: str) -> requests.Response:
    url = "https://cloud-api.yandex.net/v1/disk/resources"
    params = {"path": folder_path}
    response = session.put(url, params=params)
 
    return response


def generate_name_name_folder():
    suffix = "".join(random.choices(string.ascii_letters + string.digits, k=6))
    return f"/test_folders_{suffix.lower()}"


def delete_folder(session: Session, folder_path: str) -> requests.Response:
    url = "https://cloud-api.yandex.net/v1/disk/resources"
    params = {'path': folder_path, 'permanently': True}
    response = session.delete(url, params=params)
    return response


def main():
    session = init_session()
    folder_path =  generate_name_name_folder()
    response = create_folder(session, folder_path)
    sleep(5)
    delete_folder(session, folder_path)


if __name__ == "__main__":
    main()
