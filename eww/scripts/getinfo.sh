while true; do
get_source_logo(){

current_volume=$(pactl get-source-volume @DEFAULT_SOURCE@ | awk 'NR==1{print $5/1}') # divide by 1 to get rid of percentage sign without tr command :P
mute_status=$(pactl get-source-mute @DEFAULT_SOURCE@ | awk '{print $2}')
if [ $mute_status == "yes" ] || [ $current_volume == 0 ]; then
		status=""
else
		status=""
fi

}
###########################################################################################################################################################################################################################################
get_sink_logo() {

current_volume=$(pactl get-sink-volume @DEFAULT_SINK@ | awk 'NR==1{print $5/1}') # divide by 1 to get rid of percentage sign without tr command :P
mute_status=$(pactl get-sink-mute @DEFAULT_SINK@ | awk '{print $2}')
if [ $mute_status == "yes" ] || [ $current_volume == 0 ]; then
        status=""
else
    if (( $current_volume <= 33 )); then
        status=""
    elif (( $current_volume <= 66 )); then
        status=""
    else
        status=""
    fi
fi

}
###########################################################################################################################################################################################################################################
get_output_logo() {

case $(pactl get-default-sink) in
    *"hdmi"*)
        status="";;
    *"analog"*)
        status="";;
    *)
        status="";;
esac

}
###########################################################################################################################################################################################################################################
get_play_pause_logo() {

case $(playerctl -s status) in
    "Playing")
        status="";;
    "Paused")
        status="";;
    *)
        status="";;
esac

}
###########################################################################################################################################################################################################################################
get_now_playing() {

if [[ $(playerctl -s status) == "" ]]; then
    status=""
else
    if [[ $(playerctl metadata album) != "" ]]; then # if jellyfin is playing
        status=$(playerctl metadata --format "{{artist}} - {{title}}")
    elif [[ $(playerctl metadata artist) =~ " - Topic" ]]; then # if its youtube and artist name has "topic"
        fixedartist=$(playerctl metadata artist | rev | cut -c 9- | rev) # dunno if bash has negative slicing
        status=$(playerctl metadata --format "$fixedartist - {{title}}")
    else
        status=$(playerctl metadata title)
    fi
fi

}
###########################################################################################################################################################################################################################################
case $1 in
	"source")
		get_source_logo;;
	"sink")
		get_sink_logo;;
	"output")
		get_output_logo;;
	"playpause")
		get_play_pause_logo;;
	"nowplaying")
		get_now_playing;;
esac
if [[ $previous != $status ]]; then
    previous=$status
    echo $status
fi
sleep 0.2
done
