monitor=$(pactl list sinks short | awk '/hdmi/{print $1}')
headphone=$(pactl list sinks short | awk '/analog/{print $1}')

if [[ $(pactl list sinks short) =~ "iec958" ]]; then
       echo ""
       pactl set-default-sink $monitor
else
       echo ""
       pactl set-default-sink $headphone > /dev/null 2>&1 # it takes few seconds for pulseaudio to realize the output has changed
fi
