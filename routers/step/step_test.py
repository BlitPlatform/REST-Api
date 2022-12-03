from fastapi.testclient import TestClient
from services.common.decoders.b64helper import encode_to_b64
from definitions import TEST_FILES_PATH, TEST_FILE_NAME

from main import app

client = TestClient(app)

STEP_URL = "/step"


def read_test_file() -> str:
    encoded_file = None
    try:
        with open(TEST_FILES_PATH + "/" + TEST_FILE_NAME, "r", encoding='utf8') as test_file:
            encoded_string = encode_to_b64(test_file.read())
            encoded_file = encoded_string
    except FileNotFoundError as fne:
        print("Error: %s - %s." % (fne.filename, fne.strerror))
    except Exception as e:
        print("Error: %s - %s." % (e))
    finally:
        return encoded_file


def test_upload_file():
    encoded_file = read_test_file()
    assert encoded_file is not None

    url = STEP_URL + "/upload"
    payload = {"filename": TEST_FILE_NAME, "filedata": encoded_file}

    headers = {
        "Content-Type": "application/json",
        "x-token": "fake-jwt",
    }
    response = client.post(url=url, headers=headers, json=payload)
    assert response.status_code == 200
    assert response.headers['Content-Type'] == 'application/x-zip-compressed' 
