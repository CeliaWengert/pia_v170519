from flask import render_template, redirect, url_for, flash, request
from werkzeug.urls import url_parse
from flask_login import login_user, logout_user, current_user, login_required
from flask_babel import _
from app import db
from app.auth import bp
from app.auth.forms import LoginForm, RegistrationForm, \
    ResetPasswordRequestForm, ResetPasswordForm
from app.models import User
from app.auth.email import send_password_reset_email
import mysql.connector
from app.auth.historique_ouverture_conversation import HistoriqueOuvertureConversation


@bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    form = LoginForm()
    if form.validate_on_submit():
        global username
        username=form.username.data
        user = User.query.filter_by(username=form.username.data).first()
		
        open_conv=HistoriqueOuvertureConversation(username)
        open_conv.createNewConversation()
        open_conv.closeDBConnection()
		
        if user is None or not user.check_password(form.password.data):
            flash(_("Nom d'utilisateur ou mot de passe invalide."))
            return redirect(url_for('auth.login'))
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('main.index')		
        return redirect(next_page)
    return render_template('auth/login.html', title=_('Connexion'), form=form)

@bp.route('/logout')
def logout():
    logout_user()
    # open_conv=HistoriqueOuvertureConversation(int(current_user.id))
    # open_conv.disconnectUser()
    # open_conv.closeDBConnection()
    return redirect(url_for('main.index'))

@bp.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash(_('Félicitations, tu fais maintenant partie de notre grande famille !'))
#        try :
#            conn = mysql.connector.connect(host="130.79.207.104",user="Hugo",password="PIAisBetter1996=)",database="pia")
#            cursor = conn.cursor()
#            cursor.execute("SELECT id from user;")
#            result = cursor.fetchall()
#            args=result[-1]
#            cursor.callproc('sp_InsertIntoAll',args)
#            cursor.close()
#            conn.commit()
#        except mysql.connector.Error as error:
#            print("Failed to execute stored procedure: {}".format(error))
        return redirect(url_for('auth.login'))
    return render_template('auth/register.html', title=_('Inscription'),form=form)


@bp.route('/reset_password_request', methods=['GET', 'POST'])
def reset_password_request():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    form = ResetPasswordRequestForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user:
            send_password_reset_email(user)
        flash(
            _("Jette un coup d'oeil à tes emails et suis les instructions de réinitialisation de ton mot de passe."))
        return redirect(url_for('auth.login'))
    return render_template('auth/reset_password_request.html',
                           title=_('Réinitialisation du mot de passe'), form=form)


@bp.route('/reset_password/<token>', methods=['GET', 'POST'])
def reset_password(token):
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    user = User.verify_reset_password_token(token)
    if not user:
        return redirect(url_for('main.index'))
    form = ResetPasswordForm()
    if form.validate_on_submit():
        user.set_password(form.password.data)
        db.session.commit()
        flash(_('Ton mot de passe a été réinitialisé.'))
        return redirect(url_for('auth.login'))
    return render_template('auth/reset_password.html', form=form)