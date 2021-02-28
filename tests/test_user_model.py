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

    def test_password_setter(self):
        u = User(password='fraszka')
        self.assertTrue(u.password_hash is not None)

    def test_no_password_getter(self):
        u = User(password='fraszka')
        with self.assertRaises(AttributeError):
            u.password

    def test_password_salts_are_random(self):
        u = User(password='fraszka')
        u2 = User(password='fraszka')
        self.assertTrue(u.password_hash != u2.password_hash)


if __name__ == '__main__':
    unittest.main()
