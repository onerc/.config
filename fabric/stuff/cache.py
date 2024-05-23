from fabric.widgets.box import Box
from fabric.widgets.button import Button
from fabric.widgets.image import Image
from fabric.widgets.label import Label
from fabric.widgets.revealer import Revealer

from fabric.utils.fabricator import Fabricator

from gi.repository import Gtk

dirty_fabricator = Fabricator(poll_from="grep Dirty: /proc/meminfo", interval=1000)


class Cache(Button):
    def __init__(self):
        self.is_pinned = False

        self.label = Label(name="cacheLabel")
        self.button_icon = Image(name="revealerIcon", icon_name="drive-removable-media-symbolic", icon_size=Gtk.IconSize(1))
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

        dirty_fabricator.connect("changed", self.update_label)

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
        self.label.set_label(cache)
        return True
