from flask import Flask, redirect, url_for, render_template, request, session, flash
from flask_sqlalchemy import SQLAlchemy
import datetime


app = Flask(__name__)

app.config['SECRET_KEY'] = 'Python'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///movies.sqlite'
db = SQLAlchemy(app)


class Movies(db.Model):
    Name = db.Column(db.String(50), primary_key=True)
    Year = db.Column(db.INTEGER, nullable=False)
    Rating = db.Column(db.Float, nullable=False)

    def __str__(self):
        return f'name: {self.Name}, year: {self.Year}, rating: {self.Rating}'


@app.route('/')
@app.route('/home')
def home():
    all_movies = Movies.query.all()
    return render_template('index.html', all_movies=all_movies)


@app.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        up_letter, low_letter, digits, sp_ch = False, False, False, False
        username = request.form['username']
        password = request.form['password']
        if username == "" or password == "":
            flash("შეავსეთ ყველა ველი")
        else:
            if len(password) >= 8:
                for each in password:
                    if each.isupper():
                        up_letter = True
                    elif each.islower():
                        low_letter = True
                    elif each.isdigit():
                        digits = True
                    elif each in '!@#$%^&*()_+':
                        sp_ch = True
            else:
                flash("The length is insufficient")
        if up_letter and low_letter and digits and sp_ch:
            session['username'] = username
            return redirect(url_for('home'))
        else:
            flash('Please enter a password that contains upper and lower case letters as well as numbers and symbols.')
    return render_template('login.html')


@app.route('/user')
def user():
    now = datetime.datetime.now()
    time_string = now.strftime("%Y-%m-%d %H:%M:%S")
    template_data = {
        'title': 'HELLO!',
        'time': time_string
    }
    return render_template('user.html', template_data=template_data)






@app.route('/logout')
def logout():
    session.pop('username', None)
    return render_template('index.html')


@app.route('/movie', methods=['GET', 'POST'])
def movies():
    if request.method == 'POST':
        name = request.form['name']
        year = request.form['year']
        rating = request.form['rating']
        if name == "" or year == "" or rating == "":
            flash("შეავსეთ ყველა ველი")
        elif not rating.replace('.', '0').isnumeric():
            flash("რეიტინგი უნდა იყოს რიცხვითი მონაცემი")
        elif not year.isnumeric():
            flash("წელი უნდა იყოს რიცხვითი მონაცემი")
        else:
            b = Movies(Name=name, Year=year, Rating=rating)
            db.session.merge(b)
            db.session.commit()
            flash('მონაცემები დამატებულია')
    return render_template('movies.html')


if __name__ == "__main__":
    app.run(debug=True)