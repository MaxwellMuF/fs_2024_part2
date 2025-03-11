import unittest
import bcrypt
import yaml
import os
from application.src.utilities.authenticator_exceptions import (UserNotExistError, 
                                                                PasswordWrongError, 
                                                                MissingFieldError, 
                                                                UserExistError, 
                                                                UserNameError, 
                                                                RegisterKeyError, 
                                                                PasswordEqualError, 
                                                                PasswordLengthError)

from application.src.utilities.authenticator import (Hasher, 
                                                     FileLoader, 
                                                     Authenticator, 
                                                     RegisterNewUser)

class TestHasher(unittest.TestCase):
    def setUp(self):
        self.hasher = Hasher()

    def test_hash_string(self):
        hashed = self.hasher.hash_string("testpassword")
        self.assertTrue(isinstance(hashed, str) and len(hashed) > 0)

    def test_check_pw(self):
        password = "securepassword"
        hashed = self.hasher.hash_string(password)
        self.assertTrue(self.hasher.check_pw(password, hashed))
        self.assertFalse(self.hasher.check_pw("wrongpassword", hashed))

class TestFileLoader(unittest.TestCase):
    def setUp(self):
        self.test_file = "test_credentials1.yaml"
        self.test_data = {"test_user": {"password": "hashed_pw"}}
        with open(self.test_file, "w") as file:
            yaml.safe_dump(self.test_data, file)
        self.file_loader = FileLoader(path=self.test_file)

    def tearDown(self):
        os.remove(self.test_file)

    def test_load_yaml(self):
        loaded_data = self.file_loader.load_yaml()
        self.assertEqual(loaded_data, self.test_data)

    def test_save_yaml(self):
        new_data = {"new_user": {"password": "new_hashed_pw"}}
        self.file_loader.save_yaml(new_data)
        with open(self.test_file, "r") as file:
            loaded_data = yaml.safe_load(file)
        self.assertEqual(loaded_data, new_data)

class TestAuthenticator(unittest.TestCase):
    def setUp(self):
        self.test_file = "test_credentials2.yaml"
        self.test_data = {"test_user": {"password": bcrypt.hashpw("test123".encode(), bcrypt.gensalt()).decode()}}
        with open(self.test_file, "w") as file:
            yaml.safe_dump(self.test_data, file)
        self.authenticator = Authenticator(self.test_file)

    def tearDown(self):
        os.remove(self.test_file)

    def test_username_setter_valid(self):
        self.authenticator.username = "test_user"
        self.assertEqual(self.authenticator.username, "test_user")

    def test_username_setter_invalid(self):
        with self.assertRaises(UserNotExistError):
            self.authenticator.username = "non_existent_user"

    def test_password_setter_valid(self):
        self.authenticator.username = "test_user"
        self.authenticator.password = "test123"  # Should not raise error

    def test_password_setter_invalid(self):
        self.authenticator.username = "test_user"
        with self.assertRaises(PasswordWrongError):
            self.authenticator.password = "wrongpassword"
            
    def test_reset_password(self):
        password_new = "testabc"
        self.authenticator.reset_password(username="test_user", password="test123", password_new=password_new,
                                          repeat_new_password=password_new)
        self.authenticator.password = password_new # Should not raise error
        

class TestRegisterNewUser(unittest.TestCase):
    def setUp(self):
        self.test_file = "test_credentials3.yaml"
        self.test_data = {
            "register": {"register_key": bcrypt.hashpw("regkey".encode(), bcrypt.gensalt()).decode()},
            "existing_user": {"password": bcrypt.hashpw("password".encode(), bcrypt.gensalt()).decode()}
        }
        with open(self.test_file, "w") as file:
            yaml.safe_dump(self.test_data, file)
        self.registrar = RegisterNewUser(self.test_file)

    def tearDown(self):
        os.remove(self.test_file)

    def test_new_user_credential_valid(self):
        new_user = {
            "username": "newuser",
            "password": "newpassword",
            "password_repeat": "newpassword",
            "register_key": "regkey"
        }
        self.registrar.new_user_credential = new_user
        self.assertEqual(self.registrar.new_user_credential, new_user)

    def test_new_user_credential_missing_field(self):
        new_user = {"username": "", "password": "pass", "password_repeat": "pass", "register_key": "regkey"}
        with self.assertRaises(MissingFieldError):
            self.registrar.new_user_credential = new_user

    def test_new_user_credential_user_exists(self):
        new_user = {"username": "existing_user", "password": "pass", "password_repeat": "pass", "register_key": "regkey"}
        with self.assertRaises(UserExistError):
            self.registrar.new_user_credential = new_user
    
    def test_new_user_credential_user_exists(self):
        new_user = {"username": "existing_'user", "password": "pass", "password_repeat": "pass", "register_key": "regkey"}
        with self.assertRaises(UserNameError):
            self.registrar.new_user_credential = new_user

    def test_new_user_credential_invalid_register_key(self):
        new_user = {"username": "newuser", "password": "pass", "password_repeat": "pass", "register_key": "wrongkey"}
        with self.assertRaises(RegisterKeyError):
            self.registrar.new_user_credential = new_user

    def test_new_user_credential_password_mismatch(self):
        new_user = {"username": "newuser", "password": "pass", "password_repeat": "wrongpass", "register_key": "regkey"}
        with self.assertRaises(PasswordEqualError):
            self.registrar.new_user_credential = new_user
    
    def test_new_user_password_too_long(self):
        new_user = {"username": "newuser", "password": "pass"*20, "password_repeat": "pass"*20, "register_key": "regkey"}
        with self.assertRaises(PasswordLengthError):
            self.registrar.new_user_credential = new_user

    def test_save_new_user(self):
        new_user = {
            "username": "newuser",
            "password": "newpassword",
            "password_repeat": "newpassword",
            "register_key": "regkey"
        }
        self.registrar.new_user_credential = new_user
        self.registrar.save_new_user()
        with open(self.test_file, "r") as file:
            users = yaml.safe_load(file)
        self.assertIn("newuser", users)
        self.assertNotIn("password_repeat", users["newuser"])  # Ensure it's removed

if __name__ == "__main__":
    unittest.main()

