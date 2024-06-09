from fabric.widgets import Box, Button, Image, Label, Revealer, Stack
from fabric.utils import invoke_repeater
from gi.repository import Gtk
import psutil

network_interface = "enp6s0"


class Network(Button):
    def __init__(self):
        self.is_pinned = False

        self.label = Label(name="revealerLabel")

        self.stack = Stack(transition_type="slide-up-down")
        for i in ["network-wired-acquiring", "network-wired", "network-wired-disconnected", "lock"]:
            self.stack.add_named(Image(icon_name=f"{i}-symbolic", icon_size=Gtk.IconSize(1), name="revealerIcon"), name=i)

        self.revealer = Revealer(
            children=self.label,
            transition_type="slide-left"
        )
        super().__init__(
            on_clicked=self.toggle_pin,
            on_enter_notify_event=lambda *args: self.revealer.set_reveal_child(True),
            on_leave_notify_event=lambda *args: self.revealer.set_reveal_child(False) if not self.is_pinned else None,
            child=Box(
                children=[
                    self.stack,
                    self.revealer
                ]
            )
        )

        invoke_repeater(1000, self.update_label_and_icon)

    def toggle_pin(self, *args):
        self.is_pinned = not self.is_pinned
        self.stack.set_visible_child_name("lock" if self.is_pinned else self.find_icon())

    # todo bandwidth usage
    # maybe todo interface speed

    def update_label_and_icon(self, *args):
        self.label.set_label(psutil.net_if_addrs()[network_interface][0].address if psutil.net_if_stats()[network_interface].isup else "N/A")
        if not self.is_pinned:
            self.stack.set_visible_child_name(self.find_icon())
        return True

    @staticmethod
    def find_icon():
        return "network-wired" if psutil.net_if_stats()[network_interface].isup else "network-wired-disconnected"
