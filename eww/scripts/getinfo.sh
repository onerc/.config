while true; do

get_volume() {

uppercased_arg=$(echo $1 | tr "[:lower:]" "[:upper:]")
status=$(pactl get-$1-volume @DEFAULT_$uppercased_arg@ | awk 'NR==1{print $5/10}')

}
##########################################################################################################################################################################################################################################

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
###########################################################################################################################################################################################################################################
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
###########################################################################################################################################################################################################################################
get_now_playing() {

if [ -z $(playerctl -s status) ]; then
    status=""
else
    if [[ ! -z $(playerctl metadata album) ]]; then # if album isnt empty, aka jellyfin is playing
        status=$(playerctl metadata --format "{{artist}} - {{title}}")
    elif [[ $(playerctl metadata artist) =~ " - Topic" ]]; then # if its youtube and artist name has "topic"
        fixedartist=$(playerctl metadata artist | rev | cut -c 9- | rev) # dunno if bash has negative slicing
        status=$(playerctl metadata --format "$fixedartist - {{title}}")
    else
        status=$(playerctl metadata title)
    fi
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
	sinkvol)
		get_volume sink;;
	sourcevol)
		get_volume source;;
	sinklogo)
		get_sink_logo;;
	sourcelogo)
		get_source_logo;;
	output)
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
	sinkvol | sinklogo | sourcevol | sourcelogo)
		sleep 0.1;;
	internetlogo)
		sleep 3;;
	*)
		sleep 0.2;;
esac

done
