from flask.ext.wtf import Form
from wtforms import StringField, DateField, IntegerField, TextAreaField, TextField
from wtforms.validators import required, DataRequired

class AddBiz(Form):
  name = TextField('Biz Name',validators=[required()])
  description = TextAreaField('Description',validators=[required()])
  added_date = DateField('Added Date (mm/dd/yyyy)',validators=[required()],format='%m/%d/%Y')

class BizForm(Form):
    bizid = IntegerField('bizid', validators=[DataRequired()])
    bizname = StringField('bizname')
