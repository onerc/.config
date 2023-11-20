while true; do
case $(pactl get-default-sink) in
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
