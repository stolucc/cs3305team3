from flask import Flask, flash, redirect, render_template, request, url_for
from flask_login import current_user, login_required, login_user, LoginManager, logout_user#, UserMixin
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash#, check_password_hash
from functools import wraps
from flask_mail import Mail
from forms import ResetPasswordRequestForm, ResetPasswordForm, DeletionForm, RegistrationForm, AddProposalForm, ProfileForm, EducationForm, GeneralForm
from flask_dropzone import Dropzone
import os
import requests
import xml.dom.minidom
basedir = os.path.abspath(os.path.dirname(__file__))

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
app.config["SECRET_KEY"] = os.environ.get('SECRET_KEY') or 'you-will-never-guess'

app.config.update(
    DEBUG=True,
    MAIL_SERVER='smtp.gmail.com',
    MAIL_PORT=587,
    MAIL_USE_TLS=1,
    MAIL_USERNAME = 'sfigroup3@gmail.com',
    MAIL_PASSWORD = 'sglarzpjdohssrpu',
    UPLOADED_PATH=os.path.join(basedir, 'uploads'),
    DROPZONE_ALLOWED_FILE_CUSTOM = True,
    DROPZONE_ALLOWED_FILE_TYPE = '.pdf, .txt',
    #DROPZONE_ENABLE_CSRF = True,
    DROPZONE_UPLOAD_ON_CLICK=True,
    )

mail = Mail(app)

from email1 import send_password_reset_email
dropzone = Dropzone(app)

db = SQLAlchemy(app)
migrate = Migrate(app, db)

app.secret_key = "ewlnzibewwlxshfkwmsi"
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

from models import Researcher_Profile, CFP, User #moved this
#Unused models SFIAdmin, Reviewer, Researcher_Account, Research_Centre_Admin, Login_Account, Engagements, Presentations, FundingRatio, TeamMembers, Impacts, Funding_Diversification, EmploymentDB, AwardsDB, Conferences, Publications, Professional_Socities, AcademicCollabs, NonAcademicCollabs, Communication, Innovations, AnnualReports, ResearcherEducation

def make_shell_context():
    return dict(app=app, db=db)

@login_manager.user_loader
def load_user(user_id):
    return User.query.filter_by(username=user_id).first()

def login_required_advanced(role="ANY"):
    def wrapper(fn):
        @wraps(fn)
        def decorated_view(*args, **kwargs):
            if not current_user.is_authenticated:#current_user.is_authenticated()
                return render_template("login_page.html", error=True)
            urole = current_user.get_user_type()
            if ( (urole != role) and (role != "ANY")):
                return render_template("login_page.html", error=True)
            return fn(*args, **kwargs)
        return decorated_view
    return wrapper


def getPasswordHash(password):
    return generate_password_hash(password)

"""
                ********************
    ****************** Routes *********************
                ********************
"""

@app.route("/")
@app.route("/index")
def index():
    dom = xml.dom.minidom.parseString(requests.get('https://pub.sandbox.orcid.org/v3.0_rc1/0000-0002-9227-8514').text)
    eles = dom.documentElement
    zmin = eles.getElementsByTagName("personal-details:credit-name")[0].firstChild.data
    if not current_user.is_authenticated:
        return redirect(url_for('login'))

    if request.method == "GET":
        return render_template("main_page.html", title="Home", zmin=zmin)
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

    urole=user.get_user_type()
    login_user(user)
    #urole=user.get_user_type()
    if urole=="sfiAdmin":
        return redirect(url_for('admin_main'))

    elif urole=="researcher":
        return redirect(url_for('index'))

    elif urole=="researchCentre":
        return redirect(url_for('research_centre_main'))

    elif urole=="reviewer":
        return redirect(url_for('reviewer_main'))

    else:#user=institution:
        return redirect(url_for('institute_main'))

@app.route("/logout/")
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

@app.route('/reset_password_request', methods=['GET', 'POST'])
def reset_password_request():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = ResetPasswordRequestForm(request.form)
    if request.method == 'POST' and form.validate():
        user = User.query.filter_by(email=form.email.data).first()
        if user:
            send_password_reset_email(user)
        flash('Check your email for the instructions to reset your password')
        return redirect(url_for('login'))
    return render_template('reset_password_request.html',
                           title='Reset Password', form=form)

@app.route('/reset_password<token>', methods=['GET', 'POST'])#was /reset_password)reset_password<token>
def reset_password(token):
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    user = User.verify_reset_password_token(token)
    if not user:
        return redirect(url_for('index'))
    form = ResetPasswordForm(request.form)
    if request.method == 'POST' and form.validate():
        user.set_password(form.password.data)
        db.session.commit()
        flash('Your password has been reset.')
        return redirect(url_for('login'))

    return render_template('reset_password.html', form=form)

@app.route('/add_proposals', methods=["GET", "POST"])
@login_required_advanced(role="sfiAdmin")
def add_proposals():
    form = AddProposalForm(request.form)
    if request.method == 'POST' and form.validate():
        call=CFP(
            text_of_call=form.text_of_call.data,
            target_audience=form.target_audience.data,
            eligibility_criteria=form.eligibility_criteria.data,
            duration_of_award=form.duration_of_award.data,
            reporting_guidelines=form.reporting_guidelines.data,
            start_date=form.start_date.data,
            deadline=form.deadline.data
        )
        db.session.add(call)
        db.session.commit()
        return redirect(url_for('proposals'))
    return render_template('add_proposals.html', title='Proposals', user=user, form=form)

@app.route('/proposals')
def proposals():
    calls=CFP.query.all()
    return render_template('call_for_proposals.html', title='Proposals', user=user, calls=calls)

@app.route('/submit_proposals')
#@login_required_advanced(role="sfiAdmin")
def submit_proposals():
    return render_template('submit_proposals.html', title='Proposals', user=user)

@app.route('/admin_main')
@login_required_advanced(role="sfiAdmin")
def admin_main():
    return render_template('admin_main_page.html', title='Proposals', user=current_user)

@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm(request.form)
    if request.method == 'POST' and form.validate():
        user = User(username=form.username.data, email=form.email.data, user_type=form.user_type.data,
                    password_hash=generate_password_hash(form.password.data))
        db.session.add(user)
        db.session.commit()
        flash('Thanks for registering')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)

@app.route('/delete_user', methods=['GET', 'POST'])
@login_required_advanced(role="sfiAdmin")
def delete_user():
    form = DeletionForm(request.form)
    users=User.query.all()
    if request.method == 'POST' and form.validate():
        User.query.filter(User.id == form.user_id.data).delete()
        db.session.commit()
        return redirect(url_for('delete_user'))
    return render_template('delete_user.html', title='Delete User', users=users, form=form)

@app.route('/research_centre_main')
@login_required_advanced(role="researchCentre")
def research_centre_main():
    return render_template('research_centre_main_page.html', title='Research Centre', user=current_user)

@app.route('/reviewer_main')
@login_required_advanced(role="reviewer")
def reviewer_main():
    return render_template('reviewer_main.html', title='Reviewer', user=current_user)

@app.route('/institute_main')
@login_required_advanced(role="institution")
def institute_main():
    return render_template('institute_main.html', title='Insititution', user=current_user)

@app.route('/upload', methods=['GET', 'POST'])
def upload():
    if request.method == 'POST':
            if key.startswith('file'):
                #save_as = f.filename + current_user.get_id()
                #directory = current_user.get_id()
                f.save(os.path.join(app.config['UPLOADED_PATH'], str(current_user.get_id())))
    return render_template('drag_and_drop.html', title='Proposals', user=user)

@app.route('/user/<username>', methods=['GET', 'POST'])
#@login_required
#@login_required_advanced(role="researcher")
def user(username):
    user = User.query.filter_by(username=username).first_or_404()
    form = ProfileForm(request.form)
    if request.method == 'POST' and form.validate():
        researcher = Researcher_Profile(ORCID=form.orcid.data)

    return render_template('user.html', title='Profile', user=user, form=form)

@app.route('/user/education_form', methods=['GET', 'POST'])
#@login_required_advanced(role="sfiAdmin")
def education_form():
    form = EducationForm(request.form)
    if request.method == 'POST' and form.validate():
        makeAssignment="makeAssignmentHere"
    return render_template('forms/education_form.html', title='Education', user=user, form=form)

@app.route('/user/general_form', methods=['GET', 'POST'])
#@login_required_advanced(role="sfiAdmin")
def general_form():
    form = GeneralForm(request.form)
    if request.method == 'POST' and form.validate():
        anotherEmptyAssignment="anotherEmptyAssignmentHere"
    return render_template('forms/general_form.html', title='Education', user=user, form=form)

@app.route("/home")
def home():
    return render_template('home.html', title='Profile')