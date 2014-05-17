from flask import Blueprint, current_app, render_template

from ..db import db, Source

frontend = Blueprint('frontend', __name__, url_prefix='/')

@frontend.route('/')
def index():
    track = current_app.sleepy.current_track

    return render_template('index.html', track=track)

@frontend.route('sources')
def sources():
    sources = Source.query.all()

    return render_template('sources.html', sources=sources)

@frontend.route('source/<int:id>')
def source(id):
    source = Source.query.filter_by(id=id).first_or_404()
    
    return render_template('source.html', source=source)