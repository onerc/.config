from fabric.widgets import Box, Button, Image, Label, Revealer, Stack
from fabric.audio.service import Audio
from fabric.utils import exec_shell_command
from gi.repository import Gtk, Gdk

unwanted_sink = "alsa_output.pci-0000_00_1f.3.iec958-stereo"


class SpeakerVolume(Button):
    def __init__(self):
        self.audio = Audio(on_speaker_changed=self.update_label_and_icon)

        self.icon_stack = Stack(transition_type="slide-up-down")
        for i in ["overamplified", "high", "medium", "low", "muted"]:
            self.icon_stack.add_named(Image(icon_name=f"audio-volume-{i}-symbolic", icon_size=Gtk.IconSize(1), name="revealerIcon"), name=i)

        self.label_stack = Stack(transition_type="slide-up-down")
        for i in range(100, -10, -10):
            self.label_stack.add_named(Label(label=f"%{i}", name="revealerLabel"), name=f"{i}")

        self.revealer = Revealer(
            children=self.label_stack,
            transition_type="slide-left"
        )

        super().__init__(
            on_clicked=self.mute,
            on_scroll_event=self.on_scroll,
            on_enter_notify_event=lambda *args: self.revealer.set_reveal_child(True),
            on_leave_notify_event=lambda *args: self.revealer.set_reveal_child(False),
            child=Box(
                children=[
                    self.icon_stack,
                    self.revealer,
                ]
            ),
        )
        self.add_events(Gdk.EventMask.SCROLL_MASK)

    def on_scroll(self, widget, event):
        if self.audio.speaker.name != unwanted_sink:
            match not event.direction:
                case 0:
                    self.audio.speaker.volume -= 10
                case 1:
                    self.audio.speaker.volume += 10

    def mute(self, *args):
        self.audio.speaker.is_muted = not self.audio.speaker.is_muted

    def update_label_and_icon(self, *args):
        self.label_stack.set_visible_child_name(f"{round(self.audio.speaker.volume)}" if self.audio.speaker.name != unwanted_sink else "N/A")
        self.icon_stack.set_visible_child_name(self.find_icon_name() if self.audio.speaker.name != unwanted_sink else "muted")

    def find_icon_name(self):
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
    def __init__(self):
        self.audio = Audio(on_microphone_changed=self.update_label_and_icon)

        self.icon_stack = Stack(transition_type="slide-up-down")
        for i in ["high", "medium", "low", "muted"]:
            self.icon_stack.add_named(Image(icon_name=f"microphone-sensitivity-{i}-symbolic", icon_size=Gtk.IconSize(1), name="revealerIcon"), name=i)

        self.label_stack = Stack(transition_type="slide-up-down")
        for i in range(100, -10, -10):
            self.label_stack.add_named(Label(label=f"%{i}", name="revealerLabel"), name=f"{i}")

        self.revealer = Revealer(
            children=self.label_stack,
            transition_type="slide-left"
        )

        super().__init__(
            on_clicked=self.mute,
            on_scroll_event=self.on_scroll,
            on_enter_notify_event=lambda *args: self.revealer.set_reveal_child(True),
            on_leave_notify_event=lambda *args: self.revealer.set_reveal_child(False),
            child=Box(
                children=[
                    self.icon_stack,
                    self.revealer,
                ]
            ),
        )
        self.add_events(Gdk.EventMask.SCROLL_MASK)

    def on_scroll(self, widget, event):
        match not event.direction:
            case 0:
                self.audio.microphone.volume -= 10
            case 1:
                self.audio.microphone.volume += 10

    def mute(self, *args):
        self.audio.microphone.is_muted = not self.audio.microphone.is_muted

    def update_label_and_icon(self, *args):
        self.label_stack.set_visible_child_name(f"{round(self.audio.microphone.volume)}")
        self.icon_stack.set_visible_child_name(self.find_icon_name())

    def find_icon_name(self):
        if self.audio.microphone.is_muted:
            return "muted"
        return (
            "high" if (volume := self.audio.microphone.volume) >= 66
            else "medium" if volume >= 33
            else "low" if volume >= 1
            else "muted"
        )


class AudioOutputSwitch(Button):
    def __init__(self):
        self.audio = Audio(on_speaker_changed=self.change_icon)

        self.stack = Stack(transition_type="slide-up-down")
        for i in ["video-display", "audio-headphones", "dialog-error"]:
            self.stack.add_named(Image(icon_name=f"{i}-symbolic", icon_size=Gtk.IconSize(1)), name=i)

        super().__init__(
            on_clicked=self.switch_output,
            child=self.stack,
        )

    def change_icon(self, *args):
        match self.audio.speaker.description:
            case "Built-in Audio Analog Stereo":
                self.stack.set_visible_child_name("audio-headphones")
            case "Navi 21/23 HDMI/DP Audio Controller Digital Stereo (HDMI)":
                self.stack.set_visible_child_name("video-display")
            case "Built-in Audio Digital Stereo (IEC958)":
                self.stack.set_visible_child_name("dialog-error")

    def switch_output(self, *args):
        for speaker in self.audio.speakers:
            if speaker != self.audio.speaker:
                exec_shell_command(f"pactl set-default-sink {speaker.name}")
#                for sink_input in exec_shell_command("pactl list sink-inputs short").splitlines():
#                    exec_shell_command(f"pactl move-sink-input {sink_input.split()[0]} {speaker.name}")
