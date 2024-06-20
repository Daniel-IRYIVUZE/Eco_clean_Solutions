import unittest
from datetime import datetime, timedelta
from flask import Flask
from EcoApp.forms import RegisterForm, LoginForm, ServiceForm, RangeTime, ProfileForm
from EcoApp.model import Users
from flask_sqlalchemy import SQLAlchemy

# Setup Flask app and database for testing
app = Flask(__name__)
app.config['TESTING'] = True
app.config['WTF_CSRF_ENABLED'] = False  # Disable CSRF for testing
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'  # Use in-memory SQLite database for testing
db = SQLAlchemy(app)

# Create a mock Users model for testing
class MockUsers:
    @staticmethod
    def query():
        return MockQuery()

class MockQuery:
    @staticmethod
    def filter_by(email):
        # Simulate no user found
        return None

# Assign the mock model to the Users
Users.query = MockUsers.query

class TestForms(unittest.TestCase):

    def test_register_form_valid(self):
        form = RegisterForm(data={
            'firstname': 'John',
            'lastname': 'Doe',
            'email': 'john.doe@example.com',
            'district': 'District',
            'sector': 'Sector',
            'village': 'Village',
            'street': 'Street',
            'cell': 'Cell',
            'password': 'password123',
            'confirm_password': 'password123'
        })
        self.assertTrue(form.validate())

    def test_register_form_missing_fields(self):
        form = RegisterForm(data={})
        self.assertFalse(form.validate())
        self.assertIn('This field is required.', form.firstname.errors)
        self.assertIn('This field is required.', form.lastname.errors)
        self.assertIn('This field is required.', form.email.errors)
        self.assertIn('This field is required.', form.district.errors)
        self.assertIn('This field is required.', form.sector.errors)
        self.assertIn('This field is required.', form.village.errors)
        self.assertIn('This field is required.', form.cell.errors)
        self.assertIn('This field is required.', form.password.errors)
        self.assertIn('This field is required.', form.confirm_password.errors)

    def test_register_form_invalid_email(self):
        form = RegisterForm(data={
            'firstname': 'John',
            'lastname': 'Doe',
            'email': 'invalid-email',
            'district': 'District',
            'sector': 'Sector',
            'village': 'Village',
            'street': 'Street',
            'cell': 'Cell',
            'password': 'password123',
            'confirm_password': 'password123'
        })
        self.assertFalse(form.validate())
        self.assertIn('Invalid email address.', form.email.errors)

    def test_register_form_email_already_taken(self):
        # Mock the query to simulate email already taken
        class MockQuery:
            @staticmethod
            def filter_by(email):
                return MockQuery()

            def first(self):
                return True

        Users.query = MockQuery

        form = RegisterForm(data={
            'firstname': 'John',
            'lastname': 'Doe',
            'email': 'existing@example.com',
            'district': 'District',
            'sector': 'Sector',
            'village': 'Village',
            'street': 'Street',
            'cell': 'Cell',
            'password': 'password123',
            'confirm_password': 'password123'
        })
        self.assertFalse(form.validate())
        self.assertIn('Email already taken, please use another one', form.email.errors)

    def test_service_form_valid(self):
        form = ServiceForm(data={
            'serviceName': 'Cleaning',
            'price': 100,
            'date': (datetime.now() + timedelta(days=1)).date()
        })
        self.assertTrue(form.validate())

    def test_service_form_invalid_date(self):
        form = ServiceForm(data={
            'serviceName': 'Cleaning',
            'price': 100,
            'date': (datetime.now() - timedelta(days=1)).date()
        })
        self.assertFalse(form.validate())
        self.assertIn('Date invalid, please select a future date', form.date.errors)

if __name__ == '__main__':
    unittest.main()
