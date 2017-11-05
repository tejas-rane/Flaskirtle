from flask import Flask, render_template, flash, redirect, url_for, session, logging, request
from data import Articles
from flask_mysqldb import MySQL
from wtforms import Form, StringField, TextAreaField, PasswordField, validators
from passlib.hash import sha256_crypt

app = Flask(__name__)

Articles = Articles()

# mysql
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'root'
app.config['MYSQL_DB'] = 'flaskirtle'
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'
# init MySQL
mysql = MySQL(app)


@app.route('/')
def hello_world():
    return render_template('home.html')


@app.route('/about')
def about():
    return render_template('about.html')


@app.route('/articles')
def articles():
    return render_template('articles.html', articles=Articles)


@app.route('/articleDetail/<string:id>')
def article_detail(id):
    return render_template('articleDetail.html', id=id)


class RegisterForm(Form):
    name = StringField('Name', [
        validators.Length(min=1, max=50)
    ])
    username = StringField('userame', [
        validators.Length(min=4, max=25)
    ])
    email = StringField('email', [
        validators.Length(min=6, max=50)
    ])
    password = PasswordField('password', [
        validators.DataRequired(),
        validators.equal_to('confirm', message='passwords do not match')
    ])
    confirm = PasswordField('confirm password')


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm(request.form)
    if request.method == 'POST' and form.validate():
        name = str(form.name.data)
        email = str(form.email.data)
        username = str(form.username.data)
        password = sha256_crypt.encrypt(str(form.password.data))
        print(name, username, email, password)
        # create cursor
        cur = mysql.connection.cursor()
        #query = "INSERT INTO users(name,username,email,password) VALUES{%s, %s, %s, %s}"
        cur.execute("INSERT INTO users(name,username,email,password) VALUES(%s, %s, %s, %s)", (name, username, email, password))

        # commit to db
        mysql.connection.commit()
        cur.close()
        flash('You are now registered and you can login', 'success')

        #return redirect(url_for('/home'))

        #return render_template('register.html')
    return render_template('register.html', form=form)


if __name__ == '__main__':
    app.secret_key = 'secret_key123'
    app.run(debug=True)
