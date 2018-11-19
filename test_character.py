import unittest, os, json
from app import create_app, db

class CharacterTestCase(unittest.TestCase):
    """Character Test Cases"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app(config_name="testing")
        self.client = self.app.test_client
        self.Character = {
            "name" : 'Ness',
            "hp" : 100,
            'mana' : 45,
            "attack" : 24,
            "defense" : 18,
            'intelligence' : 20,
            'luck' : 16
        }
        self.Character2 = {  
            'name' : 'Paula',
            'hp' : 110,
            'mana' : 60,
            'attack' : 20,
            'defense' : 20,
            'intelligence' : 22,
            'luck' : 12
        } 
        # binds the app to the current context
        with self.app.app_context():
            # create all tables
            db.create_all()
    
    def test_character_creation(self):
        """Test API can create a bucketlist (POST request)"""
        response = self.client().post('/characters/', data=self.Character)
        self.assertEqual(response.status_code, 201)
        self.assertIn('Ness', repr(response.data))

    def test_get_all_characters(self):
        """Test API can get a bucketlist (GET request)."""
        self.client().post('/characters/', data=self.Character)
        response = self.client().get('/characters/')
        self.assertEqual(response.status_code, 200)
        self.assertIn('Ness', repr(response.data))

    def test_get_character_by_id(self):
        """Test API can get a single bucketlist by using it's id."""
        response = self.client().post('/characters/', data=self.Character)
        result_in_json = json.loads(response.data.decode('utf-8').replace("'", "\""))
        result = self.client().get(
            '/characters/{}'.format(result_in_json['id'])
        )
        self.assertEqual(result.status_code, 200)
        self.assertIn('Ness', repr(result.data))

    def test_character_can_be_edited(self):
        """Test API can edit an existing bucketlist. (PUT request)"""
        response = self.client().post('/characters/', data=self.Character2)
        response = self.client().patch(
            '/characters/1',
            data={  'name' : 'Ana'})
        self.assertEqual(response.status_code, 200)
        result = self.client().get('/characters/1')
        self.assertIn('Ana', repr(result.data))
    
    def test_character_deletion(self):
        response = self.client().post('/characters/', data=self.Character2)
        response = self.client().delete('/characters/1')
        self.assertEqual(response.status_code, 200)
        # Test to see if it exists, should return a 404
        response = self.client().delete('/character/1')
        self.assertEqual(response.status_code, 404)
    
    def test_character_level_up(self):
        lvlData = [
            {
                'id' : 1,
                'exp' : 45
            },
        ]
        response = self.client().post('/characters/', data=self.Character)
        response = self.client().post('/characters/addexp/', data=lvlData)
        result_in_json = json.loads(response.data.decode('utf-8').replace("'", "\""))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(result_in_json['level'], 2)

        toNext = result_in_json['Exp to next level']
        self.assertTrue(toNext >= 45 and toNext <= 49)


    def tearDown(self):
        """teardown all initialized variables."""
        with self.app.app_context():
            # drop all tables
            db.session.remove()
            db.drop_all()
    
if __name__=="__main__":
    unittest.main()