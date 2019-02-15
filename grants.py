from datetime import datetime
from flask import Flask, redirect, render_template, request, url_for
from flask_login import current_user, login_required, login_user, LoginManager, logout_user, UserMixin
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import check_password_hash

app = Flask(__name__)
app.config["DEBUG"] = True

SQLALCHEMY_DATABASE_URI = "mysql+mysqlconnector://{username}:{password}@{hostname}/{databasename}".format(
    username="cs3305team3",
    password="team3pass",
    hostname="cs3305team3.mysql.pythonanywhere-services.com",
    databasename="cs3305team3$comments",
)
app.config["SQLALCHEMY_DATABASE_URI"] = SQLALCHEMY_DATABASE_URI
app.config["SQLALCHEMY_POOL_RECYCLE"] = 299
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)
migrate = Migrate(app, db)

app.secret_key = "ewlnzibewwlxshfkwmsi"
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

@login_manager.user_loader
def load_user(user_id):
    return User.query.filter_by(username=user_id).first()

"""
    ** Database Tables **
"""

class SFIAdmin(UserMixin, db.Model):

    __tablename__ = "sfiAdmin"

    sfi_admin_id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(128))
    password_hash = db.Column(db.String(128))

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def get_id(self):
        return self.username

class Reviewer(UserMixin, db.Model):

    __tablename__ = "reviewer"

    reviewer_id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(128))
    password_hash = db.Column(db.String(128))
    email = db.Column(db.String(80))

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def get_id(self):
        return self.username

class Researcher_Account(UserMixin, db.Model):

    __tablename__ = "researcher_account"

    researcher_id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(128))
    password_hash = db.Column(db.String(128))


    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def get_id(self):
        return self.username

class Research_Centre_Admin(UserMixin, db.Model):

    __tablename__ = "research_centre_admin"

    research_centre_id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(128))
    password_hash = db.Column(db.String(128))
    research_profile = db.Column(db.Integer)
    online = db.Column(db.BOOLEAN)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def get_id(self):
        return self.username

class Researcher_Profile(UserMixin, db.Model):

    __tablename__ = "researcher_profile"

    researcher_id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(128))
    password_hash = db.Column(db.String(128))
    f_name = db.Column(db.String(64))
    l_name = db.Column(db.String(64))
    job_title = db.Column(db.String(4))
    email = db.Column(db.String(80))
    ORCID = db.Column(db.Integer)
    login_id = db.Column(db.Integer)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def get_id(self):
        return self.username

class Login_Account(UserMixin, db.Model):

    __tablename__ = "login_account"

    login_account_id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(128))
    password_hash = db.Column(db.String(128))
    user_type = db.Column(db.String(128))

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def get_id(self):
        return self.username

class User(UserMixin, db.Model):

    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(128))
    password_hash = db.Column(db.String(128))

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def get_id(self):
        return self.username

"""
    ** Routes **
"""

@app.route("/")
@app.route("/index")
@login_required
def index():
    if not current_user.is_authenticated:
        return redirect(url_for('login'))

    if request.method == "GET":
        return render_template("main_page.html", title="Home", comments=Comment.query.all())

    comment = Comment(content=request.form["contents"], commenter=current_user)
    db.session.add(comment)
    db.session.commit()
    return redirect(url_for('index'))

@app.route("/login/", methods=["GET", "POST"])
def login():
    if request.method == "GET":
        return render_template("login_page.html", error=False)

    user = load_user(request.form["username"])
    if user is None:
        return render_template("login_page.html", error=True)

    if not user.check_password(request.form["password"]):
        return render_template("login_page.html", error=True)

    login_user(user)
    return redirect(url_for('index'))

@app.route("/logout/")
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

@app.route('/user/<username>')
@login_required
def user(username):
    user = User.query.filter_by(username=username).first_or_404()
    return render_template('user.html', title='Profile', user=user)

@app.route('/user_edit/<username>', methods=['GET', 'POST'])
@login_required
def user_edit(username):
    user = User.query.filter_by(username=username).first_or_404()
    return render_template('user_edit.html', title='Edit Profile', user=user)

@app.route('/edit_profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
    return render_template('edit_profile.html', title='Edit Profile')

"""
    ** Redundant Class **
"""

class Comment(db.Model):

    __tablename__ = "comments"

    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(4096))
    posted = db.Column(db.DateTime, default=datetime.now)
    commenter_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)
    commenter = db.relationship('User', foreign_keys=commenter_id)