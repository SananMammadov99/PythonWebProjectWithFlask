from flask import Flask, redirect, request, render_template, session
import sqlite3


app = Flask(__name__)

app.secret_key = 'my_secret_key'

@app.get('/')
def hello():
    return redirect('/user/register')


@app.route('/user/register', methods=['POST', 'GET'])
def register_user():


    if session.get('is_logged_in'):
        return redirect('/user/profile' )
        
    if request.method == 'POST':
        _username = request.form['username']
        _password = request.form['password']
        conn = sqlite3.connect('worker.db')
        c = conn.cursor()
        c.execute(f"INSERT INTO worker(username,password) VALUES('{_username}', '{_password}')")
        _id = c.lastrowid
        conn.commit()
        conn.close()
        session['is_logged_in'] = True
        session['username'] = _username
        session['user_id'] = _id
        return redirect('/user/profile')

    elif request.method == 'GET':
        error = session.get('error')
        session['error'] = None
        return render_template('register.html', error=error)
        

@app.get('/user/profile')
def profile():
    if session.get('is_logged_in'):
        return render_template('profile.html', username=session['username'],id=session['user_id'])
    else:
        return redirect('/user/login')

@app.post('/user/delete/<id>')
def delete_user(id):
    conn = sqlite3.connect('worker.db')
    c = conn.cursor()
    c.execute(f"DELETE FROM worker WHERE id = {id}")
    conn.commit()
    conn.close()
    session.clear()
    session['error'] = 'User deleted'
    
    return redirect('/user/register')


@app.post('/user/update/<id>')
def update_user(id):
    conn = sqlite3.connect('worker.db')
    c = conn.cursor()
    c.execute(f"UPDATE worker SET username = '{request.form['username']}', password = '{request.form['password']}' WHERE id = {id}")
    conn.commit()
    conn.close()
    session['is_logged_in'] = False
    session['error'] = 'User updated successfully'
    return redirect('/user/login')

@app.get('/user/logout')
def logout():
    session.clear()
    return redirect('/user/login')


@app.route('/user/login', methods=['POST', 'GET'])
def login_user():
    if session.get('is_logged_in'):
        return redirect('/user/profile')
        
    if request.method == 'POST':
        _username = request.form['username']
        _password = request.form['password']
        conn = sqlite3.connect('worker.db')
        c = conn.cursor()
        c.execute(f"SELECT * FROM worker WHERE username = '{_username}' AND password = '{_password}'")
        user = c.fetchone()
        conn.close()
        if user:
            session['is_logged_in'] = True
            session['username'] = _username
            session['user_id'] = user[0]
            return redirect('/user/profile')
        else:
            session['error'] = 'Invalid username or password'
            return redirect('/user/login')
    
    if request.method == 'GET':
        error = session.get('error')
        session.clear()
        return render_template('login.html', error=error)

if __name__ == '__main__':
    app.run(debug=True)
