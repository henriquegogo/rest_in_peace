import unittest, sys, os
sys.path.append('./src')
from rest_in_peace import Database

class TestDatabase(unittest.TestCase):
    db_filename = 'test_database.db'

    def setUp(self):
        self.db = Database(self.db_filename)

    def tearDown(self):
        os.remove(self.db_filename)

    def test_drop(self):
        table = 'data_drop'
        self.db.table(table, {})
        created_table = list(self.db.schema().keys())
        self.db.drop(table)
        droped_table = list(self.db.schema().keys())

        self.assertTrue(table in created_table)
        self.assertTrue(table not in droped_table)

    def test_list(self):
        table = 'listed_data'
        self.db.table(table, {'description': ''})
        self.db.create(table, {'description': 'Left'})
        self.db.create(table, {'description': 'Right'})
        self.db.create(table, {'description': 'Left'})
        listed_data = self.db.list(table, {})
        filtered_data = self.db.list(table, {'description': 'Left'})
        limited_data = self.db.list(table, {'limit': '1'})
        offset_data = self.db.list(table, {'limit': '1', 'offset': '1'})

        self.assertEqual(len(listed_data), 3)
        self.assertEqual(len(filtered_data), 2)
        self.assertEqual(filtered_data[0]['description'], 'Left')
        self.assertEqual(len(limited_data), 1)
        self.assertEqual(offset_data[0]['description'], 'Right')

    def test_create(self):
        table = 'created_data'
        self.db.table(table, {'description': ''})
        created = self.db.create(table, {'description': 'Created'})

        self.assertEqual(created['id'], 1)
        self.assertEqual(created['description'], 'Created')

    def test_read(self):
        table = 'read_data'
        self.db.table(table, {'description': ''})
        self.db.create(table, {'description': 'Created'})
        data = self.db.read(table, '1')

        self.assertEqual(data['description'], 'Created')

    def test_update(self):
        table = 'updated_data'
        self.db.table(table, {'description': ''})
        created = self.db.create(table, {'description': 'Created'})
        updated = self.db.update(table, created['id'], {'description': 'Updated'})

        self.assertEqual(updated['description'], 'Updated')

    def test_delete(self):
        table = 'deleted_data'
        self.db.table(table, {'description': ''})
        created = self.db.create(table, {'description': 'Created'})
        self.db.delete(table, created['id'])

        try:
            data = self.db.read(table, created['id'])
            self.assertTrue(data)
        except:
            self.assertTrue('Deleted')

if __name__ == '__main__':
    unittest.main()
