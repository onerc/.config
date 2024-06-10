from fabric.widgets import Button, Label
from fabric.utils.fabricator import Fabricator
from fabric.utils import exec_shell_command
from gi.repository import Gdk

# \n{{position}}
now_playing_fabricator = Fabricator(poll_from=r"playerctl -F metadata --format '{{album}}\n{{artist}}\n{{status}}\n{{title}}\n{{volume}}'", stream=True)


class NowPlaying(Button):
    def __init__(self):
        self.label = Label("Nothing is playing",)
        now_playing_fabricator.connect("changed", lambda *args: self.label.set_label(self.find_label(*args)))
        super().__init__(on_scroll_event=self.on_scroll,
                         on_button_press_event=self.on_click,
                         child=self.label,
                         #style="margin-right: 150px;"
                         )
        self.add_events(Gdk.EventMask.SCROLL_MASK)

    @staticmethod
    def find_label(fabricator, value):
        try:
            album, artist, status, title, volume = value.split(r"\n")
            return (
                f"{artist} - {title}" if album  # if its jellyfin
                else f"{artist.replace(" - Topic", "")} - {title}" if artist.endswith(" - Topic")  # if its youtube and artist/channel name has "topic"
                else title
            )
        except ValueError:
            return "Nothing is playing"

    @staticmethod
    def on_scroll(widget, event):
        match not event.direction:
            case 0:
                exec_shell_command("playerctl previous")
            case 1:
                exec_shell_command("playerctl next")

    @staticmethod
    def on_click(widget, event):
        match event.button:
            case 1:
                exec_shell_command("playerctl play-pause")
            case 2:
                exec_shell_command("playerctl stop")
