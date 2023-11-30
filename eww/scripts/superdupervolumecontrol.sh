increase_sink_volume() {
    current_sink_volume=$(pactl get-sink-volume @DEFAULT_SINK@ | awk 'NR==1{print $5/1}')
    if (( $current_sink_volume >= 90)); then
        pactl set-sink-volume @DEFAULT_SINK@ 100%
    else
        pactl set-sink-volume @DEFAULT_SINK@ +10%
    fi
}

increase_source_volume() {
    current_source_volume=$(pactl get-source-volume @DEFAULT_SOURCE@ | awk 'NR==1{print $5/1}')
    if (( $current_source_volume >= 90)); then
        pactl set-source-volume @DEFAULT_SOURCE@ 100%
    else
        pactl set-source-volume @DEFAULT_SOURCE@ +10%
    fi
}


case $1 in
    sink-up)
        increase_sink_volume;;
    sink-down)
        pactl set-sink-volume @DEFAULT_SINK@ -10%;;
    source-up)
        increase_source_volume;;
    source-down)
        pactl set-source-volume @DEFAULT_SOURCE@ -10%
esac
