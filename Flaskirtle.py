from flask import Flask, render_template, flash,redirect, url_for, session, logging,request
from data import Articles
from flask_mysqldb import MySQL
from wtforms import Form,StringField, TextAreaField, PasswordField, validators
from passlib.hash import sha256_crypt
app = Flask(__name__)

Articles = Articles()


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
        validators.input_required(),
        validators.Length(min=1,max=50)
    ])
    username  = StringField('userame',[
        validators.input_required(),
        validators.Length(min=4,max=25)
    ])
    email = StringField('email',[
        validators.input_required(),
        validators.Length(min=6, max=50)
    ])
    password = PasswordField('password', [
        validators.data_required(),
        validators.equal_to('confirm',  message='passwords do not match')
    ])
    confirm = PasswordField('confirm password')


@app.route('/register',methods=['GET', 'POST'])
def register():
    form = RegisterForm(request.form)
    if request.method== 'POST' and form.validate():
        return render_template( 'register.html')
    return render_template( 'register.html', form = form)

if __name__ == '__main__':
    app.run(debug=True)
