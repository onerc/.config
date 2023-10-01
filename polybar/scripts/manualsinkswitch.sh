activesink=$(pacmd list-sinks | awk '/* index/ {print $3}')
nameofthesink=$(pactl list sinks short | awk "/^$activesink/"'{print $2}')

if [[ $nameofthesink =~ "hdmi" ]]; then
        echo ""
elif [[ $nameofthesink =~ "analog" ]]; then
        echo ""
else
        echo ""
fi
