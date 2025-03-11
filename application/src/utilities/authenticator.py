import yaml
import bcrypt

from application.src.utilities.authenticator_exceptions import (UserNotExistError,
                                                                PasswordWrongError,
                                                                MissingFieldError,
                                                                UserExistError,
                                                                UserNameError,
                                                                RegisterKeyError,
                                                                PasswordEqualError,
                                                                PasswordLengthError)

class Hasher:
    """Helper for hashing string and compare them by using bcrypt"""
        
    def hash_string(self, string: str) -> str:
        """Hash a string with 1-72 characters with random salt and a work factor of 15."""
        return bcrypt.hashpw(string.encode(), bcrypt.gensalt()).decode()

    def check_pw(self, string: str, hashed_string: str) -> bool:
        """Check if unhashed string is equal to hashed string"""
        return bcrypt.checkpw(password=string.encode(), hashed_password=hashed_string.encode())

class FileLoader:
    """Load yaml files savely and dump them"""
    def __init__(self, path: str):
        self.path_credential: str = path
        self.credential_users: dict[str,dict[str,str]] = self.load_yaml()

    def load_yaml(self) -> str:
        """Load yaml file from path safe."""
        with open(file=self.path_credential, mode="r") as file:
            credential_users = yaml.safe_load(stream=file)
        return credential_users
    
    def save_yaml(self, credential_users: dict[str,dict[str,str]]) -> None:
        """Dump dict as yaml in given path."""
        with open(file=self.path_credential, mode="w") as file:
            yaml.safe_dump(data=credential_users, stream=file)
        return
    
class Authenticator(Hasher, FileLoader):
    """Check usernames and passwords"""
    def __init__(self, path_credential: str):
        super().__init__(path=path_credential)
        self._username: str

    @property
    def username(self):
        return self._username
    
    @username.setter
    def username(self, value: str):
        """Check if user exist else raise error"""
        if value not in self.credential_users:
            raise UserNotExistError
        self._username = value
        
    @property
    def password(self):
        return self._password
    
    @password.setter
    def password(self, value: str):
        """Check if password is correct else raise error"""
        if not Hasher.check_pw(self, value, self.credential_users[self._username]["password"]):
            raise PasswordWrongError
        return

    def reset_password(self, username: str, password: str, password_new: str, repeat_new_password: str) -> None:
        """Reset password if user and password correct and valid"""
        self.username = username
        self.password = password
        
        if password_new != repeat_new_password:
            raise PasswordEqualError
        if len(password) > 72:
            raise PasswordLengthError
        
        # change pw and save
        self.credential_users[self.username]["password"] = self.hash_string(string=password_new)
        self.save_yaml(self.credential_users)
        
        return
        
        
class RegisterNewUser(Authenticator):
    def __init__(self, path_credential: str):
        super().__init__(path_credential)
        _new_user_credential: dict[str,dict]


    @property
    def new_user_credential(self):
        return self._new_user_credential
    
    @new_user_credential.setter
    def new_user_credential(self, new_user_dict: dict):
        """Check if credential is correct else raise error"""
        if not all(new_user_dict.values()):
            raise MissingFieldError
        elif new_user_dict["username"] in self.credential_users:
            raise UserExistError
        elif "'" in new_user_dict["username"]: 
            raise UserNameError
        elif not Hasher.check_pw(self, new_user_dict["register_key"], self.credential_users["register"]["register_key"]):
            raise RegisterKeyError
        elif new_user_dict["password"] != new_user_dict["password_repeat"]:
            raise PasswordEqualError
        elif len(new_user_dict["password"]) > 72:
            raise PasswordLengthError
        self._new_user_credential = new_user_dict

    def save_new_user(self):
        """Process new user credential and save them"""
        new_user_credential = self._new_user_credential
        username = new_user_credential.pop("username")
        del new_user_credential["password_repeat"], new_user_credential["register_key"]
        new_user_credential["password"] = Hasher.hash_string(self, string=new_user_credential["password"])
        self.credential_users[username] = new_user_credential
        self.save_yaml(self.credential_users)

        return


    