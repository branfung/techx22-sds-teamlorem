import unittest
from objects.user import User


class TestUser(unittest.TestCase):
    def test_user_init(self):
        user1 = User('BRANDON')

        self.assertEqual(user1, 'My name is Brandon.')
        self.assertRaises(User(45), TypeError)

if __name__ == '__main__':
    unittest.main()
