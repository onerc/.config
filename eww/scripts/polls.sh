while true; do
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

get_signal_status() {

if $(hyprctl clients -j | jq '.[] | select(.class=="Signal") | .title=="Signal"'); then
    status=""
else
    status=""

fi

}
##########################################################################################################################################################################################################################################
case $1 in
    playpause)
        get_play_pause_logo;;
    nowplaying)
        get_now_playing;;
    signalstatus)
        get_signal_status;;
    *)
        status="Wrong arg"
esac

if [[ $previous != $status ]]; then
    previous=$status
    echo $status
fi
sleep 0.2
done
