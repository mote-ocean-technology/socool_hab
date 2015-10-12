from flask.ext.wtf import Form
from wtforms import StringField, BooleanField, SelectField
from wtforms.validators import DataRequired
from wtforms.fields.html5 import DateField

class opdDeploymentForm(Form):

    site = StringField('site')
    serial = SelectField('serial',coerce=int, validators=[DataRequired()])
    operator = SelectField('operator', validators=[DataRequired()])
    deployed =  DateField('deployed', validators=[DataRequired()])
