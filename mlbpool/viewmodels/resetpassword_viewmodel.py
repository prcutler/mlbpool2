import datetime
from mlbpool.services.account_service import AccountService
from mlbpool.viewmodels.viewmodelbase import ViewModelBase


class ResetPasswordViewModel(ViewModelBase):
    def __init__(self):
        self.reset_code = None
        self.reset = None
        self.error_msg = None
        self.message = None
        self.password = None
        self.is_get = True

    def from_dict(self, data_dict):
        # reset_code will be third part of URL:
        #      /account/reset_password/f8489375729a
        # that is always id in our routing scheme
        self.reset_code = data_dict.get('id')

        self.password = data_dict.get('password')
        if self.reset_code:
            self.reset = AccountService.find_reset_code(self.reset_code)

    def validate(self):
        self.error_msg = None

        symbol = ['!', '@', '#', '$', '%', '^', '&', '*', '(', ')', '-', '_', '+', '=', ',', '.', '<', '>'
                  '?', "/"]

        if not self.reset:
            self.error_msg = "Reset code not found"
            return

        if not self.is_get:
            if not (self.password or self.password.strip()):
                self.error_msg = 'You must enter a valid password'
                return
            if len(self.password) < 7:
                self.error_msg = 'You must enter a password with at least eight characters'
                return
            if len(self.password) >= 24:
                self.error = 'Your password must be 24 characters or less'

            if not any(char in symbol for char in self.password):
                self.error = 'Your password should have at least one of the symbol (!, @, #, $, %, ^, &, *, (, ), _, -, '' \
                ''=, +, ,, <, ., >, /, ?)'

            if not any(char.isdigit() for char in self.password):
                self.error = 'Your password have at least one number'

            if not any(char.isupper() for char in self.password):
                self.error = 'Your password should have at least one uppercase letter'

            if not any(char.islower() for char in self.password):
                self.error = 'Your password should have at least one lowercase letter'

        if self.reset.was_used:
            self.error_msg = 'This reset code has already been used.'
            return

        if self.reset.was_used:
            self.error_msg = 'This reset code has already been used.'
            return

        dt = datetime.datetime.now() - self.reset.created_date
        days = dt.total_seconds() / 60 / 60 / 24
        if days > 1:
            self.error_msg = 'This reset code has expired, generate a new one.'
            return
