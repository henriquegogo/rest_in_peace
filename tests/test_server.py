import unittest, sys
sys.path.append('./src')
from rest_in_peace import Server

class TestServer(unittest.TestCase):
    def test(self):
        self.assertTrue(True)

if __name__ == '__main__':
    unittest.main()
