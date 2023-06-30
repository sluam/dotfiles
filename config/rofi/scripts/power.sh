apagar="⏻  Off"
suspender="󰤄 Suspend"
bloquear="  Lock"
logout="  Logout"
restart="󰜉 Restart"

dir="~/.config/rofi/scripts"
OPTIONS="${apagar}\n${restart}\n${suspender}\n${bloquear}\n${logout}"
ans=$(echo  "${OPTIONS}" | rofi -theme "~/.config/rofi/themes/powermenu.rasi" -dmenu)
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
        "$restart")
            systemctl reboot
            ;;
    esac
fi
