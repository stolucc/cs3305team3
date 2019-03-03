from flask import Flask, flash, redirect, render_template, request, url_for, jsonify
from flask_login import current_user, login_required, login_user, LoginManager, logout_user#, UserMixin
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
# use and_()
from sqlalchemy import and_
from werkzeug.security import generate_password_hash#, check_password_hash
from functools import wraps
from flask_mail import Mail
from flask_wtf.csrf import CSRFProtect
from forms import AddGrantApplicationForm,ResetPasswordRequestForm, ResetPasswordForm, DeletionForm, RegistrationForm, AddProposalForm, ProfileForm, EducationForm, GeneralForm, AddOrcid
from dynamicforms import GrantLayAbstractForm, GrantScientificAbstractForm, GrantGeneralInfoForm, CoApplicantsForm, CollaboratorsForm
from flask_dropzone import Dropzone
import os
import requests
import xml.dom.minidom
import json
basedir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)

csrf = CSRFProtect(app)
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
app.config["SECRET_KEY"] = 'dev key'#os.environ.get('SECRET_KEY') or 'you-will-never-guess'

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
    DROPZONE_ENABLE_CSRF = True,
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

from models import Researcher_Profile, CFP, User, Grant_Application,SubmittedApplications,Collaborators,Co_Applicants #moved this
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
    if not current_user.is_authenticated:
        return redirect(url_for('login'))

    if request.method == "GET":
        return render_template("main_page.html", title="Home")
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
#@login_required_advanced(role="sfiAdmin")
def add_proposals():
    form = AddProposalForm(request.form)
    if request.method == 'POST' and form.validate():
        call=CFP(
            call_for_proposal_title=form.call_for_proposal_title.data,
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

        user = User(
            username=form.username.data,
            email=form.email.data,
            user_type=form.user_type.data,
            password_hash=generate_password_hash(form.password.data)
            )
        if form.user_type.data=="researcher":
            researcher = Researcher_Profile(username=form.username.data)
            researchers_education = Researcher_Education(username=form.username.data)
            db.session.add(researcher)
            db.session.add(researchers_education)

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
        for key, f in request.files.items():
            if key.startswith('file'):
                #save_as = f.filename + current_user.get_id()
                #directory = current_user.get_id()

                saved_as = str(current_user.get_id()) + f.filename
                f.save(os.path.join(app.config['UPLOADED_PATH'], saved_as))
                #application = Grant_Application.query.filter_by(grant_application_id=(request.form['grant_application_id'])).first()
                application = Grant_Application.query.filter_by(user_id=current_user.get_id()).first()
                application.set_programme_documents(os.path.join(app.config['UPLOADED_PATH'], saved_as))

    return render_template('drag_and_drop.html', title='Proposals', user=user)

@app.route('/user/<username>', methods=['GET', 'POST'])
#@login_required
#@login_required_advanced(role="researcher")
def user(username):
    user = User.query.filter_by(username=username).first_or_404()
    form = ProfileForm(request.form)
    if request.method == 'POST' and form.validate():
        pass
    return render_template('user.html', title='Profile', user=user, form=form)

@app.route('/user/add_orcid', methods=['GET', 'POST'])
#@login_required_advanced(role="sfiAdmin")
def add_orcid():
    form = AddOrcid(request.form)
    creditName = ""
    if request.method == 'POST' and form.validate():
        if form.orcid.data:

            orcidUrl = 'https://pub.orcid.org/v2.0/' + str(form.orcid.data)
            dom = xml.dom.minidom.parseString(requests.get(orcidUrl).text)
            eles = dom.documentElement
            person = eles.getElementsByTagName("person:name")
            for i in person:
                firstName = i.getElementsByTagName("personal-details:given-names")[0].firstChild.data
                lastName = i.getElementsByTagName("personal-details:family-name")[0].firstChild.data
                creditName = creditName + firstName + " " + lastName

            if current_user.user_type == "researcher":
                researcher = Researcher_Profile.query.filter_by(username=current_user.username).first()
                researcher.f_name = firstName
                researcher.l_name = lastName
                researcher.ORCID = form.orcid.data

            db.session.commit()

    return render_template('forms/add_orcid.html', title='Education', user=user, form=form, creditName=creditName)

@app.route('/user/education_form', methods=['GET', 'POST'])
#@login_required_advanced(role="sfiAdmin")
def education_form():
    form = EducationForm(request.form)
    if request.method == 'POST' and form.validate():
        pass
    return render_template('forms/education_form.html', title='Education', user=user, form=form)

@app.route('/user/general_form', methods=['GET', 'POST'])
#@login_required_advanced(role="sfiAdmin")
def general_form():
    form = GeneralForm(request.form)
    if request.method == 'POST' and form.validate():
        pass
    return render_template('forms/general_form.html', title='Education', user=user, form=form)


@app.route('/sample_button',methods=['GET','POST'])
@login_required
def press_button():#TESTER FUNCTION REMOVE AFTERWARDS
    if request.method == 'POST':
        call_for_proposal_title=request.form['sample']
        application = Grant_Application(
        user_id = current_user.get_id(), proposal_title=call_for_proposal_title)# = application_title)
        print("IN HEEERE")
        db.session.add(application)
        db.session.commit()
        return redirect(url_for('submit_application',application_id=application.grant_application_id))#Try to pass on the value in the button as well.

    return render_template('sample_button.html')

@app.route('/submit_application/<application_id>',methods=['GET','POST'])
@login_required
def submit_application(application_id):
    application = Grant_Application.query.filter_by(grant_application_id=application_id).first()
    co_applicant_instance= Co_Applicants(grant_application=application_id)
    collaborator_instance= Collaborators(grant_application=application_id)
    general_app_form = GrantGeneralInfoForm(request.form, obj=application)
    scientific_abstract_form = GrantScientificAbstractForm(request.form, obj=application)
    lay_abstract_form = GrantLayAbstractForm(request.form, obj=application)
    co_applicants_form = CoApplicantsForm(request.form, obj=co_applicant_instance)
    collaborators_form = CollaboratorsForm(request.form, obj=collaborator_instance)

    return render_template('grant_application.html', form1= general_app_form, form2 = scientific_abstract_form,
    form3 = lay_abstract_form, form5=co_applicants_form,  form6=collaborators_form)




@app.route('/add_application_general', methods=['POST'])#CHANGED USED TO HAVE GET AS WELL
@login_required
def add_application_general():
    general_app_form = GrantGeneralInfoForm()


    #return json.dumps({'status':'OK','proposal_title':request.form['award_duration'],'award_duration':request.form['proposal_title']});#Will have to change this.


    if general_app_form.validate_on_submit():
        application = Grant_Application.query.filter_by(grant_application_id=(request.form['grant_application_id'])).first()#MUST FILTER FOR CASE WHERE A RESEARCHER HAS MULTIPLE APPLICATIONS

        application.set_propsoal_title(request.form['proposal_title'])
        application.set_award_duration(request.form['award_duration'])
        application.set_national_research_priority(request.form['national_research_priority'])
        application.set_sfi_legal_remit_justification(request.form['sfi_legal_remit_justification'])
        application.set_ethical_issues(request.form['ethical_issues'])
        application.set_applicants_country(request.form['applicants_country'])
        db.session.add(application)
        db.session.commit()

        return json.dumps({'status':'OK','ethical_issues':'New addition'});
    else:
        return jsonify(data=general_app_form.errors)



@app.route('/add_scientific_abstract', methods=['POST'])
@login_required
def add_scientific_abstract():
    #return json.dumps({'status':'OK',"ETHICAL_ISSUES":request.form['ethical_issues']});
    #application = Grant_Application.query.filter_by(user_id=current_user.get_id()).first()
    #grant_id = request.form[],
    #application = Grant_Application.query.filter_by(grant_application_id=(request.form['grant_application_id'])).first()#MUST FILTER FOR CASE WHERE A RESEARCHER HAS MULTIPLE APPLICATIONS

    scientific_abstract_form = GrantScientificAbstractForm()



    if scientific_abstract_form.validate_on_submit():
        application = Grant_Application.query.filter_by(grant_application_id=(request.form['grant_application_id'])).first()#MUST FILTER FOR CASE WHERE A RESEARCHER HAS MULTIPLE APPLICATIONS
        application.set_scientific_abstract(request.form['scientific_abstract'])
        db.session.commit()
        return json.dumps({'status':'OK','ethical_issues':'New addition'});#Will have to change this.

    else:
        return jsonify(data=scientific_abstract_form.errors)#EXPAND AND GIVE PROPER ERROR MESSAGE

@app.route('/add_lay_abstract', methods=['POST'])
@login_required
def add_lay_abstract():
    #return json.dumps({'status':'OK'});
    #application = Grant_Application.query.filter_by(grant_application_id=(request.form['grant_application_id'])).first()#MUST FILTER FOR CASE WHERE A RESEARCHER HAS MULTIPLE APPLICATIONS
    lay_abstract_form = GrantLayAbstractForm()


    if lay_abstract_form.validate_on_submit():
        application = Grant_Application.query.filter_by(grant_application_id=(request.form['grant_application_id'])).first()#MUST FILTER FOR CASE WHERE A RESEARCHER HAS MULTIPLE APPLICATIONS

        application.set_lay_abstract(request.form['lay_abstract'])
        db.session.commit()
        return json.dumps({'status':'OK','ethical_issues':'New addition'});#Will have to change this.
    else:
        return jsonify(data=lay_abstract_form.errors)

@app.route('/Co_applicants_form1', methods=['POST'])
@login_required
def Co_applicants_form1():
    #Collaborators_form = CollaboratorsForm(request.form)
    co_app =CoApplicantsForm(request.form)

    if co_app.validate_on_submit():
        co_app = Co_Applicants(name=request.form['name'],organization=request.form['organization'],
        email=request.form['email'],grant_application=request.form['grant_application'])
        db.session.add(co_app)
        db.session.commit()
        return json.dumps({'status':'OK','ethical_issues':'New addition'});#Will have to change this.
    else:
        return jsonify(co_app.errors)

@app.route('/Collaborators_form1', methods=['POST'])
@login_required
def Collaborators_form1():
    #Collaborators_form = CollaboratorsForm(request.form)
    co_app =CollaboratorsForm(request.form)

    if co_app.validate_on_submit():
        co_app = Collaborators(name=request.form['name'],organization=request.form['organization'],
        email=request.form['email'],grant_application=request.form['grant_application'])
        db.session.add(co_app)
        db.session.commit()
        return json.dumps({'status':'OK','ethical_issues':'New addition'});#Will have to change this.
    else:
        return jsonify(co_app.errors)



@app.route('/submit_Form', methods=['POST'])
@login_required
def submit_Form():
    #return json.dumps({'status':'OK',"ETHICAL_ISSUES":request.form['ethical_issues']});
    return_string = ""

    application = Grant_Application.query.filter_by(grant_application_id=(request.form['grant_application_id'])).first()#MUST FILTER FOR CASE WHERE A RESEARCHER HAS MULTIPLE APPLICATIONS
    general_app_form = AddGrantApplicationForm(request.form, obj=application)
    if general_app_form.validate():
        new_Submitted=SubmittedApplications(grant_application_id=request.form['grant_application_id'],proposal_name=application.proposal_title)
        db.session.add(new_Submitted)
        db.session.commit()
        return json.dumps({'status':'OK','ethical_issues':'New addition'});#Will have to change this.
    else:
        return jsonify(data=general_app_form.errors)


    #db.session.commit()
    return json.dumps({'status':'OK','query:':return_string});



@app.route("/home")
def home():
    return render_template('home.html', title='Profile')


@app.route("/sample_slider")
def sample_slider():
    return render_template('sample_slider.html')

@app.route("/notifications")
def notifications():
    #grants=Grant_Application.query.all()
    grants = db.session.query(Grant_Application).count()
    calls= db.session.query(CFP).count()
    return render_template('notifications.html', title='Profile', user=user, grants=grants, calls=calls)




