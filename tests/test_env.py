"""A function ensuring unit tests are done in the testing environment."""
from os import environ

def test_environment_is_set():
    """Checks if the test environment variables are set"""
    test_environment = {
        'HBNB_MYSQL_USER': 'hbnb_test',
        'HBNB_MYSQL_PWD': 'hbnb_test_pwd',
        'HBNB_MYSQL_HOST': 'localhost',
        'HBNB_MYSQL_DB': 'hbnb_test_db',
        'HBNB_TYPE_STORAGE': 'db'
    }

    for key, value in test_environment.items():
        if environ.get(key) != value:
            return False
    return True
