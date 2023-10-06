activesink=$(pactl get-default-sink)
if [[ $activesink =~ "hdmi" ]]; then
        echo ""
elif [[ $activesink =~ "analog" ]]; then
        echo ""
else
        echo ""
fi
