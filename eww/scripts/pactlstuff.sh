get_audio_stuff() {
pactl subscribe | grep --line-buffered "'change' on $1 #" | while read; do
uppercased_arg=$(echo $1 | tr "[:lower:]" "[:upper:]")
current_volume=$(pactl get-$1-volume @DEFAULT_$uppercased_arg@ | awk 'NR==1{print $5/1}')
mute_status=$(pactl get-$1-mute @DEFAULT_$uppercased_arg@ | awk '{print $2}')
if [[ $2 == "icon" ]]; then  # && -n $current_volume?
    case $1 in
        sink)
            if [ $mute_status == "yes" ] || [ $current_volume == 0 ]; then
                icon=""
            elif (( $current_volume <= 33 )); then
                icon=""
            elif (( $current_volume <= 66 )); then
                icon=""
            else
                icon=""
            fi
            ;;
        source)
            if [ $mute_status == "yes" ] || [ $current_volume == 0 ]; then
                icon=""
            else
                icon=""
            fi
            ;;
    esac
    echo $icon
else
    echo $current_volume
fi
done
}

get_output_icon() {
pactl subscribe | grep --line-buffered "'change' on server #" | while read; do
case $(pactl get-default-sink) in
    *hdmi*)
        icon="";;
    *analog*)
        icon="";;
    *)
        icon="";;
esac
echo $icon
done
}

case $1 in
    sink|source)
        get_audio_stuff $1 $2;;
    outputlogo)
        get_output_icon;;
esac
