import requests
from requests import Session
import pytest

from tests_dev.create_yandex_folder import (
        init_session,
        create_folder,
        delete_folder, 
        generate_name_name_folder,
)



@pytest.fixture()
def session():
        return init_session()

@pytest.fixture()
def random_folder_name():
        return generate_name_name_folder()


@pytest.fixture
def temporary_folder(session):
        folder_name = generate_name_name_folder()
        responce = create_folder(session, folder_name)
        assert responce.status_code in [200, 201]

        yield folder_name

        delete_response = delete_folder(session, folder_name)
        print(f"Удалена папка: {folder_name}, статус: {delete_response.status_code}")



def test_check_init_session(session):

        assert isinstance(session, Session)

        assert 'Authorization' in session.headers
        assert 'Content-Type' in session.headers
        assert 'Accept' in session.headers


        assert session.headers["Content-Type"] == "application/json"
        assert session.headers["Accept"] == "application/json"

        assert "OAuth" in session.headers["Authorization"]

def test_create_folder_success(temporary_folder):
        assert temporary_folder.startswith('/test_folders_')

def test_create_folder_and_delete(session, random_folder_name):
        response = create_folder(session, random_folder_name)
        assert response.status_code in [200, 201]

        response = delete_folder(session, random_folder_name)
        assert response.status_code in [204]