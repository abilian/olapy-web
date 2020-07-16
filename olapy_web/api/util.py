from flask_login import current_user


def get_current_user():
    """# todo temporary until authentication with vue.

    :return:
    """
    user = current_user  # use this in prod
    # user = User.query.first()  # use this in dev
    return user
