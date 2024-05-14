import psutil
import fabric
from fabric.widgets.box import Box
from fabric.widgets.button import Button
from fabric.widgets.centerbox import CenterBox
from fabric.widgets.date_time import DateTime
from fabric.widgets.image import Image
from fabric.widgets.label import Label
from fabric.widgets.revealer import Revealer
from fabric.widgets.wayland import Window
#from fabric.widgets.window import Window

from gi.repository import Gtk, Gdk

from fabric.utils import exec_shell_command
from fabric.utils import invoke_repeater

from fabric.utils.fabricator import Fabricator

from fabric.hyprland.widgets import WorkspaceButton, Workspaces

from fabric.audio.service import Audio
# \n{{position}}
nowPlayingFabricator = Fabricator(poll_from=r"playerctl -F metadata --format '{{album}}\n{{artist}}\n{{status}}\n{{title}}\n{{volume}}'", stream=True)
dirtyFabricator = Fabricator(poll_from="grep Dirty: /proc/meminfo", interval=1000)
unwantedSink = "alsa_output.pci-0000_00_1f.3.iec958-stereo"


class NowPlaying(Button):
    def __init__(self):
        self.label = Label()
        nowPlayingFabricator.connect("changed", self.update_label)
        super().__init__(on_scroll_event=self.on_scroll,
                         on_button_press_event=self.on_click,
                         child=self.label
                         )
        self.add_events(Gdk.EventMask.SCROLL_MASK)

    def update_label(self, fabricator, value):
        album, artist, status, title, volume = value.split(r"\n")
        if album:  # if its jellyfin
            self.label.set_label(f"{artist} - {title}")
        elif " - Topic" in artist:  # if its youtube and artist/channel name has "topic"
            self.label.set_label(f"{artist.replace(" - Topic", "")} - {title}")
        else:
            self.label.set_label(title)

    @staticmethod
    def on_scroll(widget, event):
        match event.direction:
            case 0:
                exec_shell_command("playerctl next")
            case 1:
                exec_shell_command("playerctl previous")

    @staticmethod
    def on_click(widget, event):
        match event.button:
            case 1:
                exec_shell_command("playerctl play-pause")
            case 2:
                exec_shell_command("playerctl stop")


class SpeakerVolume(Button):
    def __init__(self, **kwargs):
        self.audio = Audio(on_speaker_changed=self.update_label_and_icon)
        self.label = Label()
        self.revealer = Revealer(
            children=self.label,
            transition_type="slide-right"
        )
        self.icon = Image()

        super().__init__(
            on_clicked=self.mute,
            on_scroll_event=self.on_scroll,
            on_enter_notify_event=lambda *args: self.revealer.set_reveal_child(True),
            on_leave_notify_event=lambda *args: self.revealer.set_reveal_child(False),
            child=Box(
                children=[
                    self.icon,
                    self.revealer,
                ]
            ),
            **kwargs
        )
        self.add_events(Gdk.EventMask.SCROLL_MASK)

    def on_scroll(self, widget, event):
        if self.audio.speaker.name != unwantedSink:
            match event.direction:
                case 0:
                    self.audio.speaker.volume += 10
                case 1:
                    self.audio.speaker.volume -= 10

    def mute(self, *args):
        self.audio.speaker.is_muted = not self.audio.speaker.is_muted

    def update_label_and_icon(self, *args):
        self.label.set_label(f"%{round(self.audio.speaker.volume)}" if self.audio.speaker.name != unwantedSink else "N/A")
        self.icon.set_from_icon_name(f"audio-volume-{self.lookup_icon_name()}-symbolic" if self.audio.speaker.name != unwantedSink else "audio-volume-muted-symbolic", Gtk.IconSize(1))

    def lookup_icon_name(self):
        if self.audio.speaker.is_muted:
            return "muted"
        return (
            "overamplified" if (volume := self.audio.speaker.volume) >= 99
            else "high" if volume >= 66
            else "medium" if volume >= 33
            else "low" if volume >= 1
            else "muted"
        )


class MicVolume(Button):
    def __init__(self, **kwargs):
        self.audio = Audio(on_microphone_changed=self.update_label_and_icon)
        self.label = Label()
        self.revealer = Revealer(
            children=self.label,
            transition_type="slide-right"
        )
        self.icon = Image()

        super().__init__(
            on_clicked=self.mute,
            on_scroll_event=self.on_scroll,
            on_enter_notify_event=lambda *args: self.revealer.set_reveal_child(True),
            on_leave_notify_event=lambda *args: self.revealer.set_reveal_child(False),
            child=Box(
                children=[
                    self.icon,
                    self.revealer,
                ]
            ),
            **kwargs
        )
        self.add_events(Gdk.EventMask.SCROLL_MASK)

    def on_scroll(self, widget, event):
        match event.direction:
            case 0:
                self.audio.microphone.volume += 10
            case 1:
                self.audio.microphone.volume -= 10

    def mute(self, *args):
        self.audio.microphone.is_muted = not self.audio.microphone.is_muted

    def update_label_and_icon(self, *args):
        self.label.set_label(f"%{round(self.audio.microphone.volume)}")
        self.icon.set_from_icon_name(f"microphone-sensitivity-{self.lookup_icon_name()}-symbolic", Gtk.IconSize(1))

    def lookup_icon_name(self):
        if self.audio.microphone.is_muted:
            return "muted"
        return (
            "high" if (volume := self.audio.microphone.volume) >= 66
            else "medium" if volume >= 33
            else "low" if volume >= 1
            else "muted"
        )


class AudioOutputSwitch(Button):
    def __init__(self, **kwargs):
        self.audio = Audio(on_speaker_changed=self.update_icon)
        self.icon = Image()
        super().__init__(
            on_clicked=self.switch_output,
            child=self.icon,
            **kwargs
        )

    def update_icon(self, *args):
        match self.audio.speaker.description:
            case "Built-in Audio Analog Stereo":
                self.icon.set_from_icon_name("audio-headphones-symbolic", Gtk.IconSize(1))
            case "Navi 21/23 HDMI/DP Audio Controller Digital Stereo (HDMI)":
                self.icon.set_from_icon_name("video-display-symbolic", Gtk.IconSize(1))
            case _:
                self.icon.set_from_icon_name("dialog-error-symbolic", Gtk.IconSize(1))

    def switch_output(self, *args):
        for i in self.audio.speakers:
            if i != self.audio.speaker:
                exec_shell_command(f"pactl set-default-sink {i.name}")


class HardwareUsage(Button):
    def __init__(self, **kwargs):
        self.is_pinned = False

        self.left_icon = Image(icon_name="cpu-symbolic", icon_size=Gtk.IconSize(1))
        self.left_label = Label()
        self.left_revealer = Revealer(
            children=Box(
                children=[
                    self.left_icon,
                    self.left_label
                ]
            ),
            transition_type="slide-left"
        )

        self.button_icon = Image(icon_name="edit-find-symbolic", icon_size=Gtk.IconSize(1))

        self.right_icon = Image(icon_name="ram-symbolic", icon_size=Gtk.IconSize(1))
        self.right_label = Label()
        self.right_revealer = Revealer(
            children=Box(
                children=[
                    self.right_label,
                    self.right_icon
                ]
            ),
            transition_type="slide-right")
        super().__init__(
            on_clicked=self.toggle_pin,
            on_leave_notify_event=self.unreveal,
            on_enter_notify_event=self.reveal,
            child=Box(
                children=[
                    self.left_revealer,
                    self.button_icon,
                    self.right_revealer
                ]
            ),
            **kwargs
        )
        invoke_repeater(1000, self.update_labels)

    def toggle_pin(self, *args):
        self.is_pinned = not self.is_pinned
        self.button_icon.set_from_icon_name("lock-symbolic" if self.is_pinned else "edit-find-symbolic", Gtk.IconSize(1))

    def unreveal(self, *args):
        if not self.is_pinned:
            self.left_revealer.set_reveal_child(False),
            self.right_revealer.set_reveal_child(False)

    def reveal(self, *args):
        self.left_revealer.set_reveal_child(True),
        self.right_revealer.set_reveal_child(True)

    def update_labels(self):
        self.left_label.set_label(f"{round(psutil.cpu_percent())}%")
        self.right_label.set_label(f"{round(psutil.virtual_memory().percent)}%")
        return True


class HardwareTemps(Button):
    def __init__(self, **kwargs):
        self.is_pinned = False

        self.left_icon = Image(icon_name="cpu-symbolic", icon_size=Gtk.IconSize(1))
        self.left_label = Label()
        self.left_revealer = Revealer(
            children=Box(
                children=[
                    self.left_icon,
                    self.left_label
                ]
            ),
            transition_type="slide-left"
        )

        self.button_icon = Image(icon_name="temp-symbolic", icon_size=Gtk.IconSize(1))

        self.right_icon = Image(icon_name="freon-gpu-temperature-symbolic", icon_size=Gtk.IconSize(1))
        self.right_label = Label()
        self.right_revealer = Revealer(
            children=Box(
                children=[
                    self.right_label,
                    self.right_icon
                ]
            ),
            transition_type="slide-right")
        super().__init__(
            on_clicked=self.toggle_pin,
            on_leave_notify_event=self.unreveal,
            on_enter_notify_event=self.reveal,
            child=Box(
                children=[
                    self.left_revealer,
                    self.button_icon,
                    self.right_revealer
                ]
            ),
            **kwargs
        )
        invoke_repeater(1000, self.update_labels)

    def toggle_pin(self, *args):
        self.is_pinned = not self.is_pinned
        self.button_icon.set_from_icon_name("lock-symbolic" if self.is_pinned else "temp-symbolic", Gtk.IconSize(1))

    def unreveal(self, *args):
        if not self.is_pinned:
            self.left_revealer.set_reveal_child(False),
            self.right_revealer.set_reveal_child(False)

    def reveal(self, *args):
        self.left_revealer.set_reveal_child(True),
        self.right_revealer.set_reveal_child(True)

    def update_labels(self):
        self.left_label.set_label(f"{round(psutil.sensors_temperatures()['coretemp'][0].current)}°C")
        self.right_label.set_label(f"{round(psutil.sensors_temperatures()['amdgpu'][1].current)}°C")
        return True


class Cache(Button):
    def __init__(self):
        self.is_pinned = False

        self.label = Label("test")
        self.button_icon = Image(icon_name="drive-removable-media-symbolic", icon_size=Gtk.IconSize(1))
        self.revealer = Revealer(
            children=self.label,
            transition_type="slide-left"
        )
        super().__init__(
            on_clicked=self.toggle_pin,
            on_enter_notify_event=lambda *args: self.revealer.set_reveal_child(True),
            on_leave_notify_event=self.unreveal,
            child=Box(
                children=[
                    self.button_icon,
                    self.revealer
                ]
            )
        )

        dirtyFabricator.connect("changed", self.update_label)

    def unreveal(self, *args):
        if not self.is_pinned:
            self.revealer.set_reveal_child(False),

    def toggle_pin(self, *args):
        self.is_pinned = not self.is_pinned
        self.button_icon.set_from_icon_name("lock-symbolic" if self.is_pinned else "drive-removable-media-symbolic", Gtk.IconSize(1))

    def update_label(self, fabricator, value):
        cache = int(value.split()[1])
        if cache >= 1048576:
            cache = f"{round(cache / 1048576, 1)} GB"
        elif cache >= 1024:
            cache = f"{round(cache / 1024, 1)} MB"
        else:
            cache = f"{cache} KB"
        self.label.set_label(str(cache))
        return True


class barbar(Window):
    def __init__(self):
        super().__init__(
            layer="top",
            anchor="left top right",
        )
        self.centerbox = CenterBox()
        self.media_box = Box(
            children=[
                Cache(),
                MicVolume(),
                SpeakerVolume(),
                AudioOutputSwitch()
            ]
        )
        self.workspaces = Workspaces(
            buttons_list=[WorkspaceButton() for _ in range(10)]
        )
        self.centerbox.add_start(
            CenterBox(start_children=self.workspaces, center_children=Box(children=[HardwareTemps(), HardwareUsage()]))
        )
        self.centerbox.add_center(DateTime(["%H:%M", "%A | %m.%d.%Y"]))
        self.centerbox.add_end(
            CenterBox(center_children=NowPlaying(), end_children=self.media_box)
        )
        self.add(self.centerbox)
        self.show_all()


if __name__ == "__main__":
    bar = barbar()
    fabric.start()
