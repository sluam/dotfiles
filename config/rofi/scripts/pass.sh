github="  Github"
reddit="󰑍  Reddit"
stack="  Stackoverflow"
discord="󰙯  Discord"

dir="~/.config/rofi/scripts"
OPTIONS="${github}\n${reddit}\n${stack}\n${discord}"
ans=$(echo "${OPTIONS}" | rofi -p "Sluam" -dmenu)
rs=$?
if [ $rs -eq 0 ]; then
	case "$ans" in
	"$github")
		pass Github | xclip -selection clipboard
		;;
	"$reddit")
		pass Reddit | xclip -selection clipboard
                ;;
	"$stack")
		pass Stackoverflow | xclip -selection clipboard
                ;;
	"$discord")
                pass Discord | xclip -selection clipboard
                ;;
	esac
fi
