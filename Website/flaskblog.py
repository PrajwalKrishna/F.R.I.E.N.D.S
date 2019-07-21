from flask import Flask, render_template, url_for, flash, redirect
from forms import UserForm
from auxilary_function import *

app = Flask(__name__)
app.config['SECRET_KEY'] = '5791628bb0b13ce0c676dfde280ba245'

app.arr = []

@app.route("/")
@app.route("/home", methods=['GET', 'POST'])
def home():
    form = UserForm()
    if form.validate_on_submit():
        flash('The results are shown below', 'success')
        app.arr = utilityFunction(form.username.data)
        return render_template('home.html', form=form,  array=app.arr)
    return render_template('home.html', form=form, array=app.arr)

if __name__ == '__main__':
    app.run(debug=True)
