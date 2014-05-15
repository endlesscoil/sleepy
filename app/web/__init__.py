from flask import Flask, g

flask_app = Flask('sleepy')
flask_app.debug = False

@flask_app.route('/')
def index():
    track = flask_app.sleepy.current_track

    html = """
    <html>
    <body>
    <h1>Now Playing</h1>
    <div>{track.artist}</div>
    <div>{track.title}</div>
    <div>{track.album}</div>
    </vody>
    </html>
    """.format(track=track)

    return html