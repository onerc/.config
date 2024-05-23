import psutil

from fabric.widgets.box import Box
from fabric.widgets.button import Button
from fabric.widgets.image import Image
from fabric.widgets.label import Label
from fabric.widgets.revealer import Revealer

from fabric.utils import invoke_repeater

from gi.repository import Gtk

network_interface = "enp6s0"


class Network(Button):
    def __init__(self):
        self.is_pinned = False

        self.label = Label(name="revealerLabel")
        self.button_icon = Image(name="revealerIcon", icon_name="network-wired-acquiring-symbolic", icon_size=Gtk.IconSize(1))
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
                    self.button_icon,
                    self.revealer
                ]
            )
        )

        invoke_repeater(1000, self.update_label_and_icon)

    def toggle_pin(self, *args):
        self.is_pinned = not self.is_pinned
        self.button_icon.set_from_icon_name("lock-symbolic" if self.is_pinned else self.find_icon(), Gtk.IconSize(1))

    # todo bandwidth usage
    # maybe todo interface speed
    def update_label_and_icon(self, *args):
        self.label.set_label(psutil.net_if_addrs()[network_interface][0].address if psutil.net_if_stats()[network_interface].isup else "N/A")
        if not self.is_pinned:
            self.button_icon.set_from_icon_name(self.find_icon(), Gtk.IconSize(1))
        return True

    @staticmethod
    def find_icon():
        return "network-wired-symbolic" if psutil.net_if_stats()[network_interface].isup else "network-wired-disconnected-symbolic"
