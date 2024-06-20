import unittest
from datetime import datetime, timedelta
from EcoApp import create_app, db
from EcoApp.model import Users, Services, Order, OrderServices

class TestModels(unittest.TestCase):

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
        self.app_context = self.app.app_context()
        self.app_context.push()

    def tearDown(self):
        db.session.remove()
        self.app_context.pop()

    def test_user_creation(self):
        user = Users(
            first_name="John",
            last_name="Doe",
            email="john.doe@example.com",
            district="District",
            sector="Sector",
            village="Village",
            street="Street",
            password="password",
            cell="Cell"
        )
        db.session.add(user)
        db.session.commit()
        retrieved_user = Users.query.filter_by(email="john.doe@example.com").first()
        self.assertIsNotNone(retrieved_user)
        self.assertEqual(retrieved_user.email, "john.doe@example.com")

    def test_service_creation(self):
        service = Services(service_name="Cleaning", price=100)
        db.session.add(service)
        db.session.commit()
        retrieved_service = Services.query.filter_by(service_name="Cleaning").first()
        self.assertIsNotNone(retrieved_service)
        self.assertEqual(retrieved_service.service_name, "Cleaning")

    def test_order_creation(self):
        user = Users(
            first_name="Jane",
            last_name="Smith",
            email="jane.smith@example.com",
            district="District",
            sector="Sector",
            village="Village",
            street="Street",
            password="password",
            cell="Cell"
        )
        db.session.add(user)
        db.session.commit()

        order = Order(
            user_id=user.id,
            scheduled_date=(datetime.now() + timedelta(days=1)).date()
        )
        db.session.add(order)
        db.session.commit()

        retrieved_order = Order.query.filter_by(user_id=user.id).first()
        self.assertIsNotNone(retrieved_order)
        self.assertEqual(retrieved_order.user_id, user.id)

    def test_order_services_relationship(self):
        user = Users(
            first_name="Emily",
            last_name="Jones",
            email="emily.jones@example.com",
            district="District",
            sector="Sector",
            village="Village",
            street="Street",
            password="password",
            cell="Cell"
        )
        db.session.add(user)
        db.session.commit()

        service1 = Services(service_name="Gardening", price=150)
        service2 = Services(service_name="Plumbing", price=200)
        db.session.add(service1)
        db.session.add(service2)
        db.session.commit()

        order = Order(
            user_id=user.id,
            scheduled_date=(datetime.now() + timedelta(days=1)).date()
        )
        db.session.add(order)
        db.session.commit()

        order_service1 = OrderServices(order_id=order.id, service_id=service1.id)
        order_service2 = OrderServices(order_id=order.id, service_id=service2.id)
        db.session.add(order_service1)
        db.session.add(order_service2)
        db.session.commit()

        retrieved_order_services = OrderServices.query.filter_by(order_id=order.id).all()
        self.assertEqual(len(retrieved_order_services), 2)
        self.assertEqual(retrieved_order_services[0].service_id, service1.id)
        self.assertEqual(retrieved_order_services[1].service_id, service2.id)

if __name__ == '__main__':
    unittest.main()
