while true; do
currentvolume=$(pactl get-sink-volume @DEFAULT_SINK@ | awk '{print $5}' | tr -d '%\n')
if [ $(pactl get-sink-mute @DEFAULT_SINK@ | awk '{print $2}') == "yes" ]  || [ $currentvolume == 0 ]; then
        status=""
else
    if (( $currentvolume <= 33 )); then
        status=""
    elif (( $currentvolume <= 66 )); then
        status=""
    else
        status=""
    fi
fi

if [[ $status != $previous ]]; then
    echo $status
    previous=$status
fi

sleep 0.2
done
