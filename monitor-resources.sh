#!/bin/bash

# Script de monitoreo de recursos para contenedores Docker
# Monitorea CPU, RAM y uso de disco de los contenedores

echo "============================================"
echo "  Monitoreo de Recursos - EVA2 Backend"
echo "============================================"
echo ""

# Colores para mejor visualización
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Verificar si los contenedores están corriendo
if ! docker ps | grep -q "reservas_api\|reservas_db"; then
    echo -e "${RED}❌ Los contenedores no están corriendo${NC}"
    echo "Ejecuta: docker-compose up -d"
    exit 1
fi

echo -e "${GREEN}✓ Contenedores activos${NC}"
echo ""

# Función para mostrar uso de recursos
mostrar_recursos() {
    echo -e "${BLUE}📊 Estado de Contenedores:${NC}"
    docker ps --format "table {{.Names}}\t{{.Status}}" | grep -E "reservas_api|reservas_db|NAMES"
    echo ""
    
    echo -e "${BLUE}💻 Uso de CPU y Memoria:${NC}"
    docker stats --no-stream --format "table {{.Name}}\t{{.CPUPerc}}\t{{.MemUsage}}\t{{.MemPerc}}" reservas_api reservas_db
    echo ""
    
    echo -e "${BLUE}💾 Uso de Disco (Volúmenes):${NC}"
    docker system df -v | grep -A 10 "Local Volumes" | head -15
    echo ""
    
    echo -e "${BLUE}🔌 Conexiones a Base de Datos:${NC}"
    docker exec reservas_db psql -U postgres -d reservas_db -c "SELECT count(*) as conexiones_activas FROM pg_stat_activity WHERE datname='reservas_db';" 2>/dev/null || echo "No se pudo conectar a la base de datos"
    echo ""
    
    echo -e "${BLUE}📝 Tamaño de Logs:${NC}"
    docker exec reservas_api du -sh /app/logs 2>/dev/null || echo "No se encontraron logs"
    echo ""
}

# Función para monitoreo continuo
monitoreo_continuo() {
    echo -e "${YELLOW}Monitoreo continuo activado. Presiona Ctrl+C para salir.${NC}"
    echo ""
    
    while true; do
        clear
        echo "============================================"
        echo "  Monitoreo en Tiempo Real - $(date '+%H:%M:%S')"
        echo "============================================"
        echo ""
        mostrar_recursos
        sleep 5
    done
}

# Función para mostrar alertas
verificar_alertas() {
    echo -e "${YELLOW}⚠️  Verificando alertas...${NC}"
    echo ""
    
    # Obtener uso de memoria del contenedor API
    MEM_API=$(docker stats --no-stream --format "{{.MemPerc}}" reservas_api | sed 's/%//')
    MEM_DB=$(docker stats --no-stream --format "{{.MemPerc}}" reservas_db | sed 's/%//')
    
    # Alertar si el uso de memoria es alto
    if (( $(echo "$MEM_API > 80" | bc -l) )); then
        echo -e "${RED}⚠️  ALERTA: API usando más del 80% de memoria ($MEM_API%)${NC}"
    else
        echo -e "${GREEN}✓ API: Memoria OK ($MEM_API%)${NC}"
    fi
    
    if (( $(echo "$MEM_DB > 80" | bc -l) )); then
        echo -e "${RED}⚠️  ALERTA: Base de datos usando más del 80% de memoria ($MEM_DB%)${NC}"
    else
        echo -e "${GREEN}✓ Base de datos: Memoria OK ($MEM_DB%)${NC}"
    fi
    
    echo ""
}

# Menú principal
case "$1" in
    watch)
        monitoreo_continuo
        ;;
    alerts)
        verificar_alertas
        ;;
    *)
        mostrar_recursos
        echo "Uso:"
        echo "  ./monitor-resources.sh          - Mostrar estado actual"
        echo "  ./monitor-resources.sh watch    - Monitoreo continuo (actualiza cada 5s)"
        echo "  ./monitor-resources.sh alerts   - Verificar alertas de recursos"
        ;;
esac
