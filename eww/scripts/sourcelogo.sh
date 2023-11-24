while true; do
currentvolume=$(pactl get-source-volume @DEFAULT_SOURCE@ | awk 'NR==1{print $5/1}') # divide by 1 to get rid of percentage sign without tr command :P
mutestatus=$(pactl get-source-mute @DEFAULT_SOURCE@ | awk '{print $2}')
if [ $mutestatus == "yes" ]  || [ $currentvolume == 0 ]; then
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
