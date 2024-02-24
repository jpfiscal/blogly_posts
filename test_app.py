from unittest import TestCase

from app import app
from models import db, User

# Use test database and don't clutter tests with SQL
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///test_blogly'
app.config['SQLALCHEMY_ECHO'] = False

# Make Flask errors be real errors, rather than HTML pages with error info
app.config['TESTING'] = True

# This is a bit of hack, but don't use Flask DebugToolbar
app.config['DEBUG_TB_HOSTS'] = ['dont-show-debug-toolbar']

with app.app_context():
    db.drop_all()
    db.create_all()

class UserViewsTestCase(TestCase):
    """Tests Views for Users"""

    def setUp(self):
        """Add sample user."""
        with app.app_context():
            User.query.delete()

            user = User(first_name="testUser", last_name="Testy", image_url="img/default_profile.jpeg")
            
            db.session.add(user)
            db.session.commit()

            self.user_id = user.id
    
    def tearDown(self):
        """Clean up uncommitted transactions"""
        with app.app_context():
            db.session.rollback()

    def test_list_user(self):
        with app.test_client() as client:
            resp = client.get("/users")
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('testUser', html)
    
    def test_show_detail(self):
        with app.test_client() as client:
            resp = client.get(f"/users/{self.user_id}")
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('testUser Testy', html)

    def test_add_user(self):
        with app.test_client() as client:
            d = {"ip_first_name": "TestUser2", "ip_last_name": "Testy2", "ip_img": ""}
            resp = client.post("/users/new", data=d, follow_redirects=True)
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn("TestUser2 Testy2", html)

    def test_edit_user(self):
        with app.test_client() as client:
            d = {"ip_first_name": "TestUser_Edit", "ip_last_name": "Testy", "ip_img": "img/default_profile.jpeg"}
            resp = client.post(f"/users/{self.user_id}/edit", data=d, follow_redirects=True)
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn("TestUser_Edit Testy", html)

