from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField
from wtforms.validators import DataRequired

class DocumentRequestForm(FlaskForm):
    receiver = StringField('수신', validators=[DataRequired()])
    referrer = StringField('경유', )
    title = StringField('제목', validators=[DataRequired()])
    contents = TextAreaField('문서제목', validators=[DataRequired()])
    attach = StringField('붙임', validators=[DataRequired()])
    organization = StringField('기관명', validators=[DataRequired()])