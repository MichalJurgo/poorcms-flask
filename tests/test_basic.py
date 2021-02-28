import os, sys
import unittest

topdir = os.path.join(os.path.dirname(__file__), '..')
sys.path.append(topdir)

from poorcms import app, db


TEST_DB = 'test.db'

class BasicTests(unittest.TestCase):
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

    def test_app_exists(self):
        self.assertFalse(app is None)

    def test_app_is_testing(self):
        self.assertTrue(app.config['TESTING'])

    def test_main_page(self):
        response = self.app.get('/', follow_redirects=True)
        self.assertEqual(response.status_code, 200)



if __name__ == '__main__':
    unittest.main()
