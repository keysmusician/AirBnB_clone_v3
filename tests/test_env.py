"""A test ensuring unit tests are done in the testing environment."""
from os import environ
import unittest


class TestEnv(unittest.TestCase):
    """Checks the test environment."""

    def test_using_test_environment(self):
        test_environment = {
            'HBNB_MYSQL_USER': 'hbnb_test',
            'HBNB_MYSQL_PWD': 'hbnb_test_pwd',
            'HBNB_MYSQL_HOST': 'localhost',
            'HBNB_MYSQL_DB': 'hbnb_test_db',
            'HBNB_TYPE_STORAGE': 'db'
        }

        # Ensure tests were executed in the test environment
        # ? This mainly ensures the test database is used.
        for key, value in test_environment.items():
            if environ.get(key) != value:
                raise EnvironmentError(
                    'Do not run this test outside of the test environment.'
                )


if __name__ == '__main__':
    unittest.main()
