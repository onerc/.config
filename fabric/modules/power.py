from __init__ import *

class Power(Button):
    def __init__(self):
        self.is_shutdown = True
        self.is_locked = True

        self.icon_stack = Stack(transition_type="slide-up-down", transition_duration=transition_duration)
        self.label_stack = Stack(transition_type="slide-up-down", transition_duration=transition_duration)
        self.label_stack.set_sensitive(False)
        for i in ["Shutdown", "Reboot"]:
            self.icon_stack.add_named(Image(icon_name=f"system-{i.lower()}-symbolic", icon_size=icon_size, name="icon"), name=i)
            self.label_stack.add_named(Label(label=i, name="powerLabel"), name=i)

        self.revealer = Revealer(
            transition_type="slide-left",
            transition_duration=transition_duration,
            child=self.label_stack
        )
        super().__init__(
            on_enter_notify_event=lambda *args: self.revealer.set_reveal_child(True),
            on_leave_notify_event=lambda *args: self.revealer.set_reveal_child(not self.is_locked),
            on_button_press_event=lambda *args: self.lock_handler(*args, is_pressed=True),
            on_button_release_event=lambda *args: self.lock_handler(*args, is_pressed=False),
            on_clicked=lambda *args: self.on_click(),
            on_scroll_event=self.on_scroll,
            child=Box(
                children=[
                    self.icon_stack,
                    self.revealer,
                ]
            )
        )
        self.add_events("scroll")

    def on_click(self):
        if not self.is_locked:
            exec_shell_command_async("shutdown now" if self.is_shutdown else "reboot")

    def on_scroll(self, widget, event):
        self.is_shutdown = not event.direction
        self.icon_stack.set_visible_child_name("Shutdown" if self.is_shutdown else "Reboot")
        self.label_stack.set_visible_child_name("Shutdown" if self.is_shutdown else "Reboot")

    def lock_handler(self, widget, event, is_pressed):
        if event.button == 3:
            self.is_locked = not is_pressed
            self.label_stack.set_sensitive(is_pressed)

