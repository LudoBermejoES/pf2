#!/bin/bash
# Script para reemplazar símbolos de acciones por includes de Jekyll
#
# Patrones a reemplazar:
#   ◆◆◆ → {% include accion.html tipo="3" %}
#   ◆◆  → {% include accion.html tipo="2" %}
#   ◆   → {% include accion.html tipo="1" %}
#   ◇   → {% include accion.html tipo="libre" %}
#
# IMPORTANTE: El orden importa - primero los más largos

cd /Users/ludo/code/pf2/docs

# Contador de archivos modificados
count=0

# Buscar todos los archivos .md con símbolos de acciones
for file in $(grep -rl "◆\|◇" --include="*.md" 2>/dev/null); do
    # Hacer los reemplazos en orden (primero los más largos)
    # Usamos sed con -i para editar in-place

    # macOS sed requiere -i '' (string vacío para backup)
    sed -i '' \
        -e 's/◆◆◆/{% include accion.html tipo="3" %}/g' \
        -e 's/◆◆/{% include accion.html tipo="2" %}/g' \
        -e 's/◆/{% include accion.html tipo="1" %}/g' \
        -e 's/◇/{% include accion.html tipo="libre" %}/g' \
        "$file"

    ((count++))

    # Mostrar progreso cada 50 archivos
    if (( count % 50 == 0 )); then
        echo "Procesados $count archivos..."
    fi
done

echo ""
echo "✅ Completado: $count archivos modificados"
