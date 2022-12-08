import sqlite3
from flask import Flask, request, redirect, url_for, render_template, session, send_file
import pdfkit


def connect_db():
    """Соединяет с указанной базой данных."""
    rv = sqlite3.connect('users.db')  # внутри конфигураций надо будет указать БД, в которую мы будем все хранить
    rv.row_factory = sqlite3.Row  # инстанс для итерации по строчкам (может брать по строке и выдавать)
    return rv


app = Flask(__name__)
app.secret_key = 'abacaba'


@app.route('/', methods=['GET'])
def start_page():
    return redirect(url_for('login_page'))


@app.route('/login', methods=['GET'])
def login_page():
    success = request.args.get('success')
    return render_template('main.html', success=success)


@app.route('/resume', methods=['GET'])
def resume_page():
    if not session.get('logged_in', False):
        return redirect(url_for('login_page'))
    return render_template('resume.html')


@app.route('/register', methods=['GET', 'POST'])
def register_page():
    success = request.args.get('success')
    return render_template('register.html', success=success)


@app.route('/lookup', methods=['POST'])
def lookup():
    if request.method == 'POST':
        db = connect_db()
        cur = db.cursor()
        cur.execute("select count(*) from users where login = ?", (request.form['login'],))
        data = cur.fetchone()[0]
        if data == 0:
            cur.execute("insert into users (email, name, login, password) values (?, ?, ?, ?)",
                        (f'{request.form["email"]}', f'{request.form["name"]}', f'{request.form["login"]}',
                         f'{request.form["password"]}')
                        )
            db.commit()
            db.close()
        else:
            return redirect(url_for('register_page', success=False))
    return redirect('http://localhost:5000')


@app.route('/validate', methods=["POST"])
def validate():
    if request.method == 'POST':
        db = connect_db()
        cur = db.cursor()
        cur.execute("select count(*) from users where login = ?", (request.form['login'],))
        data = cur.fetchone()[0]
        if data == 0:
            return redirect(url_for('login_page', success='False'))
        else:
            login = request.form['login']
            password = request.form['password']
            cur.execute(f"select login, password from users where login = '{login}' and password = '{password}'")
            db.commit()
            if not cur.fetchone():
                return redirect(url_for('login_page', success='not_found'))
            else:
                session['logged_in'] = True
                return redirect(url_for('resume_page'))


@app.route('/compiled_pdf', methods=['GET', 'POST'])
def compiled_pdf():
    arguments = request.form
    return render_template('template.html', args=arguments)


@app.route('/logout')
def logout():
    session['logged_in'] = False
    return redirect(url_for('login_page'))


@app.route('/supersecretpage', methods=['GET'])
def show_data():
    db = connect_db()
    users = db.execute('select * from users').fetchall()
    db.close()
    return render_template('show_db.html', users=users)


if __name__ == '__main__':
    app.run(host='localhost', debug=True)
