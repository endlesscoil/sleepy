import urwid

class ConsoleUI(object):
    def __init__(self):
        self.program_label = urwid.Text(u'Sleepy v0.1', align='center')
        self.artist_label = urwid.Text(u'Artist: ', align='right')
        self.artist_data = urwid.Text(u'', align='left')
        self.artist_box = urwid.Columns([self.artist_label, self.artist_data])
        self.title_label = urwid.Text(u'Title: ', align='right')
        self.title_data = urwid.Text(u'', align='left')
        self.title_box = urwid.Columns([self.title_label, self.title_data])
        self.album_label = urwid.Text(u'Album: ', align='right')
        self.album_data = urwid.Text(u'', align='left')
        self.album_box = urwid.Columns([self.album_label, self.album_data])
        self.divider = urwid.Divider()

        self.pile = urwid.Pile([self.program_label, self.divider, self.artist_box, self.title_box, self.album_box])

        self.bg = urwid.Filler(self.pile)
        self.loop = urwid.MainLoop(self.bg)

    def run(self):
        self.loop.run()

    @property
    def artist(self):
        return self.artist_data.get_text()
    
    @artist.setter
    def artist(self, value):
        print value
        self.artist_data.set_text(value)

    @property
    def title(self):
        return self.title_data.get_text()
    
    @title.setter
    def title(self, value):
        self.title_data.set_text(value)

    @property
    def album(self):
        return self.album_data.get_text()
    
    @album.setter
    def album(self, value):
        self.album_data.set_text(value)

class WebUI(object):
    pass