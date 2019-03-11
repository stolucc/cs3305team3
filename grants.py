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
from forms import AddGrantApplicationForm,ResetPasswordRequestForm, ResetPasswordForm, DeletionForm, RegistrationForm, AddProposalForm, ProfileForm, EducationForm, EducationFormAdd, GeneralForm, AddOrcid, RegisterForm, GeneralUpdateForm, TeamMembersForm, EmploymentForm, ProfessionalSocietiesForm, AwardsForm, FundingDiversificationForm, ImpactsForm, InnovationsForm, PublicationsForm, PresentationsForm, AcademicCollabForm, NonAcademicCollabForm, ConferencesForm,CommunicationForm,FundingRatioForm,EngagementsForm
from dynamicforms import GrantLayAbstractForm, GrantScientificAbstractForm, GrantGeneralInfoForm, CoApplicantsForm, CollaboratorsForm
from flask_dropzone import Dropzone
import os
import requests
import xml.dom.minidom
import json
basedir = os.path.abspath(os.path.dirname(__file__))
from datetime import datetime

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

from email1 import send_password_reset_email, send_grant_accepted, send_grant_rejected, notify_of_reviewer_response
dropzone = Dropzone(app)

db = SQLAlchemy(app)
migrate = Migrate(app, db)

app.secret_key = "ewlnzibewwlxshfkwmsi"
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

from models import Researcher_Profile, CFP, User, Grant_Application,SubmittedApplications,Collaborators,Co_Applicants, ResearcherEducation, EmploymentDB, ProposalsAccepted, Engagements, AcademicCollabs, NonAcademicCollabs,Publications, FundingRatio, Conferences, Communication, Professional_Societies, TeamMembers, AwardsDB, Funding_Diversification, Impacts, Innovations, Presentations  #moved this

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
        return render_template("main_page.html", title="Home", user=current_user)
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

    elif urole=="institution":
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

@app.route('/reset_password)<token>', methods=['GET', 'POST'])#was /reset_password)reset_password<token>#Changed to reset_password<token>
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

@app.route('/proposals',methods=['GET', 'POST'])
def proposals():
    calls=CFP.query.all()
    date=datetime.now()
    if request.method == 'POST':
        call_for_proposal_title=request.form['grant_id']
        application = Grant_Application(
        user_id = current_user.id, proposal_title=call_for_proposal_title)
        db.session.add(application)
        db.session.commit()
        return redirect(url_for('submit_application',application_id=application.grant_application_id))#
    return render_template('call_for_proposals.html', title='Proposals', user=user, date=date, calls=calls)


@app.route("/proposals1")
def proposals1():
    date=datetime.now()
    calls=CFP.query.all()
    return render_template('call_for_proposals1.html', title='Proposals', user=user, date=date, calls=calls)

@app.route('/submit_proposals')
#@login_required_advanced(role="sfiAdmin")
def submit_proposals():
    return render_template('submit_proposals.html', title='Proposals', user=user)

# Redirects to the main page for an SFI admin when they log in
@app.route('/admin_main')
@login_required_advanced(role="sfiAdmin")
def admin_main():
    return render_template('admin_main_page.html', title='Admin Main Page', user=current_user)

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
            researchers_education = ResearcherEducation(username=form.username.data)
            db.session.add(researcher)
            db.session.add(researchers_education)
        db.session.add(user)
        db.session.commit()
        flash('Thanks for registering')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)

@app.route('/registration', methods=['GET', 'POST'])
def registration():
    form = RegisterForm(request.form)
    if request.method == 'POST' and form.validate():

        user = User(
            username=form.username.data,
            email=form.email.data,
            user_type="researcher",
            password_hash=generate_password_hash(form.password.data)
            )

        db.session.add(user)
        db.session.commit()
        flash('Thanks for registering')
        return redirect(url_for('login'))
    return render_template('registration.html', title='Register', form=form)

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

# Redirects to the main page for a research centre when they log in
@app.route('/research_centre_main')
@login_required_advanced(role="researchCentre")
def research_centre_main():
    return render_template('research_centre_main_page.html', title='Research Centre', user=current_user)

# Redirects to the main page for a reviewer when they log in
@app.route('/reviewer_main')
@login_required_advanced(role="reviewer")
def reviewer_main():
    return render_template('reviewer_main.html', title='Reviewer', user=current_user)

# Redirects to the main page for an institution when they log in
@app.route('/institute_main')
@login_required_advanced(role="institution")
def institute_main():
    return render_template('institute_main.html', title='Insititution', user=current_user)

@app.route('/upload', methods=['GET', 'POST'])
def upload():
    for key, f in request.files.items():
        flash('IN SECOND LOOP')
        saved_as = str(current_user.id) + str(f.filename)
        application = Grant_Application.query.filter_by(user_id=current_user.id).first()
        application.programme_documents = str(saved_as) # url_for('uploaded_file', filename=saved_as)
        db.session.commit()
        f.save(os.path.join(app.config['UPLOADED_PATH'], saved_as))
    return "uploading"

@app.route('/user/<username>', methods=['GET', 'POST'])
def user(username):
    user = User.query.filter_by(username=username).first_or_404()
    form = ProfileForm(request.form)
    if request.method == 'POST' and form.validate():
        pass
    return render_template('user.html', title='Profile', user=user, form=form)

@app.route('/user/add_orcid', methods=['GET', 'POST'])
@login_required#_advanced#(role="sfiAdmin")
def add_orcid():
    form = AddOrcid(request.form)
    creditName = ""
    output=""
    if request.method == 'POST' and form.validate():
        if form.orcid.data:


            """ ******ORCID IMPLEMENTATION START******** """
            orcidUrl = 'https://pub.orcid.org/v2.0/' + str(form.orcid.data)
            dom = xml.dom.minidom.parseString(requests.get(orcidUrl).text)
            eles = dom.documentElement
            person = eles.getElementsByTagName("person:name")

            #NAME
            for i in person:
                firstName = i.getElementsByTagName("personal-details:given-names")[0].firstChild.data #Gets First Name
                lastName = i.getElementsByTagName("personal-details:family-name")[0].firstChild.data #Gets Last Name
                creditName = creditName + firstName + " " + lastName #Gets full name
                output = "ORCID entered of: " + creditName


            #Create an
            application = Researcher_Profile.query.filter_by(users=current_user.id).first()#MUST FILTER FOR CASE WHERE A RESEARCHER HAS MULTIPLE APPLICATIONS

            if application:
                application.f_name = firstName
                application.l_name = lastName

            if not application:
                profile=Researcher_Profile(
                        f_name=firstName,
                        l_name=lastName,
                        users=current_user.id
                    )
                db.session.add(profile)
            db.session.commit()

            #EDUCATION
            educations = eles.getElementsByTagName("activities:educations")
            for education in educations:
                degree_title = education.getElementsByTagName("education:role-title")[0].firstChild.data #e.g. "PhD"
                fieldofstudy = education.getElementsByTagName("education:department-name")[0].firstChild.data #e.g. "Computer Science"
                institution = education.getElementsByTagName("common:name")[0].firstChild.data #e.g. "University of Limerick"
                city = education.getElementsByTagName("common:city")[0].firstChild.data
                country = education.getElementsByTagName("common:country")[0].firstChild.data
                location = (city + ", " + country) #Location
                awardyear = education.getElementsByTagName("common:year")[1].firstChild.data #Year degree awarded

            education = ResearcherEducation.query.filter_by(users=current_user.id).first()#MUST FILTER FOR CASE WHERE A RESEARCHER HAS MULTIPLE APPLICATIONS

            if education:
                education.field_of_study = fieldofstudy,
                education.degree = degree_title

            if not education:
                profile=ResearcherEducation(
                        field_of_study = fieldofstudy,
                        degree = degree_title,
                        users=current_user.id
                    )
                db.session.add(profile)
            db.session.commit()

            #EMPLOYMENT
            employments = eles.getElementsByTagName("activities:employments")
            for employment in employments:
                company = employment.getElementsByTagName("common:name")[0].firstChild.data #e.g. "University College Cork"
                employcity = employment.getElementsByTagName("common:city")[0].firstChild.data
                employcountry = employment.getElementsByTagName("common:country")[0].firstChild.data
                location = (employcity + ", " + employcountry) #e.g. "Cork, IE"
                employyear = employment.getElementsByTagName("common:year")[0].firstChild.data
                employmonth = employment.getElementsByTagName("common:month")[0].firstChild.data
                employday = employment.getElementsByTagName("common:day")[0].firstChild.data
                start_date = (employyear + "-" + employmonth + "-" + employday) #e.g. "2017-09-01"

            #PUBLICATIONS
            publications = eles.getElementsByTagName("activities:group")
            for pub in publications:
                title = pub.getElementsByTagName("common:title")[0].firstChild.data #publication title
                type = pub.getElementsByTagName("work:type")[0].firstChild.data #publication type
                try:
                    year = pub.getElementsByTagName("common:year")[0].firstChild.data       #publication year if there is one
                except:
                    pass
                try:
                    doiNull = pub.getElementsByTagName("common:external-id-value")[0].firstChild.data
                except IndexError:
                    pass #Remove this
                    #print("\n" + year + "\n" + type + "\n" + title + "\n" + "No doi value here!!!") Add assignements here for publication with no doi
                pubtypes= pub.getElementsByTagName("common:external-ids")
                doi = " "
                for pubtype in pubtypes:
                    pub1s = pubtype.getElementsByTagName("common:external-id")
                    for pub1 in pub1s:
                        type1 = pub1.getElementsByTagName("common:external-id-type")[0].firstChild.data
                        if type1 == 'doi' and doi != pub1.getElementsByTagName("common:external-id-value")[0].firstChild.data:
                            doi = pub1.getElementsByTagName("common:external-id-value")[0].firstChild.data      #publication doi if there is one
                            pass #Remove this
                            #print("\n" + year + "\n" + type + "\n" + title + "\n" + doi) Add assignements here for publication with no doi
                            type1 = ""
                            break
                        elif type1 == "eid":
                            break

            """ ******ORCID IMPLEMENTATION END******** """

            if current_user.user_type == "researcher":
                researcher_check = Researcher_Profile.query.filter_by(users=current_user.id).first()
                if researcher_check == None:
                    researcher=Researcher_Profile(
                        f_name = firstName,
                        l_name = lastName,
                        ORCID = form.orcid.data
                    )
                    db.session.add(researcher)
                    db.session.commit()
                #researcher.f_name = firstName
                #researcher.l_name = lastName
                #researcher.ORCID = form.orcid.data


    return render_template('forms/add_orcid.html', title='Education', user=user, form=form, output=output)

# Allows a researcher to add their education, update their education, and view their education
@app.route('/user/education_form', methods=['GET', 'POST'])
@login_required#_advanced#role="sfiAdmin")
def education_form():
    data=ResearcherEducation.query.filter_by(users=current_user.id).first()
    if data:
        form = EducationForm(request.form,obj=data)
        profile_exists=True;
    else:
        form = EducationForm(request.form)
        profile_exists=False;

    if request.method == 'POST' and form.validate():
        if data == None:
            education=ResearcherEducation(
                field_of_study=request.form['field_of_study'],
                degree=request.form['degree'],
                institution=request.form['institution'],
                year_of_degree=request.form['year_of_degree'],
                users= current_user.id,
                location=request.form['location']

                )
            db.session.add(education)
        else:
            data.field_of_study=request.form['field_of_study']
            data.degree=request.form['degree']
            data.institution=request.form['institution']
            data.year_of_degree=request.form['year_of_degree']
            data.location=request.form['location']
        db.session.commit()
    return render_template('forms/education_form.html', title='Education', user=current_user.id, form=form, profile_exists=profile_exists )

"""
@app.route('/user/education_form_add', methods=['GET', 'POST'])
#@login_required_advanced(role="sfiAdmin")
def education_form_add():
    form = EducationFormAdd(request.form)
    if request.method == 'POST' and form.validate():
        education=ResearcherEducation(
            field_of_study=form.field_of_study.data,
            degree=form.degree.data,
            institution=form.institution.data,
            year_of_degree=form.year_of_degree.data,
            location=form.location.data,
            users=current_user.id
        )
        db.session.add(education)
        db.session.commit()
        return redirect(url_for('education_form'))
    return render_template('forms/education_form.html', title='Education', user=current_user.id, form=form)"""

# Allows a researcher to add their general information, update their general information, and view their general information
@app.route('/user/general_form', methods=['GET', 'POST'])
#@login_required_advanced(role="sfiAdmin")
def general_form():
    #Displays the info from the database.
    data=Researcher_Profile.query.filter_by(users=current_user.id).first()
    if data:
        form = GeneralForm(request.form,obj=data)
        profile_exists = True;
    else:
        form = GeneralForm(request.form)
        profile_exists = False;

    if request.method == 'POST' and form.validate():
        if data == None:
            profile=Researcher_Profile(
                    f_name= request.form['f_name'],
                    l_name= request.form['l_name'],
                    job_title = request.form['job_title'],
                    prefix = request.form['prefix'],
                    suffix = request.form['suffix'],
                    phone = request.form['phone'],
                    users= current_user.id,
                    phone_extension = request.form['phone_extension']
                )
            db.session.add(profile)
        else:
            data.f_name= request.form['f_name']
            data.l_name= request.form['l_name']
            data.job_title = request.form['job_title']
            data.prefix = request.form['prefix']
            data.suffix = request.form['suffix']
            data.phone = request.form['phone']
            data.phone_extension = request.form['phone_extension']
        db.session.commit()
        #return redirect(url_for('/general_form'))
    return render_template('forms/general_form.html', title='General info', profile_exists= profile_exists, user=current_user.id , form=form)

# Allows a researcher to add their employment, update their employment, and view their employment
@app.route('/user/employment_form', methods=['GET', 'POST'])
#@login_required_advanced(role="sfiAdmin")
def employment_form():
    data=EmploymentDB.query.filter_by(users=current_user.id).first()
    if data:
        form = EmploymentForm(request.form,obj=data)
        profile_exists=True
    else:
        form = EmploymentForm(request.form)
        profile_exists=False
    if request.method == 'POST' and form.validate():
        if data==None:
            employment=EmploymentDB(
                institution=request.form['institution'],
                location=request.form['location'],
                year=request.form['year'],
                users=current_user.id
            )
            db.session.add(employment)
        else:
            data.institution=request.form['institution']
            data.location=request.form['location']
            data.year=request.form['year']
        db.session.commit()
    return render_template('forms/employment_form.html', title='Employment',  form=form, profile_exists=profile_exists, user=current_user.id )

# Allows a researcher to add their engagements, update their engagements, and view their engagements
@app.route('/user/engagements_form', methods=['GET', 'POST'])
#@login_required_advanced(role="sfiAdmin")
def engagements_form():
    data=Engagements.query.filter_by(users=current_user.id).first()
    if data:
        form = EngagementsForm(request.form,obj=data)
        profile_exists=True
    else:
        form=EngagementsForm(request.form)
        profile_exists=False
    if request.method == 'POST' and form.validate():
        if data==None:
            engagements=Engagements(
                start_date=request.form['start_date'],
                end_date=request.form['end_date'],
                project_name=request.form['project_name'],
                project_topic=request.form['project_topic'],
                activity_type=request.form['activity_type'],
                target_area=request.form['target_area'],
                users=current_user.id
            )
            db.session.add(engagements)
        else:
            data.start_date=request.form['start_date']
            data.end_date=request.form['end_date']
            data.project_name=request.form['project_name']
            data.project_topic=request.form['project_topic']
            data.activity_type=request.form['activity_type']
            data.target_area=request.form['target_area']
        db.session.commit()
    return render_template('forms/engagements_form.html', title='Engagements', form=form, profile_exists=profile_exists, user=current_user.id)

"""
@app.route('/user/employment_form_add', methods=['GET', 'POST'])
#@login_required_advanced(role="sfiAdmin")
def employment_form_add():
    form = EmploymentForm(request.form)
    if request.method == 'POST' and form.validate():
        employment=EmploymentDB(
            institution=form.institution.data,
            location=form.location.data,
            year=form.year.data,
            users=current_user.id
        )
        db.session.add(employment)
        db.session.commit()
        return redirect(url_for('employment_form'))
    return render_template('forms/employment_form.html', title='Employment', user=current_user.id, form=form)"""

@app.route('/user/team_members_form', methods=['GET', 'POST'])
#@login_required_advanced(role="sfiAdmin")
def team_members_form():
    data=TeamMembers.query.filter_by(users=current_user.id).first()
    if data:
        form = TeamMembersForm(request.form,obj=data)
        profile_exists=True
    else:
        form= TeamMembersForm(request.form)
        profile_exists=False

    if request.method == 'POST' and form.validate():
        if data==None:
            team_member=TeamMembers(
                start_date=request.form['start_date'],
                departure_date=request.form['departure_date'],
                name=request.form['name'],
                position=request.form['position'],
                users=current_user.id
                )
            db.session.add(team_member)
        else:
            data.start_date=request.form['start_date']
            data.departure_date=request.form['departure_date']
            data.name=request.form['name']
            data.position=request.form['position']
        db.session.commit()
    return render_template('forms/team_members_form.html', title='Team-Members', user=current_user.id, form=form, profile_exists= profile_exists)

# Allows a researcher to add their professional societies, update their professional societies, and view their professional societies
@app.route('/user/professional_societies_form', methods=['GET', 'POST'])
#@login_required_advanced(role="sfiAdmin")
def professional_societies_form():
    data=Professional_Societies.query.filter_by(users=current_user.id).first()
    if data:
        form = ProfessionalSocietiesForm(request.form,obj=data)
        profile_exists=True
    else:
        form= ProfessionalSocietiesForm(request.form)
        profile_exists=False

    if request.method == 'POST' and form.validate():
        if data==None:
            professional_society=Professional_Societies(
                start_date=request.form['start_date'],
                end_date=request.form['end_date'],
                name=request.form['name'],
                membership_type=request.form['membership_type'],
                status=request.form['status'],
                users=current_user.id
                )
            db.session.add(professional_society)
        else:
            data.start_date=request.form['start_date']
            data.end_date=request.form['end_date']
            data.name=request.form['name']
            data.membership_type=request.form['membership_type']
            data.status=request.form['status']
        db.session.commit()
    return render_template('forms/professional_societies_form.html', title='Professional Societies', user=current_user.id, form=form, profile_exists= profile_exists)

# Allows a researcher to add their award, update their awards, and view their awards
@app.route('/user/awards_form', methods=['GET', 'POST', 'PUT'])
#@login_required_advanced(role="sfiAdmin")
def awards_form():
    data=AwardsDB.query.filter_by(users=current_user.id).first()
    if data:
        form = AwardsForm(request.form,obj=data)
        profile_exists=True
    else:
        form= AwardsForm(request.form)
        profile_exists=False

    if request.method == 'POST' or request.method == 'PUT':
        if data==None:
            award=AwardsDB(
                awarding_body=request.form['awarding_body'],
                awarding_details=request.form['awarding_details'],
                year=request.form['year'],
                users=current_user.id
                )
            db.session.add(award)
        else:
            data.awarding_body=request.form['awarding_body']
            data.awarding_details=request.form['awarding_details']
            data.year=request.form['year']
        db.session.commit()
    return render_template('forms/awards_form.html', title='Awards & Distinctions', user=current_user.id, form=form, profile_exists= profile_exists)

# Allows a researcher to add their funding diversification, update their funding diversification, and view their funding diversification
@app.route('/user/funding_diversification_form', methods=['GET', 'POST'])
#@login_required_advanced(role="sfiAdmin")
def funding_diversification_form():
    data=Funding_Diversification.query.filter_by(users=current_user.id).first()
    if data:
        form = FundingDiversificationForm(request.form,obj=data)
        profile_exists=True
    else:
        form= FundingDiversificationForm(request.form)
        profile_exists=False

    if request.method == 'POST' and form.validate():
        if data==None:
            funding_diversification=Funding_Diversification(
                start_date=request.form['start_date'],
                end_date =request.form['end_date'],
                funding_amount=request.form['funding_amount'],
                funding_body=request.form['funding_body'],
                funding_programme=request.form['funding_programme'],
                status=request.form['status'],
                users=current_user.id
                )
            db.session.add(funding_diversification)
        else:
            data.start_date=request.form['start_date']
            data.end_date =request.form['end_date']
            data.funding_amount=request.form['funding_amount']
            data.funding_body=request.form['funding_body']
            data.funding_programme=request.form['funding_programme']
            data.status=request.form['status']
        db.session.commit()
    return render_template('forms/funding_diversification_form.html', title='Funding Diversification', user=current_user.id, form=form, profile_exists= profile_exists)

# Allows a researcher to add their impacts, update their impacts, and view their impacts
@app.route('/user/impacts_form', methods=['GET', 'POST'])
#@login_required_advanced(role="sfiAdmin")
def impacts_form():
    data=Impacts.query.filter_by(users=current_user.id).first()
    if data:
        form = ImpactsForm(request.form,obj=data)
        profile_exists=True
    else:
        form= ImpactsForm(request.form)
        profile_exists=False

    if request.method == 'POST' and form.validate():
        if data==None:
            impact=Impacts(
                impact_title=request.form['impact_title'],
                impact_category =request.form['impact_category'],
                primary_beneficiary=request.form['primary_beneficiary'],
                users=current_user.id
                )
            db.session.add(impact)
        else:
            data.impact_title=request.form['impact_title']
            data.impact_category =request.form['impact_category']
            data.primary_beneficiary=request.form['primary_beneficiary']
        db.session.commit()
    return render_template('forms/impacts_form.html', title='Impacts', user=current_user.id, form=form, profile_exists= profile_exists)

# Allows a researcher to add their innovations, update their innovations, and view their innovations
@app.route('/user/innovations_form', methods=['GET', 'POST'])
#@login_required_advanced(role="sfiAdmin")
def innovations_form():
    data=Innovations.query.filter_by(users=current_user.id).first()
    if data:
        form = InnovationsForm(request.form,obj=data)
        profile_exists=True
    else:
        form= InnovationsForm(request.form)
        profile_exists=False

    if request.method == 'POST' and form.validate():
        if data==None:
            innovation=Innovations(
                year=request.form['year'],
                type =request.form['type'],
                title=request.form['title'],
                users=current_user.id
                )
            db.session.add(innovation)
        else:
            data.year=request.form['year']
            data.type =request.form['type']
            data.title=request.form['title']
        db.session.commit()
    return render_template('forms/innovations_form.html', title='Innovations', user=current_user.id, form=form, profile_exists= profile_exists)

# Allows a researcher to add their publications, update their publications, and view their publications
@app.route('/user/publications_form', methods=['GET', 'POST'])
#@login_required_advanced(role="sfiAdmin")
def publications_form():
    data=Publications.query.filter_by(users=current_user.id).first()
    if data:
        form = PublicationsForm(request.form,obj=data)
        profile_exists=True
    else:
        form = PublicationsForm(request.form)
        profile_exists=False

    if request.method == 'POST' and form.validate():
        if data==None:
            if request.form['published'] == "True":
                published2= True
            if request.form['published'] == "False":
                published2 = False
            if request.form['in_press']  == "True":
                in_press2 = True
            if request.form['in_press'] == "False":
                in_press2 = False
            publications=Publications(
                year=request.form['year'],
                title=request.form['title'],
                type=request.form['type'],
                journal_conference_name=request.form['journal_conference_name'],
                published=published2,
                in_press=in_press2,
                users= current_user.id,
                doi=request.form['doi']
                )
            db.session.add(publications)
        else:
            if request.form['published'] == "True":
                published2= True
            if request.form['published'] == "False":
                published2 = False
            if request.form['in_press']  == "True":
                in_press2 = True
            if request.form['in_press'] == "False":
                in_press2 = False
            data.year=request.form['year']
            data.title=request.form['title']
            data.type=request.form['type']
            data.journal_conference_name=request.form['journal_conference_name']
            #if request.form['published']==True
            data.published= published2
            data.in_press= in_press2
            data.doi=request.form['doi']
        db.session.commit()
    return render_template('forms/publications_form.html', title='Publications', user=current_user.id, form=form, profile_exists= profile_exists)

# Allows a researcher to add their presentations, update their presentations, and view their presentations
@app.route('/user/presentations_form', methods=['GET', 'POST'])
#@login_required_advanced(role="sfiAdmin")
def presentations_form():
    data=Presentations.query.filter_by(users=current_user.id).first()
    if data:
        form = PresentationsForm(request.form,obj=data)
        profile_exists=True
    else:
        form = PresentationsForm(request.form)
        profile_exists=False

    if request.method == 'POST' and form.validate():
        if data==None:
            presentation=Presentations(
                year=request.form['year'],
                type=request.form['type'],
                title=request.form['title'],
                organizing_body=request.form['organizing_body'],
                location=request.form['location'],
                users= current_user.id
                )
            db.session.add(presentation)
        else:
            data.year=request.form['year']
            data.type=request.form['type']
            data.title=request.form['title']
            data.organizing_body=request.form['organizing_body']
            data.location=request.form['location']
        db.session.commit()
    return render_template('forms/presentations_form.html', title='Presentations', user=current_user.id, form=form, profile_exists= profile_exists)

# Allows a researcher to add their academic collaborations, update their academic collaborations, and view their academic collaborations
@app.route('/user/academic_collab_form', methods=['GET', 'POST'])
#@login_required_advanced(role="sfiAdmin")
def academic_collab_form():
    data=AcademicCollabs.query.filter_by(users=current_user.id).first()
    if data:
        form = AcademicCollabForm(request.form,obj=data)
        profile_exists=True
    else:
        form = AcademicCollabForm(request.form)
        profile_exists=False

    if request.method == 'POST' and form.validate():
        if data==None:
            a_collabs= AcademicCollabs(
                start_date=request.form['start_date'],
                end_date=request.form['end_date'],
                department=request.form['department'],
                institution_name=request.form['institution_name'],
                location=request.form['location'],
                collaborator_name=request.form['collaborator_name'],
                collaborator_goal=request.form['collaborator_goal'],
                users= current_user.id,
                interaction_frequency=request.form['interaction_frequency']
                )
            db.session.add(a_collabs)
        else:
            data.start_date=request.form['start_date']
            data.end_date=request.form['end_date']
            data.department=request.form['department']
            data.institution_name=request.form['institution_name']
            data.location=request.form['location']
            data.collaborator_name=request.form['collaborator_name']
            data.collaborator_goal=request.form['collaborator_goal']
            data.interaction_frequency=request.form['interaction_frequency']
        db.session.commit()
    return render_template('forms/academic_collab_form.html', title='Academic Collab', user=current_user.id, form=form, profile_exists= profile_exists)

# Allows a researcher to add their non-academic collaborations, update their non-academic collaborations, and view their non-academic collaborations
@app.route('/user/non_academic_collab_form', methods=['GET', 'POST'])
#@login_required_advanced(role="sfiAdmin")
def non_academic_collab_form():
    data=NonAcademicCollabs.query.filter_by(users=current_user.id).first()
    if data:
        form = NonAcademicCollabForm(request.form,obj=data)
        profile_exists=True
    else:
        form = NonAcademicCollabForm(request.form)
        profile_exists=False

    if request.method == 'POST' and form.validate():
        if data==None:
            non_a_collabs= NonAcademicCollabs(
                start_date=request.form['start_date'],
                end_date=request.form['end_date'],
                department=request.form['department'],
                location=request.form['location'],
                collaborator_name=request.form['collaborator_name'],
                collaborator_goal=request.form['collaborator_goal'],
                users= current_user.id,
                interaction_frequency=request.form['interaction_frequency']
                )
            db.session.add(non_a_collabs)
        else:
            data.start_date=request.form['start_date']
            data.end_date=request.form['end_date']
            data.department=request.form['department']
            data.location=request.form['location']
            data.collaborator_name=request.form['collaborator_name']
            data.collaborator_goal=request.form['collaborator_goal']
            data.interaction_frequency=request.form['interaction_frequency']
        db.session.commit()
    return render_template('forms/non_academic_collab_form.html', title='Non Academic Collab', user=current_user.id, form=form, profile_exists= profile_exists)

# Allows a researcher to add their conferences, update their conferences, and view their conferences
@app.route('/user/conferences_form', methods=['GET', 'POST'])
#@login_required_advanced(role="sfiAdmin")
def conferences_form():
    data=Conferences.query.filter_by(users=current_user.id).first()
    if data:
        form = ConferencesForm(request.form,obj=data)
        profile_exists=True
    else:
        form = ConferencesForm(request.form)
        profile_exists=False

    if request.method == 'POST' and form.validate():
        if data==None:
            conferences= Conferences(
                start_date=request.form['start_date'],
                end_date=request.form['end_date'],
                title=request.form['title'],
                type=request.form['type'],
                role=request.form['role'],
                event_location=request.form['event_location'],
                users= current_user.id
                )
            db.session.add(conferences)
        else:
            data.start_date=request.form['start_date']
            data.end_date=request.form['end_date']
            data.title=request.form['title']
            data.type=request.form['type']
            data.role=request.form['role']
            data.event_location=request.form['event_location']
        db.session.commit()
    return render_template('forms/conferences_form.html', title='Conferences', user=current_user.id, form=form, profile_exists= profile_exists)

# Allows a researcher to add their communications overview, update their communications overview, and view their communications overview
@app.route('/user/communication_form', methods=['GET', 'POST'])
#@login_required_advanced(role="sfiAdmin")
def communication_form():
    data=Communication.query.filter_by(users=current_user.id).first()
    if data:
        form = CommunicationForm(request.form,obj=data)
        profile_exists=True
    else:
        form = CommunicationForm(request.form)
        profile_exists=False

    if request.method == 'POST' and form.validate():
        if data==None:
            communication= Communication(
                year=request.form['year'],
                num_lectures=request.form['num_lectures'],
                num_visits=request.form['num_visits'],
                num_media_interactions=request.form['num_media_interactions'],
                users= current_user.id
                )
            db.session.add(communication)
        else:
            data.year=request.form['year']
            data.num_lectures=request.form['num_lectures']
            data.num_visits=request.form['num_visits']
            data.num_media_interactions=request.form['num_media_interactions']
        db.session.commit()
    return render_template('forms/communication_form.html', title='Communication', user=current_user.id, form=form, profile_exists= profile_exists)

# Allows a researcher to add their SFI funding ratio, update their SFI funding ratio, and view their SFI funding ratio
@app.route('/user/funding_ratio', methods=['GET', 'POST'])
#@login_required_advanced(role="sfiAdmin")
def funding_ratio_form():
    data=FundingRatio.query.filter_by(users=current_user.id).first()
    if data:
        form = FundingRatioForm(request.form,obj=data)
        profile_exists=True
    else:
        form = FundingRatioForm(request.form)
        profile_exists=False

    if request.method == 'POST' and form.validate():
        if data==None:
            funding_ratio= FundingRatio(
                year=request.form['year'],
                percentage=request.form['percentage'],
                users= current_user.id
                )
            db.session.add(funding_ratio)
        else:
            data.year=request.form['year']
            data.percentage=request.form['percentage']
        db.session.commit()
    return render_template('forms/funding_ratio.html', title='Funding Ratio', user=current_user.id, form=form, profile_exists= profile_exists)

@app.route('/sample_button',methods=['GET','POST'])
@login_required
def press_button():#TESTER FUNCTION REMOVE AFTERWARDS
    if request.method == 'POST':
        call_for_proposal_title=request.form['sample']
        application = Grant_Application(
        user_id = current_user.id, proposal_title=call_for_proposal_title)
        db.session.add(application)
        db.session.commit()
        return redirect(url_for('submit_application',application_id=application.grant_application_id))#

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
#@login_required_advanced("role
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
    return json.dumps({'status':'OK','query:':return_string});

@app.route("/sample_slider")
def sample_slider():
    return render_template('sample_slider.html')

@app.route("/notifications")
def notifications():
    #grants=Grant_Application.query.all()
    grants = db.session.query(Grant_Application).count()
    calls= db.session.query(CFP).count()
    return render_template('notifications.html', title='Profile', user=user, grants=grants, calls=calls)

@app.route("/submitted_applications", methods=['GET', 'POST'])
def submitted_applications():
    application_count = 0
    submittedApps =[]
    applications = SubmittedApplications.query.all()#Change to submited_applications
    for grant in applications:
        application_count = application_count + 1
        new_grant =Grant_Application.query.filter_by(grant_application_id=grant.grant_application_id).first()
        if new_grant:
            submittedApps.append(new_grant)

    if request.method == 'POST':
        application_id =request.form['application_id']
        app = Grant_Application.query.filter_by(grant_application_id=application_id).first()
        app.approved = True
        db.session.commit()
    return render_template('submitted_applications.html', title='Profile', user=user, grants=submittedApps, application_count=application_count)

@app.route("/review_applications", methods=['GET', 'POST'])
def review_applications():
    application_count = 0
    grants = Grant_Application.query.filter_by(approved=True).all()
    for grant in grants:
        application_count = application_count + 1
    if request.method == 'POST':
        grant_application = request.form["grant_id"]
        get_grant = Grant_Application.query.filter_by(grant_application_id=grant_application).first()
        get_grant.reviewer_approved = True
        db.session.commit()
    return render_template('review_applications.html', title='Profile', user=user, grants=grants, application_count=application_count)

@app.route("/reviewed_applications", methods=['GET', 'POST'])
def reviewed_applications():
    application_count = 0
    grants = Grant_Application.query.filter_by(reviewer_approved=True).all()
    for grant in grants:
        application_count = application_count + 1

    if request.method == 'POST':
        if request.form['submit_button'] == 'Accept verdict':
            for approved_grants in grants:
                accepted_proposal = ProposalsAccepted(grant_number=approved_grants.grant_application_id,confirmed=False,began=False)#Send email.
                db.session.add(accepted_proposal)
                db.session.commit()
                applicant = User.query.filter_by(id = approved_grants.user_id).first()
                if applicant:
                    send_grant_accepted(applicant)
        elif request.form['submit_button'] == 'Reject verdict':
            for approved_grants in grants:
                applicant = User.query.filter_by(id = approved_grants.user_id).first()
                if applicant:
                    send_grant_rejected(applicant)

        else:
            pass
            #return jsonify({'status':'OK','File loop':"TESTER"});

    return render_template('reviewed_applications.html', title='Profile', user=current_user, grants=grants, application_count=application_count)

# Route to the SFI home page
@app.route("/home", methods=['GET','POST'])
def home():
    calls=CFP.query.all()
    date=datetime.now()
    return render_template('home.html', title='Home', user=user, date=date, calls=calls)

# Route to the subscribe page
@app.route("/subscribe")
def subscribe():
    return render_template('subscriptions.html', title='Subscribe', user=user)

# Route to the about page
@app.route("/about")
def about():
    return render_template('about.html', title='About', user=user)

# Route to the services page
@app.route("/services")
def services():
    return render_template('services.html', title='Services', user=user)

# Route to the clients page
@app.route("/clients")
def clients():
    return render_template('clients.html', title='Clients', user=user)

# Route to the contact page
@app.route("/contact")
def contact():
    return render_template('contact.html', title='Contact', user=user)

#Route for pending applications page
@app.route("/pending_applications", methods=['GET', 'POST'])
def pending_applications():
    new_msg = ""
    grants= []
    new_app = ""
    applications = Grant_Application.query.filter_by(user_id=current_user.id).all()
    for grant in applications:
        accepted_proposals = ProposalsAccepted.query.filter_by(grant_number=grant.grant_application_id).first()
        if accepted_proposals:
            if accepted_proposals.confirmed==False:#Should be checking to see if confirmed and adding form to confirm if true
                grants.append(grant)
                new_msg = "Your grant application has been accepted"
                new_app = True
            else:
                new_msg = "You have no new accepted grant applications"
                new_app = False


    if request.method == 'POST':
        if request.form['submit_button'] == 'Accept offer':
            #user_grant = Grant_Application.query.filter_by(user_id=current_user.id).first()#Will need to iterate through to get the right version.
            #proposal = ProposalsAccepted.query.filter_by(grant_number=user_grant.grant_application_id).first()#will need to fix this and linke to the above.
            accepted_proposals.confirmed = True # Should be true
            db.session.commit()
        elif request.form['submit_button'] == 'Reject offer':
            grant_app = Grant_Application.query.filter_by(user_id=current_user.id).first()
            ProposalsAccepted.query.filter_by(grant_number=grant_app.grant_application_id).delete()
            Grant_Application.query.filter(user_id  == current_user.id).delete() # Might have to delete from other databases as well
            pass


    return render_template('pending_applications.html', title='Applications Pending Action', user=current_user, msg = new_msg, new_apps = new_app, grant_list=grants)

# Route to the Scientific Reports Pending Action page
@app.route("/pending_scientific_reports")
def pending_scientific_reports():
    return render_template('pending_scientific_reports.html', title='Scientific Reports Pending Action', user=user)

# Route to the Financial Reports Pending Action page
@app.route("/pending_financial_reports")
def pending_financial_reports():
    return render_template('pending_financial_reports.html', title='Financial Reports Pending Action', user=user)

# Route to the Budgets Pending Action page
@app.route("/pending_budgets")
def pending_budgets():
    return render_template('pending_budgets.html', title='Budgets Pending Action', user=user)

# Route to the Pre Award Applicant Response Pending Action page
@app.route("/pending_pre_award_applicant_response")
def pending_pre_award_applicant_response():
    return render_template('pending_pre_award_applicant_response.html', title='Pre Award Applicant Response Pending Action', user=user)

# Route to the Other Items Pending Action page
@app.route("/pending_other_items")
def pending_other_items():
    return render_template('pending_other_items.html', title='Other Items Pending Action', user=user)