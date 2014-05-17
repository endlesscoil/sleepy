from flask_wtf import Form
from wtforms import TextField, SubmitField

class Source(Form):
    test = TextField(u'hi')

    submit = SubmitField(u'Save')