from __init__ import *


class HardwareUsage(Button):
    def __init__(self):
        self.left_image = Image(icon_name="cpu-symbolic", icon_size=icon_size, name="icon")
        self.left_label = Label(label="N/A", h_expand=True, name="hardwareLabel")
        
        self.center_image = Image(icon_name="edit-find", icon_size=icon_size)
        
        self.right_label = Label(label="N/A", h_expand=True, name="hardwareLabel")
        self.right_image = Image(icon_name="ram-symbolic", icon_size=icon_size, name="icon")

        super().__init__(
            child=Box(
                children=[
                    self.left_image,
                    self.left_label,
                    self.center_image,
                    self.right_label,
                    self.right_image,
                ]
            ),
        )

        psutil_fabricator.connect("changed", self.label_handler)

    def label_handler(self, fabricator, value):
        self.left_label.set_label(value["cpu_usage"])
        self.right_label.set_label(value["ram_usage"])


class HardwareTemps(Button):
    def __init__(self):
        self.left_image = Image(icon_name="freon-gpu-temperature-symbolic", icon_size=icon_size, name="icon")
        self.left_label = Label(label="N/A", h_expand=True, name="hardwareLabel")

        self.center_image = Image(icon_name="temp", icon_size=icon_size)
        
        self.right_label = Label(label="N/A", h_expand=True, name="hardwareLabel")
        self.right_image = Image(icon_name="cpu-symbolic", icon_size=icon_size, name="icon")
        
        super().__init__(
            child=Box(
                children=[
                    self.left_image,
                    self.left_label,
                    self.center_image,
                    self.right_label,
                    self.right_image,
                ]
            ),
        )

        psutil_fabricator.connect("changed", self.label_handler)

    def label_handler(self, fabricator, value):
        self.left_label.set_label(value["gpu_temp"])
        self.right_label.set_label(value["cpu_temp"])
