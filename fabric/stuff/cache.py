from fabric.widgets import Box, Button, Image, Label, Revealer, Stack
from fabric.utils.fabricator import Fabricator
from gi.repository import Gtk

dirty_fabricator = Fabricator(poll_from="grep Dirty: /proc/meminfo", interval=1000)


class Cache(Button):
    def __init__(self):
        self.is_pinned = False

        self.label = Label(name="cacheLabel")

        self.stack = Stack("slide-up-down")
        for i in ["drive-removable-media", "lock"]:
            self.stack.add_named(Image(name="revealerIcon", icon_name=f"{i}-symbolic", icon_size=Gtk.IconSize(1)), name=i)

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

        dirty_fabricator.connect("changed", self.update_label)

    def toggle_pin(self, *args):
        self.is_pinned = not self.is_pinned
        self.stack.set_visible_child_name("lock" if self.is_pinned else "drive-removable-media")

    @staticmethod
    def find_label(value):
        cache = int(value.split()[1])
        return (
            f"{round(cache / 1048576, 1)} GB" if cache >= 1048576
            else f"{round(cache / 1024, 1)} MB" if cache >= 1024
            else f"{cache} KB"
        )

    def update_label(self, fabricator, value):
        self.label.set_label(self.find_label(value))
        return True
