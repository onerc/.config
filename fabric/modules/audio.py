from __init__ import *


class SpeakerVolume(Button):
    def __init__(self):
        self.audio = Audio(on_speaker_changed=self.label_and_icon_handler)

        self.icon_stack = Stack(transition_type="slide-up-down", transition_duration=transition_duration)
        for i in ["overamplified", "high", "medium", "low", "muted"]:
            self.icon_stack.add_named(Image(icon_name=f"audio-volume-{i}-symbolic", icon_size=icon_size, name="icon"), name=i)

        self.label_stack = Stack(transition_type="slide-up-down", transition_duration=transition_duration)
        for i in range(100, -10, -10):
            self.label_stack.add_named(Label(label=f"%{i}", name="revealerLabel"), name=f"{i}")

        self.revealer = Revealer(
            child=self.label_stack,
            transition_type="slide-left",
            transition_duration = transition_duration
        )

        super().__init__(
            on_clicked=self.toggle_mute,
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
        self.add_events("scroll")

    def on_scroll(self, widget, event):
        if self.audio.speaker.name != config["unwanted_sink"]:
            match not event.direction:
                case 0:
                    self.audio.speaker.volume -= 10
                case 1:
                    self.audio.speaker.volume += 10

    def toggle_mute(self, *args):
        self.audio.speaker.muted = not self.audio.speaker.muted

    def label_and_icon_handler(self, *args):
        if self.audio.speaker.name == config["unwanted_sink"]:
            label="N/A"
            icon="muted"
        else:
            label=f"{round(self.audio.speaker.volume)}"
            icon=self.find_icon_name()

        self.label_stack.set_visible_child_name(label)
        self.icon_stack.set_visible_child_name(icon)

    def find_icon_name(self):
        if self.audio.speaker.muted:
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
        self.audio = Audio(on_microphone_changed=self.label_and_icon_handler)

        self.icon_stack = Stack(transition_type="slide-up-down", transition_duration=transition_duration)
        for i in ["high", "medium", "low", "muted"]:
            self.icon_stack.add_named(Image(icon_name=f"microphone-sensitivity-{i}-symbolic", icon_size=icon_size, name="icon"), name=i)

        self.label_stack = Stack(transition_type="slide-up-down", transition_duration=transition_duration)
        for i in range(100, -10, -10):
            self.label_stack.add_named(Label(label=f"%{i}", name="revealerLabel"), name=f"{i}")
        self.label_stack.add_named(Label(label="N/A", name="revealerLabel"), name="N/A")

        self.revealer = Revealer(
            child=self.label_stack,
            transition_type="slide-left",
            transition_duration=transition_duration
        )

        super().__init__(
            on_clicked=self.toggle_mute,
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
        self.add_events("scroll")

    def on_scroll(self, widget, event):
        if self.audio.microphone:
            match event.direction:
                case 1:
                    self.audio.microphone.volume -= 10
                case 0:
                    self.audio.microphone.volume += 10
        else:
            self.mic_not_found()

    def toggle_mute(self, *args):
        if self.audio.microphone:
            self.audio.microphone.muted = not self.audio.microphone.muted
        else:
            self.mic_not_found()

    def label_and_icon_handler(self, *args):
        self.label_stack.set_visible_child_name(f"{round(self.audio.microphone.volume)}")
        self.icon_stack.set_visible_child_name(self.find_icon_name())

    def find_icon_name(self):
        if self.audio.microphone.muted:
            return "muted"
        return (
            "high" if (volume := self.audio.microphone.volume) >= 66
            else "medium" if volume >= 33
            else "low" if volume >= 1
            else "muted"
        )

    def mic_not_found(self):
        self.label_stack.set_visible_child_name("N/A")
        self.icon_stack.set_visible_child_name("muted")


class AudioOutputSwitch(Button):
    def __init__(self):
        self.audio = Audio(on_speaker_changed=self.icon_handler)

        self.stack = Stack(transition_type="slide_up_down", transition_duration=transition_duration)
        for i in ["video-display", "audio-headphones", "dialog-error"]:
            self.stack.add_named(Image(icon_name=f"{i}-symbolic", icon_size=icon_size), name=i)

        super().__init__(
            on_clicked=self.switch_output,
            child=self.stack,
        )

    def icon_handler(self, *args):
        icon_dict = {
            "Built-in Audio Analog Stereo": "audio-headphones",
            "Navi 21/23 HDMI/DP Audio Controller Digital Stereo (HDMI)": "video-display",
            "Built-in Audio Digital Stereo (IEC958)": "dialog-error"
        }
        self.stack.set_visible_child_name(icon_dict[self.audio.speaker.description])

    def switch_output(self, *args):
        for speaker in self.audio.speakers:
            if speaker != self.audio.speaker:
                exec_shell_command_async(f"pactl set-default-sink {speaker.name}")
#                for sink_input in exec_shell_command("pactl list sink-inputs short").splitlines():
#                    exec_shell_command(f"pactl move-sink-input {sink_input.split()[0]} {speaker.name}")
