from fabric.widgets import Box, Button, Image, Label, Revealer, Stack
from fabric.utils import invoke_repeater
from gi.repository import Gtk
import psutil


class HardwareUsage(Button):
    def __init__(self):
        self.is_pinned = False

        self.stack = Stack(transition_type="slide-up-down")
        for i in ["edit-find", "lock"]:
            self.stack.add_named(Image(icon_name=f"{i}-symbolic", icon_size=Gtk.IconSize(1), name="revealerIcon"), name=i)

        self.left_image = Image(name="revealerIcon", icon_name="cpu-symbolic", icon_size=Gtk.IconSize(1))
        self.left_label = Label(name="hardwareLabel")
        self.left_revealer = Revealer(
            transition_type="crossfade",
            children=Box(
                children=[
                    self.left_image,
                    self.left_label,
                ]
            )
        )

        self.right_image = Image(name="revealerIcon", icon_name="ram-symbolic", icon_size=Gtk.IconSize(1))
        self.right_label = Label(name="hardwareLabel")
        self.right_revealer = Revealer(
            transition_type="crossfade",
            children=Box(
                children=[
                    self.right_label,
                    self.right_image,
                ]
            )
        )

        super().__init__(
            on_clicked=self.toggle_pin,
            on_leave_notify_event=self.unreveal,
            on_enter_notify_event=self.reveal,
            child=Box(
                children=[
                    self.left_revealer,
                    self.stack,
                    self.right_revealer
                ]
            ),
        )
        invoke_repeater(1000, self.update_labels)

    def toggle_pin(self, *args):
        self.is_pinned = not self.is_pinned
        self.stack.set_visible_child_name("lock" if self.is_pinned else "edit-find")

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
    def __init__(self):
        self.is_pinned = False

        self.stack = Stack(transition_type="slide-up-down")
        for i in ["temp", "lock"]:
            self.stack.add_named(Image(icon_name=f"{i}-symbolic", icon_size=Gtk.IconSize(1), name="revealerIcon"), name=i)

        self.left_image = Image(name="revealerIcon", icon_name="freon-gpu-temperature-symbolic", icon_size=Gtk.IconSize(1))
        self.left_label = Label(name="hardwareLabel")
        self.left_revealer = Revealer(
            transition_type="crossfade",
            children=Box(
                children=[
                    self.left_image,
                    self.left_label,
                ]
            )
        )

        self.right_image = Image(name="revealerIcon", icon_name="cpu-symbolic", icon_size=Gtk.IconSize(1))
        self.right_label = Label(name="hardwareLabel")
        self.right_revealer = Revealer(
            transition_type="crossfade",
            children=Box(
                children=[
                    self.right_label,
                    self.right_image,
                ]
            )
        )
        super().__init__(
            on_clicked=self.toggle_pin,
            on_leave_notify_event=self.unreveal,
            on_enter_notify_event=self.reveal,
            child=Box(
                children=[
                    self.left_revealer,
                    self.stack,
                    self.right_revealer,
                ]
            ),
        )
        invoke_repeater(1000, self.update_labels)

    def toggle_pin(self, *args):
        self.is_pinned = not self.is_pinned
        self.stack.set_visible_child_name("lock" if self.is_pinned else "temp")

    def unreveal(self, *args):
        if not self.is_pinned:
            self.left_revealer.set_reveal_child(False),
            self.right_revealer.set_reveal_child(False)

    def reveal(self, *args):
        self.left_revealer.set_reveal_child(True),
        self.right_revealer.set_reveal_child(True)

    def update_labels(self):
        self.left_label.set_label(f"{round(psutil.sensors_temperatures()['amdgpu'][1].current)}°C")
        self.right_label.set_label(f"{round(psutil.sensors_temperatures()['coretemp'][0].current)}°C")
        return True
