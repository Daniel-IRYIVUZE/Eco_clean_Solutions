import unittest
from flask import url_for
from EcoApp import create_app, db, bcrypt
from EcoApp.model import Users, Services, Order
from EcoApp.form import RegisterForm, LoginForm, ServiceForm, RangeTime, ProfileForm

class TestRoutes(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.app = create_app()
        cls.app.config['TESTING'] = True
        cls.app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        cls.app.config['WTF_CSRF_ENABLED'] = False

        with cls.app.app_context():
            db.create_all()

    @classmethod
    def tearDownClass(cls):
        with cls.app.app_context():
            db.drop_all()

    def setUp(self):
        self.client = self.app.test_client()
        self.app_context = self.app.app_context()
        self.app_context.push()

        # Create a test user
        hashed_pw = bcrypt.generate_password_hash('password').decode('utf-8')
        self.user = Users(
            first_name='John',
            last_name='Doe',
            email='john.doe@example.com',
            password=hashed_pw,
            district='District',
            sector='Sector',
            village='Village',
            cell='Cell'
        )
        db.session.add(self.user)
        db.session.commit()

    def tearDown(self):
        db.session.remove()
        self.app_context.pop()

    def login(self, email, password):
        return self.client.post('/login', data=dict(
            email=email,
            password=password
        ), follow_redirects=True)

    def test_index(self):
        response = self.client.get(url_for('index'))
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'index.html', response.data)

    def test_register_get(self):
        response = self.client.get(url_for('register'))
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'signup.html', response.data)

    def test_register_post(self):
        response = self.client.post('/register', data=dict(
            firstname='Jane',
            lastname='Doe',
            email='jane.doe@example.com',
            district='District',
            sector='Sector',
            village='Village',
            street='Street',
            cell='Cell',
            password='password',
            confirm_password='password'
        ), follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Your account was successfully created', response.data)

    def test_login_get(self):
        response = self.client.get(url_for('login'))
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'login.html', response.data)

    def test_login_post(self):
        response = self.login('john.doe@example.com', 'password')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'index.html', response.data)

    def test_logout(self):
        self.login('john.doe@example.com', 'password')
        response = self.client.get('/logout', follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'index.html', response.data)

    def test_admin_access_denied(self):
        self.login('john.doe@example.com', 'password')
        response = self.client.get('/admin', follow_redirects=True)
        self.assertEqual(response.status_code, 403)

    def test_book_service(self):
        self.login('john.doe@example.com', 'password')
        service = Services(service_name='Cleaning', price=100)
        db.session.add(service)
        db.session.commit()

        response = self.client.get(url_for('book', service_name='Cleaning'))
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'booking.html', response.data)

        response = self.client.post(url_for('book', service_name='Cleaning'), data=dict(
            serviceName='Cleaning',
            price=100,
            date='2023-12-31'
        ), follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Your order has been placed successfully', response.data)

    def test_user_dashboard(self):
        self.login('john.doe@example.com', 'password')
        response = self.client.get(url_for('user_dash'))
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'user-dash.html', response.data)

    def test_settings_get(self):
        self.login('john.doe@example.com', 'password')
        response = self.client.get(url_for('settings'))
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'settings.html', response.data)

    def test_settings_post(self):
        self.login('john.doe@example.com', 'password')
        response = self.client.post('/settings', data=dict(
            firstname='John',
            lastname='Doe',
            email='john.doe@example.com',
            district='District',
            sector='Sector',
            village='Village',
            street='Street',
            cell='Cell',
            current_password='password'
        ), follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Your Profile info was successfully updated', response.data)

if __name__ == '__main__':
    unittest.main()
