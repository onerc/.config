while true; do
if [[ $(playerctl -s status) == "" ]]; then
	status=""
else
	if [[ $(playerctl -s metadata album) != "" ]]; then # if jellyfin is playing
		status="$(playerctl -s metadata artist) - $(playerctl -s metadata title)"
	elif [[ $(playerctl -s metadata artist) =~ " - Topic" ]]; then # if its youtube and artist name has "topic"
		status="$(playerctl -s metadata artist | rev | cut -c 9- | rev) - $(playerctl -s metadata title)" # dunno if bash has negative slicing
	else
		status=$(playerctl -s metadata title)
	fi
fi

if [[ $status != $previous ]]; then
     echo $status
     previous=$status
fi

sleep 0.2
done
