from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, TextAreaField
from wtforms.validators import DataRequired, Length

class LoginForm(FlaskForm):
    headText = StringField('输入：', validators=[Length(min=0, max=140)])
    input = StringField('上联：', validators=[Length(min=0, max=140)])
    output = StringField('下联：', validators=[Length(min=0, max=140)])
    submit = SubmitField('对下联')
