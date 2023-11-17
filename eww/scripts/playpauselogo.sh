while true; do
playerstatus=$(playerctl -s status)
if [[ $playerstatus == "Playing" ]]; then
	status=""
elif [[ $playerstatus == "Paused" ]]; then
	status=""
else
	status=""
fi

if [[ $status != $previous ]]; then
     echo $status
     previous=$status
fi

sleep 0.2
done
