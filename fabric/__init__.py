from fabric import Application
from fabric.audio.service import Audio
from fabric.core import Fabricator
from fabric.hyprland.widgets import Workspaces, WorkspaceButton
from fabric.utils import exec_shell_command_async, get_relative_path, set_stylesheet_from_file
from fabric.widgets.box import Box
from fabric.widgets.button import Button
from fabric.widgets.centerbox import CenterBox
from fabric.widgets.datetime import DateTime
from fabric.widgets.entry import Entry
from fabric.widgets.image import Image
from fabric.widgets.label import Label
from fabric.widgets.revealer import Revealer
from fabric.widgets.stack import Stack
from fabric.widgets.wayland import WaylandWindow
from gi.repository import Gtk

from time import sleep
import psutil
import requests
from datetime import datetime

transition_duration = 250
icon_size = 16

# TODO jsonify

config = {
    "api_key" : "d07186c0c823985f93cf8b2b1dc0c387",
    "city_name" : "Balçova",
    "network_interface": "enp6s0",
    "unwanted_sink": "alsa_output.pci-0000_00_1f.3.iec958-stereo",
    "psutil_cpu": "coretemp",
    "psutil_gpu": "amdgpu"
}

def psutil_poll(fabricator):
    while True:
        yield {
            "cpu_usage": f"{round(psutil.cpu_percent())}%",
            "ram_usage": f"{round(psutil.virtual_memory().percent)}%",
            "cpu_temp": f"{round(psutil.sensors_temperatures()[config["psutil_cpu"]][0].current)}°C",
            "gpu_temp": f"{round(psutil.sensors_temperatures()[config["psutil_gpu"]][1].current)}°C",
            "is_network_up": psutil.net_if_stats()[config["network_interface"]].isup,
            "ip_address": psutil.net_if_addrs()[config["network_interface"]][0].address
        }
        sleep(1)

psutil_fabricator = Fabricator(poll_from=psutil_poll, stream=True)


def convert_kb_to_gb(number):
    return (
        f"{round(number / 1048576, 1)} GB" if number >= 1048576
        else f"{round(number / 1024, 1)} MB" if number >= 1024
        else f"{number} KB"
    )
