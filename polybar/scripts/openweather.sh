api_key=":)"
city=":)"
info=$(curl -s "https://api.openweathermap.org/data/2.5/weather?appid=$api_key&q=$city&units=metric")
temperature=$(echo $info | jq .main.temp | awk '{print int($0+0.5)}')
id=$(echo $info | jq .weather[].id)

case $id in
    "2"*)
    icon="";;
    "3"*)
    icon="";;
    "5"*)
    icon="";;
    "6"*)
    icon="";;
    "7"*)
    icon="";;
    "800")
    icon="";;
    "80"*)
    icon="";;
esac

sleep 5

echo "$icon $temperature°C"
