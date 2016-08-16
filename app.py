from flask import Flask, render_template, request, make_response, flash
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////tmp/test.db'

db = SQLAlchemy(app)

challenges = db.Table('challenges',
    db.Column('challenge_id', db.Integer, db.ForeignKey('tag.id')),
    db.Column('user_id', db.Integer, db.ForeignKey('user.id'))
)

class Challenge(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100))
    description = db.Column(db.String(256))
    key = db.Column(db.String(50))

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), unique=True)
    challenges = db.relationship('Challenge', secondary=challenges, backref=db.backref('solvers', lazy='dynamic'))


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        # process the form here
        username = request.form['username']
        key = request.form['key']

        # check if user exists in the system
        usr = User.query.filter_by(email=username).first()
        if usr is None:
            # error
            flash("Email is not registered with the system")
        else:
            # check if key exists in the system
            challenge = Challenge.query.filter_by(key=key).first()
            if challenge is None:
                flash("Invalid key")
            else:
                # add a new key entry for this user to the database
                user.challenges.add(challenge)
                db.session.add(user)
                db.session.commit()

                flash("Congratulations! The key was added to your account")

    return render_template("index.html")

if __name__ == '__main__':
    app.run(debug=True, port=8000)    
