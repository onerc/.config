multipliedvolume="${2}0"
if [[ $1 == "sink" ]]; then
	pactl set-sink-volume @DEFAULT_SINK@ $multipliedvolume%
elif [[ $1 == "source" ]]; then
	pactl set-source-volume @DEFAULT_SOURCE@ $multipliedvolume%
fi
