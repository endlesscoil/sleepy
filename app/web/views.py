from flask import Blueprint, current_app, render_template

frontend = Blueprint('frontend', __name__, url_prefix='/')

@frontend.route('/')
def index():
    track = current_app.sleepy.current_track

    return render_template('index.html', track=track)
