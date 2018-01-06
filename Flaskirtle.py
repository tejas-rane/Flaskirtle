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
        return redirect(url_for('login'))
        #return redirect(url_for('/home'))

        #return render_template('register.html')
    return render_template('register.html', form=form)

#user login
@app.route('/login',methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        #get form fields
        username = request.form['username']
        password_candidate = request.form['password']

        #cur to verify
        cur = mysql.connection.cursor()

        result = cur.execute('SELECT * FROM users where username = %s',[username])

        if result > 0:
            data = cur.fetchone()
            password = data['password']
            # compare password
            if sha256_crypt.verify(password_candidate, password):
                app.logger.info('password matched')
                session['logged_in']= True
                session['username']=username
                flash('You are now logged in','success')
                return redirect(url_for('dashboard'))
            else:
                app.logger.info('password not matched')
                error = 'Invalid login'
                return render_template('login.html', error=error)
            cur.close
        else:
            app.logger.info('NO user')
            error = 'username not found'
            return render_template('login.html',error=error)
    return render_template('login.html')

@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html')
if __name__ == '__main__':
    app.secret_key = 'secret_key123'
    app.run(debug=True)
