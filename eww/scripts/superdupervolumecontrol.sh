uppercased_arg=$(echo $1 | tr "[:lower:]" "[:upper:]")
current_volume=$(pactl get-$1-volume @DEFAULT_$uppercased_arg@ | awk 'NR==1{print $5/1}')
case $2 in
    up)
        if (( $current_volume >= 90)); then
            pactl set-$1-volume @DEFAULT_$uppercased_arg@ 100%
        else
            pactl set-$1-volume @DEFAULT_$uppercased_arg@ +10%
        fi
        ;;
    down)
        pactl set-$1-volume @DEFAULT_$uppercased_arg@ -10%
        ;;
esac
