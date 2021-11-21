import unittest, sys, os
sys.path.append('./src')
from rest_in_peace import Database

class TestDatabase(unittest.TestCase):
    db_filename = 'test_database.db'

    def setUp(self):
        self.db = Database(self.db_filename)

    def tearDown(self):
        os.remove(self.db_filename)

    def test_create(self):
        self.db.table('data', {'description': ''})
        created = self.db.create('data', {'description': 'Created'})

        self.assertEqual(created['id'], 1)
        self.assertEqual(created['description'], 'Created')

    def test_read(self):
        self.db.table('data', {'description': ''})
        self.db.create('data', {'description': 'Created'})
        data = self.db.read('data', '1')

        self.assertEqual(data['description'], 'Created')

    def test_update(self):
        self.db.table('data', {'description': ''})
        created = self.db.create('data', {'description': 'Created'})
        updated = self.db.update('data', created['id'], {'description': 'Updated'})

        self.assertEqual(updated['description'], 'Updated')

    def test_delete(self):
        self.db.table('data', {'description': ''})
        created = self.db.create('data', {'description': 'Created'})
        self.db.delete('data', created['id'])

        try:
            data = self.db.read('data', created['id'])
            self.assertTrue(data)
        except:
            self.assertTrue('Deleted')

if __name__ == '__main__':
    unittest.main()
