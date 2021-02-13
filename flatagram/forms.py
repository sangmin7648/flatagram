from flask import current_app
from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileRequired, FileAllowed
from wtforms import StringField, TextAreaField, MultipleFileField, PasswordField, SubmitField
from wtforms.fields.html5 import EmailField
from wtforms.validators import DataRequired, EqualTo, Email, Length
from werkzeug.utils import secure_filename


class UploadForm(FlaskForm):
    img = MultipleFileField('이미지', validators=[
        # FileRequired(message='파일을 선택하세요'),
        # FileAllowed(['jpg', 'jpeg', 'png'], '이미지 파일만 업로드 가능합니다')
    ])
    desc = TextAreaField('설명')


class CommentForm(FlaskForm):
    comment = TextAreaField('댓글', validators=[DataRequired()])


class UserCreateForm(FlaskForm):
    username = StringField('아이디', validators=[
        DataRequired(), Length(min=3, max=25, message='아이디는 3자 이상 25자 이하여야합니다')])
    name = StringField('닉네임', validators=[DataRequired()])
    password1 = PasswordField('비밀번호', validators=[
        DataRequired(), EqualTo('password2', '비밀번호가 일치하지 않습니다')])
    password2 = PasswordField('비밀번호 확인', validators=[DataRequired()])
    email = EmailField('이메일', validators=[DataRequired(), Email()])


class LoginForm(FlaskForm):
    username_or_email = StringField('아이디 또는 이메일', validators=[
        DataRequired(), Length(min=3, max=25, message='아이디는 3자 이상 25자 이하여야합니다')])
    password = PasswordField('비밀번호', validators=[
        DataRequired()])


class MessageForm(FlaskForm):
    message = TextAreaField('메시지', validators=[DataRequired(), Length(min=0, max=140)])