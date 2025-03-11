# Exceptions for the Authenticator and Register class

# Authenticator
class UserNotExistError(Exception):
    """Error that username not exist"""
    def __init__(self):
        super().__init__("This username does not exist. Please try another username or sign up.")

class PasswordWrongError(Exception):
    """Error that passwords is incorrect"""
    def __init__(self):
        super().__init__("Your password is incorrect! Please check your input.")


# Register
class MissingFieldError(Exception):
    """Error that a filed is missing"""
    def __init__(self):
        super().__init__("All fields are required!")

class UserExistError(Exception):
    """Error that username already exist"""
    def __init__(self):
        super().__init__("This username already exists! Please try another username.")

class UserNameError(Exception):
    """Error that username contains an unallowed digit"""
    def __init__(self):
        super().__init__("the username contains the character: ' . Please use a different username.")

class RegisterKeyError(Exception):
    """Error that register key is wrong"""
    def __init__(self):
        super().__init__("The registration key is incorrect! Please contact the admin to get a registration key.")

class PasswordEqualError(Exception):
    """Error that passwords are not equal"""
    def __init__(self):
        super().__init__("Password and repeat password do not match! Please check your input.")
