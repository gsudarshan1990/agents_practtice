import unittest
import json
from flask import Flask
from models import Publisher, db, init_db
from routes.publishers import publishers_bp

class TestPublishersRoutes(unittest.TestCase):
    TEST_PUBLISHERS = [
        {"name": "DevGames Inc"},
        {"name": "Scrum Masters"}
    ]

    def setUp(self):
        """Set up test database and seed data"""
        self.app = Flask(__name__)
        self.app.config['TESTING'] = True
        self.app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        self.app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
        
        self.app.register_blueprint(publishers_bp)
        self.client = self.app.test_client()
        
        init_db(self.app, testing=True)
        
        with self.app.app_context():
            db.create_all()
            self._seed_test_data()

    def tearDown(self):
        """Clean up test database"""
        with self.app.app_context():
            db.session.remove()
            db.drop_all()
            db.engine.dispose()

    def _seed_test_data(self):
        """Helper method to seed test publishers"""
        publishers = [Publisher(**data) for data in self.TEST_PUBLISHERS]
        db.session.add_all(publishers)
        db.session.commit()

    def test_get_publishers(self):
        """Test successful retrieval of publishers"""
        response = self.client.get('/api/publishers')
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(data), len(self.TEST_PUBLISHERS))
        
        for i, publisher in enumerate(data):
            self.assertIn('id', publisher)
            self.assertEqual(publisher['name'], self.TEST_PUBLISHERS[i]['name'])

if __name__ == '__main__':
    unittest.main()
