from flask import Blueprint, current_app, render_template, redirect, url_for, flash

from ..db import db, Source, SourcePlaylist
from .forms import SourceForm, PlaylistsForm

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

@frontend.route('sources/<int:id>', methods=['GET', 'POST'])
def source(id):
    source = Source.query.filter_by(id=id).first_or_404()
    form = SourceForm(obj=source)

    if form.validate_on_submit():
        form.populate_obj(source)

        db.session.add(source)
        db.session.commit()

        return redirect(url_for('frontend.sources'))
    
    return render_template('source.html', active='Sources', form_target='/sources/{0}'.format(id), form=form)

@frontend.route('sources/create', endpoint='create_source', methods=['GET', 'POST'])
def create_source():
    form = SourceForm()

    if form.validate_on_submit():
        source = Source()
        form.populate_obj(source)

        db.session.add(source)
        db.session.commit()

        return redirect(url_for('frontend.sources'))

    return render_template('source.html', active='Sources', form_target='/sources/create', form=form)

@frontend.route('sources/<int:id>/delete', endpoint='delete_source', methods=['GET', 'POST'])
def delete_source(id):
    source = Source.query.filter_by(id=id).first_or_404()

    db.session.delete(source)
    db.session.commit()

    return redirect(url_for('frontend.sources'))

@frontend.route('playlists/<int:id>', methods=['GET', 'POST'])
def playlists(id):
    form = PlaylistsForm()
    source = current_app.sleepy.sources.sources[id]

    playlists_available = []
    form.playlist.choices = []
    if source.authenticated or source.authenticate():
        playlists_available = source.get_playlists()
        playlists_added = SourcePlaylist.query.filter_by(source_id=id).all()

        # Automatically remove playlists that no longer exist.
        removed_playlists = []
        for p in source.playlists:
            if p not in playlists_available:
                sp = SourcePlaylist.query.filter_by(source_id=id, name=p).first()
                removed_playlists.append(sp.name)
                source.playlists.remove(sp.name)
                db.session.delete(sp)

        if len(removed_playlists) > 0:
            msg = 'The following playlists were removed because they no longer exist on the source: '
            for rp in removed_playlists:
                msg += rp + ','

            msg = msg[:-1]
            flash(msg, 'bg-warning')
            db.session.commit()

        # Remove playlists that are already added.
        for sp in playlists_added:
            if sp.name in playlists_available:
                playlists_available.remove(sp.name)

        form.playlist.choices = [(playlist, playlist) for playlist in playlists_available]

    if form.validate_on_submit():
        source_playlist = SourcePlaylist(source_id=id, name=form.playlist.data)

        source.add_playlist(form.playlist.data)

        db.session.add(source_playlist)
        db.session.commit()

    return render_template('playlists.html', active='Sources', source=source, playlists=source.playlists,
                            form_target='/playlists/{0}'.format(id), form=form)