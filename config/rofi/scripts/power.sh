apagar="⏻  off"
suspender="  suspend"
bloquear="  lock"
logout="  logout"

dir="~/.config/rofi/scripts"
OPTIONS="${apagar}\n${suspender}\n${bloquear}\n${logout}"
ans=$(echo  "${OPTIONS}" | rofi -p "Power Options" -dmenu)
rs=$?
if [ $rs -eq 0 ]
then
    case "$ans" in
        "$apagar")
            systemctl poweroff
            ;;
        "$suspender")
            systemctl suspend
            ;;
        "$bloquear")
            betterlockscreen -l
            ;;
        "$logout")
            bspc quit
            ;;
    esac
fi
