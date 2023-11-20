while true; do
activesink=$(pactl get-default-sink)
case $activesink in
    *"hdmi"*)
        status="";;
    *"analog"*)
        status="";;
    *)
        status="";;
esac

if [[ $status != $previous ]]; then
     echo $status
     previous=$status
fi

sleep 0.2
done
