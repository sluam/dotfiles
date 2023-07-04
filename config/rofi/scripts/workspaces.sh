#!/bin/bash

# Ruta al archivo de configuración
config_file="$HOME/.config/rofi/data.txt"

# Leer el archivo de configuración y almacenar las líneas en un array
mapfile -t workspaces < "$config_file"

add_workspace() {
    new_workspace="$1"
    if ! grep -Fxq "$new_workspace" "$config_file"; then
        echo "$new_workspace" >> "$config_file"
    fi
}

# Utilizar Rofi para mostrar un menú de selección
selected=$(printf '%s\n' "${workspaces[@]}" | rofi -dmenu -theme "$HOME/.config/rofi/themes/workspaces.rasi")

# Verificar la opción seleccionada y realizar la acción correspondiente
for workspace in "${workspaces[@]}"; do
    if [[ "$workspace" == "$selected" ]]; then
        # Abrir la carpeta o archivo en nvim
        nvim "$workspace"
        exit 0
    else
        exit 1
    fi
done

if [[ $# -eq 1 && $1 == "add" ]]; then
    # Si se proporcionó el argumento "add", ejecutar solo la función de añadir una dirección
     current_dir="$PWD"
    add_workspace(  pwd)
fi
