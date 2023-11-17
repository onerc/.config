while true; do
currentvolume=$(pactl get-source-volume @DEFAULT_SOURCE@ | awk '{print $5}' | tr -d '%\n')
if [ $(pactl get-source-mute @DEFAULT_SOURCE@ | awk '{print $2}') == "yes" ]  || [ $currentvolume == 0 ]; then
        status=""
else
        status=""
fi

if [[ $status != $previous ]]; then
     echo $status
     previous=$status
fi

sleep 0.2
done
