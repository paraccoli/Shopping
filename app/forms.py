from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed, FileRequired
from wtforms import StringField, FloatField, TextAreaField, SubmitField, PasswordField
from wtforms.validators import DataRequired, Email, EqualTo
from wtforms import SelectField

class ProductForm(FlaskForm):
    name = StringField('商品名', validators=[DataRequired()])
    price = FloatField('価格', validators=[DataRequired()])
    description = TextAreaField('説明')
    image = FileField('商品画像', validators=[FileAllowed(['jpg', 'jpeg', 'png'], 'Images only!'), FileRequired('File was empty!')])
    submit = SubmitField('追加')

class LoginForm(FlaskForm):
    username = StringField('ユーザー名', validators=[DataRequired()])
    password = PasswordField('パスワード', validators=[DataRequired()])
    submit = SubmitField('ログイン')

class RegistrationForm(FlaskForm):
    username = StringField('ユーザー名', validators=[DataRequired()])
    email = StringField('メールアドレス', validators=[DataRequired(), Email()])
    password = PasswordField('パスワード', validators=[DataRequired()])
    password2 = PasswordField('パスワード（確認用）', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('登録')

class UpdateUserForm(FlaskForm):
    username = StringField('ログインID', validators=[DataRequired()])
    nickname = StringField('ニックネーム')
    password = PasswordField('新しいパスワード')
    password2 = PasswordField('新しいパスワード（確認用）', validators=[EqualTo('password')])
    avatar = FileField('アバター', validators=[FileAllowed(['jpg', 'jpeg', 'png'], 'Images only!')])
    submit = SubmitField('更新')