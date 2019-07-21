from flask import Flask, render_template, url_for, flash, redirect
from forms import UserForm
from func import *

app = Flask(__name__)
app.config['SECRET_KEY'] = '5791628bb0b13ce0c676dfde280ba245'

app.arr = []

@app.route("/")
@app.route("/home")
def home():
    return render_template('home.html', array=app.arr)


@app.route("/login", methods=['GET', 'POST'])
def login():
    form = UserForm()
    if form.validate_on_submit():
        flash('The results are shown below', 'success')
        app.arr = test(form.username.data)
        return redirect(url_for('home'))
    return render_template('login.html', title='Login', form=form)

if __name__ == '__main__':
    app.run(debug=True)
