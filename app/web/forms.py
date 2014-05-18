from flask_wtf import Form
from wtforms import TextField, SubmitField, SelectField, PasswordField
from wtforms.validators import Required, Length

from ..sources import SOURCES

class SourceForm(Form):
    name = TextField(u'Name', [Required(), Length(max=255)])
    type = SelectField(u'Type', choices=[(k, k) for k in SOURCES.keys()])

    url = TextField(u'URL', [Length(max=255)])
    username = TextField(u'Username', [Length(max=255)])
    password = PasswordField(u'Password', [Length(max=255)])

    submit = SubmitField(u'Save')

class PlaylistsForm(Form):
    playlist = SelectField(u'Playlist')

    submit = SubmitField(u'Add')
