from functools import wraps
from flask  import session,redirect,url_for
from yummy_app.models import User

# check if user is logged in
def is_logged_in():
    if 'username' in session:
        return True
    return False

# return user for logged in user
def get_user() -> User:
    return User.query.filter_by(username=session['username']).first()

# check if user is admin
def is_admin():
    if 'username' in session:
        user = User.query.filter_by(username=session['username']).first()
        if user.is_admin:
            return True
    return False

#  login required decorator
# burda wraps basa dusmedim niye yazilir
def login_required(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'username' in session:
            return f(*args, **kwargs)
        else:
            return redirect(url_for('login'))
    return wrap
    
#  admin required decorator 
def admin_required(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if is_admin():
            return f(*args, **kwargs)
        else:
            return redirect(url_for('login'))
    return wrap

# logout user
def logout():
    session.pop('username', None)
    return redirect(url_for('login'))

# checkif user already exists
def user_exists(username):
    user = User.query.filter_by(username=username).first()
    if user:
        return True
    return False
    