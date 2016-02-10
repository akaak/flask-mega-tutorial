from flask.ext.wtf import Form
from wtforms import StringField, DateField, IntegerField, \
	TextAreaField, TextField, validators
from wtforms.validators import required, DataRequired, InputRequired

class AddBiz(Form):
  name = TextField('Biz Name',[validators.Length(min=4, max=80)])
  description = TextAreaField('Description',validators=[required()])
  added_date = DateField('When did you add this business? (mm/dd/yyyy)',
  	validators=[InputRequired()],format='%m/%d/%Y')

class BizForm(Form):
    bizid = IntegerField('bizid', validators=[DataRequired()])
    bizname = StringField('bizname')
