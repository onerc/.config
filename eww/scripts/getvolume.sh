while true; do
sinkvolume=$(pactl get-sink-volume @DEFAULT_SINK@ | awk 'NR==1{print $5/10}')
sourcevolume=$(pactl get-source-volume @DEFAULT_SOURCE@ | awk 'NR==1{print $5/10}')

if [[ $1 == "sink" ]]; then
        if [[ $sinkvolume != $previous ]]; then
             echo $sinkvolume
             previous=$sinkvolume
        fi
elif [[ $1 == "source" ]]; then
    if [[ $sourcevolume != $previous ]]; then
         echo $sourcevolume
         previous=$sourcevolume
    fi
fi


sleep 0.1
done
