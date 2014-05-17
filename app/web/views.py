from flask import Blueprint, current_app, render_template

from ..db import db, Source
from .forms import SourceForm

frontend = Blueprint('frontend', __name__, url_prefix='/')

TABS = [
    ('/', 'Home'),
    ('/sources', 'Sources'),
    ('/settings', 'Settings'),
]

@frontend.context_processor
def frontend_context_processor():
    return { 'TABS': TABS }

@frontend.route('/')
def index():
    track = current_app.sleepy.current_track

    return render_template('index.html', active='Home', track=track)

@frontend.route('sources')
def sources():
    sources = Source.query.all()

    return render_template('sources.html', active='Sources', sources=sources)

@frontend.route('sources/<int:id>')
def source(id):
    source = Source.query.filter_by(id=id).first_or_404()
    form = SourceForm(obj=source)

    if form.validate_on_submit():
        form.populate_obj(source)

        db.session.add(source)
        db.session.commit()
    
    return render_template('source.html', active='Sources', form_target='/sources/{0}'.format(id), form=form)

@frontend.route('sources/create', endpoint='create_source', methods=['GET', 'POST'])
def create_source():
    form = SourceForm()

    if form.validate_on_submit():
        source = Source()
        form.populate_obj(source)

        db.session.add(source)
        db.session.commit()

    return render_template('source.html', active='Sources', form_target='/sources/create', form=form)