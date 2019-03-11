from flask_mail import Message
from flask import render_template
from grants import mail,app

def send_email(subject, sender, recipients, text_body, html_body):
    msg = Message(subject, sender=sender, recipients=recipients)
    msg.body = text_body
    msg.html = html_body
    mail.send(msg)

def send_password_reset_email(user):
    token = user.get_reset_password_token()
    send_email('[SFI] Reset Your Password',
               sender=app.config["MAIL_USERNAME"],
               recipients=[user.email],
               text_body=render_template('email/reset_password.txt',
                                         user=user, token=token),
               html_body=render_template('email/reset_password.html/',
                                         user=user, token=token))

def send_grant_accepted(user):
    #Contacts the applicants to let them know that their grant has been accepted.
    send_email('[SFI] GRANT Application Accepted',
               sender=app.config["MAIL_USERNAME"],
               recipients=[user.email],
               text_body=render_template('email/grant_accepted.txt',
                                         user=user),
               html_body=render_template('email/grant_accepted.html/',
                                         user=user))

def send_grant_rejected(user):
    #Contacts the user to let them know that the grant has been rejected.
    send_email('[SFI] Grant Application Rejected',
               sender=app.config["MAIL_USERNAME"],
               recipients=[user.email],
               text_body=render_template('email/grant_rejected.txt',
                                         user=user),
               html_body=render_template('email/grant_rejected.html/',
                                         user=user))


def notify_of_reviewer_response(user):
    #Contacts the sfiAdmin to let them know of update to
    send_email('[SFI] Reviewer has reviewed the Applications',
               sender=app.config["MAIL_USERNAME"],
               recipients=[user.email],
               text_body=render_template('email/reviewed.txt',
                                         user=user),
               html_body=render_template('email/reviewed.html/',
                                         user=user))

def notify_reviewer(user):
    if user.email is not None:
        send_email('[SFI] There are new applications which require reviewing',
                   sender=app.config["MAIL_USERNAME"],
                   recipients=[user.email],
                   text_body=render_template('email/notify_reviewer.txt',
                                             user=user),
                   html_body=render_template('email/notify_reviewer.html/',
                                             user=user))

def welcomeEmail(user):
    send_email('[SFI] Thanks for creating an account with SFI',
               sender=app.config["MAIL_USERNAME"],
               recipients=[user.email],
               text_body=render_template('email/new_user.txt',
                                         user=user),
               html_body=render_template('email/new_user.html/',
                                         user=user))