while true; do
case $(playerctl -s status) in
    "Playing")
        status="";;
    "Paused")
        status="";;
    *)
        status="";;
esac

if [[ $status != $previous ]]; then
     echo $status
     previous=$status
fi

sleep 0.2
done
