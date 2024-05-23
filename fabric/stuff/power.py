from fabric.widgets.box import Box
from fabric.widgets.button import Button
from fabric.widgets.image import Image
from fabric.widgets.label import Label
from fabric.widgets.revealer import Revealer

from fabric.utils import exec_shell_command

from gi.repository import Gtk, Gdk


class Power(Button):
    def __init__(self):
        self.is_locked = True
        self.is_shutdown = True
        self.icon = Image(name="revealerIcon", icon_name="system-shutdown-symbolic", icon_size=Gtk.IconSize(1))
        self.label = Label("Locked", name="powerLabel")
        self.revealer = Revealer(
            transition_type="slide-right",
            children=self.label
        )
        super().__init__(
            on_enter_notify_event=lambda *args: self.revealer.set_reveal_child(True),
            on_leave_notify_event=lambda *args: self.revealer.set_reveal_child(False) if self.is_locked else None,
            on_button_press_event=lambda *args: self.lock_handler(*args, False),
            on_button_release_event=lambda *args: self.lock_handler(*args, True),
            on_clicked=lambda *args: exec_shell_command("shutdown now" if self.is_shutdown else "reboot") if not self.is_locked else None,
            on_scroll_event=self.on_scroll,
            child=Box(
                children=[
                    self.icon,
                    self.revealer,
                ]
            )
        )
        self.add_events(Gdk.EventMask.SCROLL_MASK)

    def on_scroll(self, widget, event):
        self.is_shutdown = event.direction
        self.icon.set_from_icon_name(f"system-{self.find_label().lower()}-symbolic", Gtk.IconSize(1))
        if not self.is_locked:
            self.label.set_label(self.find_label())

    def find_label(self):
        return "Shutdown" if self.is_shutdown else "Reboot"

    def lock_handler(self, widget, event, is_released):
        if event.button == 3:
            self.is_locked = is_released
            self.label.set_label("Locked" if is_released else self.find_label())
