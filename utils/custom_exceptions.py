class EmailValueException(Exception):
    def __init__(self, message='Incorrect email format.'):
        super().__init__(message)

class PhoneValueException(Exception):
    def __init__(self, message='Phone number should be 10 digits!'):
        super().__init__(message)

class BirthdayPeriodException(Exception):
    def __init__(self, message='The "days" parameter must be an integer.'):
        super().__init__(message)

class BirthdayFormatException(Exception):
    def __init__(self, expected_format: str = None, message: str = 'Incorrect birthday format!'):
        if expected_format:
            message = f'Birthday format should be {expected_format}'
        super().__init__(message)

class UserNotExistException(Exception):
    def __init__(self, message='❌ Contact does not exist', user_name = ""):
        if user_name:
            message = f'❌ Contact with name: {user_name} does not exist'
        super().__init__(message)