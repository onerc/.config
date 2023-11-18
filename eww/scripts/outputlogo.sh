#fixme

while true; do
activesink=$(pactl get-default-sink)
if [[ $activesink =~ "hdmi" ]]; then
        echo ""
elif [[ $activesink =~ "analog" ]]; then
        echo ""
else
        echo ""
fi

if [[ $status != $previous ]]; then
     echo $status
     previous=$status
fi

sleep 0.2
done
