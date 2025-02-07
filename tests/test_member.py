# this file is used to design tests for members

# imports
from app import create_app # import function to create instance of flask app
from app.models import db, Member # import db to manage database, member to create app instance with a member
import unittest # import unittest to set up and run test cases
from datetime import datetime # import datetime for test user
from app.utils.util import encode_token
import jwt

# create member test cases
class TestMember(unittest.TestCase): # inheriting from unittest.TestCase
    def setUp(self):
        self.app = create_app("TestingConfig") # create test app instance using TestingConfig
        self.member = Member(name="test_user", email="test@email.com", DOB=datetime.strptime("1900-01-01", "%Y-%m-%d").date() , password='test')
        with self.app.app_context():
            db.drop_all() # clear existing tables, reset database
            db.create_all() # set up fresh tables for each test
            db.session.add(self.member)
            db.session.commit()
        self.token = encode_token(1)
        self.client = self.app.test_client() # create test client to simulate requests

    # positive create member test case
    def test_create_member(self):
        member_payload = {
            "name": "John Doe",
            "email": "jd@email.com",
            "DOB": "1900-01-01",
            "password": "123"
        }

        response = self.client.post('/members/', json=member_payload)
        self.assertEqual(response.status_code, 201)
        self. assertEqual(response.json['name'], "John Doe")

    # negative create member test case
    def test_invalid_creation(self):
        member_payload = {
            "name": "John Doe",
            "DOB": "1900-01-01",
            "password": "123"       
        }

        response = self.client.post('/members/', json=member_payload)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json['email'], ['Missing data for required field.'])

    # positive member login test case 
    def test_login_member(self):
        credentials = {
            "email": "test@email.com",
            "password": "test"
        }

        response = self.client.post('/members/login', json=credentials)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json['status'], 'success')
        print("\nPRINTING:\n",response.json)
        return response.json['token']
    
    # nagative member login test case
    def test_invalid_login(self):
        credentials = {
            "email": "bad_email@email.com",
            "password": "bad_pw"
        }

        response = self.client.post('/members/login', json=credentials)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json['message'], 'invalid email or password')

    # positive update member test case
    def test_update_member(self):
        update_payload = {
            "name": "Peter",
            "email": "test@email.com",
            "DOB": "1900-01-01",
            "password": "test"
        }

        headers = {'Authorization': "Bearer " + self.test_login_member()}

        response = self.client.put('/members/1', json=update_payload, headers=headers)
        print("\nPRINTING:\n", response.json)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json['name'], 'Peter') 
        self.assertEqual(response.json['email'], 'test@email.com')

    # negative update member test case
    