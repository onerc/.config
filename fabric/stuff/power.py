from fabric.widgets import Box, Button, Image, Label, Revealer, Stack
from fabric.utils import exec_shell_command
from gi.repository import Gtk, Gdk


class Power(Button):
    def __init__(self):
        self.is_locked = True
        self.is_shutdown = True

        self.icon_stack = Stack(transition_type="slide-up-down")
        for i in ["shutdown", "reboot"]:
            self.icon_stack.add_named(Image(icon_name=f"system-{i}-symbolic", icon_size=Gtk.IconSize(1), name="revealerIcon"), name=i)

        self.label_stack = Stack()
        for i in ["Locked", "Shutdown", "Reboot"]:
            self.label_stack.add_named(Label(label=i, name="powerLabel"), name=i)

        self.revealer = Revealer(
            transition_type="slide-left",
            children=self.label_stack
        )
        super().__init__(
            on_enter_notify_event=lambda *args: self.revealer.set_reveal_child(True),
            on_leave_notify_event=lambda *args: self.revealer.set_reveal_child(False) if self.is_locked else None,
            on_button_press_event=lambda *args: self.lock_handler(*args, is_released=False),
            on_button_release_event=lambda *args: self.lock_handler(*args, is_released=True),
            on_clicked=lambda *args: exec_shell_command("shutdown now" if self.is_shutdown else "reboot") if not self.is_locked else None,
            on_scroll_event=self.on_scroll,
            child=Box(
                children=[
                    self.icon_stack,
                    self.revealer,
                ]
            )
        )
        self.add_events(Gdk.EventMask.SCROLL_MASK)

    def on_scroll(self, widget, event):
        self.is_shutdown = not event.direction
        self.icon_stack.set_visible_child_name(self.find_label().lower())
        if not self.is_locked:
            self.label_stack.set_transition_type("slide-up-down")
            self.label_stack.set_visible_child_name(self.find_label())

    def find_label(self):
        return "Shutdown" if self.is_shutdown else "Reboot"

    def lock_handler(self, widget, event, is_released):
        if event.button == 3:
            self.is_locked = is_released
            self.label_stack.set_transition_type("none")
            self.label_stack.set_visible_child_name("Locked" if self.is_locked else self.find_label())

