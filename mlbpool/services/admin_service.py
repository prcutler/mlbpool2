from mlbpool.data.dbsession import DbSessionFactory
from mlbpool.data.account import Account


def admin_check():
    """Create a check that only the user who is True in the AccountInfo database with is_superuser can access
    the admin pages.  Make sure mlbpool/data/config.py has an email assigned that matches the user during
    registration"""
    session = DbSessionFactory.create_session()
    su__query = session.query(Account.id).filter(Account.is_super_user == 1) \
        .filter(Account.id == self.logged_in_user_id).first()
    print(su__query)

    if not su__query[0] == self.logged_in_user_id:
        print("You must be an administrator to view this page")
        self.redirect('/home')

    session.close()


class AccountService:
    @staticmethod
    def get_all_accounts():
        session = DbSessionFactory.create_session()
        account_list = session.query(Account).all()

        session.close()

        return account_list

    @classmethod
    def update_admin(cls, user_id: str):

        session = DbSessionFactory.create_session()

        for player in session.query(Account.id).filter(Account.id == user_id):
            session.query(Account.id).filter(Account.id == user_id).update({"is_super_user": 1})

        session.commit()
        session.close()

    @classmethod
    def update_paid(cls, user_id: str):

        session = DbSessionFactory.create_session()

        for player in session.query(Account.id).filter(Account.id == user_id):
            session.query(Account.id).filter(Account.id == user_id).update({"paid": 1})

        session.commit()
        session.close()

    @staticmethod
    def reset_paid():

        session = DbSessionFactory.create_session()

        for player in session.query(Account):
            session.query(Account.paid).update({"paid": 0})

        session.commit()
        session.close()

