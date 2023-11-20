multipliedvolume="${2}0"
case $1 in
    "sink")
    pactl set-sink-volume @DEFAULT_SINK@ $multipliedvolume%;;
    "source")
    pactl set-source-volume @DEFAULT_SOURCE@ $multipliedvolume%;;
esac
