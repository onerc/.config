from __init__ import *

# \n{{position}}
now_playing_fabricator = Fabricator(poll_from=r"playerctl -F metadata --format '{{album}}\n{{artist}}\n{{status}}\n{{title}}\n{{volume}}'", stream=True)


class NowPlaying(Button):
    def __init__(self):
        self.label = Label("Nothing is playing")
        self.icon = Image(icon_name="media-playback-stop-symbolic", icon_size=icon_size, name="icon")

        super().__init__(
            on_scroll_event=self.on_scroll,
            on_button_release_event=self.on_button_press,
            child=Box(
                children=[
                    self.icon,
                    self.label,
                ]
            )
        )
        now_playing_fabricator.connect("changed", lambda *args: self.update_icon_and_label(*args))
        self.add_events("scroll")

    def update_icon_and_label(self, fabricator, value):
        self.icon.set_from_icon_name(self.find_icon(value))
        self.label.set_label(self.find_label(value))

    @staticmethod
    def find_label(value):
        try:
            album, artist, status, title, volume = value.split(r"\n")
            return (
                f"{artist} - {title}" if album  # if it's Jellyfin
                else f"{artist.replace(' - Topic', '')} - {title}" if artist.endswith(" - Topic")  # if it's YouTube and artist/channel name has "topic"
                else title
            )
        except ValueError:
            return "Nothing is playing"

    @staticmethod
    def find_icon(value):
        icon_dict = {
            "Stopped": "media-playback-stop-symbolic",
            "Paused": "media-playback-start-symbolic",
            "Playing": "media-playback-pause-symbolic"
        }
        try:
            return icon_dict[value.split(r"\n")[-3]]
        except IndexError:
            return "Stopped"

    @staticmethod
    def on_scroll(widget, event):
        match event.direction:
            case 0:
                exec_shell_command_async("playerctl next")
            case 1:
                exec_shell_command_async("playerctl previous")

    @staticmethod
    def on_button_press(widget, event):
        match event.button:
            case 1:
                exec_shell_command_async("playerctl play-pause")
            case 2:
                exec_shell_command_async("playerctl stop")
