while true; do

get_audio_stuff() {

uppercased_arg=$(echo $1 | tr "[:lower:]" "[:upper:]")
current_volume=$(pactl get-$1-volume @DEFAULT_$uppercased_arg@ | awk 'NR==1{print $5/1}')
mute_status=$(pactl get-$1-mute @DEFAULT_$uppercased_arg@ | awk '{print $2}')
if [[ $2 == "logo" ]]; then
    case $1 in
        sink)
            if [ $mute_status == "yes" ] || [ $current_volume == 0 ]; then
                status=""
            elif (( $current_volume <= 33 )); then
                status=""
            elif (( $current_volume <= 66 )); then
                status=""
            else
                status=""
            fi
            ;;
        source)
            if [ $mute_status == "yes" ] || [ $current_volume == 0 ]; then
                status=""
            else
                status=""
            fi
            ;;
    esac
else
    status=$current_volume
fi

}
##########################################################################################################################################################################################################################################

get_output_logo() {

case $(pactl get-default-sink) in
    *hdmi*)
        status="";;
    *analog*)
        status="";;
    *)
        status="";;
esac

}
##########################################################################################################################################################################################################################################

get_play_pause_logo() {

case $(playerctl -s status) in
    Playing)
        status="";;
    Paused)
        status="";;
    *)
        status="";;
esac

}
##########################################################################################################################################################################################################################################

get_now_playing() {

if [ -z $(playerctl -s status) ]; then
    status=""
elif [[ ! -z $(playerctl -s metadata album) || $(playerctl metadata -s artist) =~ " - Topic" ]]; then # if album isnt empty, aka jellyfin is playing or if its youtube and the channel name has "topic"
    fixedartist=$(playerctl metadata artist | sed 's/ - Topic//')
    status=$(playerctl metadata --format "$fixedartist - {{title}}")
else
    status=$(playerctl -s metadata title)
fi

}
##########################################################################################################################################################################################################################################

get_internet_status() {

if ping -c 1 -W 3 ping.archlinux.org > /dev/null; then
	status=""
else
	status=""
fi

}
##########################################################################################################################################################################################################################################

get_signal_status() {

if $(hyprctl clients -j | jq '.[] | select(.class=="Signal") | .title=="Signal"'); then
	status=""
else
	status=""

fi

}
##########################################################################################################################################################################################################################################

case $1 in
    sink|source)
        get_audio_stuff $1 $2;;
    outputlogo)
        get_output_logo;;
	playpause)
		get_play_pause_logo;;
	nowplaying)
		get_now_playing;;
	internetlogo)
		get_internet_status;;
	signalstatus)
		get_signal_status;;
	*)
		status="Wrong arg";;
esac

if [[ $previous != $status ]]; then
    previous=$status
   	echo $status
fi

case $1 in
	sink | source)
		sleep 0.1;;
	internetlogo)
		sleep 3;;
	*)
		sleep 0.2;;

esac

done
