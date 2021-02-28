import os, sys
import unittest

topdir = os.path.join(os.path.dirname(__file__), '..')
sys.path.append(topdir)

from poorcms import app, db
from poorcms.models import User

TEST_DB = 'test.db'


class UserModelTestCase(unittest.TestCase):
    def setUp(self):
        app.config['TESTING'] = True
        app.config['DEBUG'] = False
        app.config['SQLALCHEMY_DATABASE_URI'] = ('sqlite:///' +
            os.path.join(topdir, TEST_DB))
        self.app = app.test_client()
        db.drop_all()
        db.create_all()

    def tearDown(self):
        pass


if __name__ == '__main__':
    unittest.main()
