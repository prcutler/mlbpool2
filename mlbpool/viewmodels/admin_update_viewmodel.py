from mlbpool.viewmodels.viewmodelbase import ViewModelBase


class AdminViewModel(ViewModelBase):
    def __init__(self):
        self.new_admin = None
        self.is_super_user = None

    def from_dict(self, data_dict):
        self.new_admin = data_dict.get('new_admin')
        self.is_super_user = data_dict.get('is_super_user')

