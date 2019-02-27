from flask import request
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField
from wtforms.validators import ValidationError, DataRequired, Length
from flask_babel import _, lazy_gettext as _l
from app.models import User


class EditProfileForm(FlaskForm):
    username = StringField(_l("Nom d'utilisateur"), validators=[DataRequired()])
    about_me = TextAreaField(_l('À propos de moi'),
                             validators=[Length(min=0, max=140)])
    submit = SubmitField(_l('Soumettre'))

    def __init__(self, original_username, *args, **kwargs):
        super(EditProfileForm, self).__init__(*args, **kwargs)
        self.original_username = original_username

    def validate_username(self, username):
        if username.data != self.original_username:
            user = User.query.filter_by(username=self.username.data).first()
            if user is not None:
                raise ValidationError(_("Merci d'utiliser un nom d'utilisateur différent."))


class PostForm(FlaskForm):
    post = TextAreaField(_l('Dis moi quelque chose...'), validators=[DataRequired()])
    submit = SubmitField(_l('Envoyer'))