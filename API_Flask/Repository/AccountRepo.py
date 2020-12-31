from Database.DB import session, Account


def get_account_by(username, input_password):
    account = session.query(Account).filter(Account.username == username).first()
    if account is None or not account.verify_password(input_password):
        return ""
    return account.id


def generate_auth_token(account_id, token_time_life, secrect_key):
    account = session.query(Account).get(account_id)
    return account.generate_auth_token(token_time_life, secrect_key)


def verify_auth_token(token, secret_key):
    return Account.verify_auth_token(token, secret_key)