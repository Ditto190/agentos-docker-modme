#!/bin/bash

############################################################################
#
#    Agno Container Entrypoint
#
############################################################################

# Colors
ORANGE='\033[38;5;208m'
DIM='\033[2m'
BOLD='\033[1m'
NC='\033[0m'

echo ""
echo -e "${ORANGE}"
cat << 'BANNER'
     █████╗  ██████╗ ███╗   ██╗ ██████╗
    ██╔══██╗██╔════╝ ████╗  ██║██╔═══██╗
    ███████║██║  ███╗██╔██╗ ██║██║   ██║
    ██╔══██║██║   ██║██║╚██╗██║██║   ██║
    ██║  ██║╚██████╔╝██║ ╚████║╚██████╔╝
    ╚═╝  ╚═╝ ╚═════╝ ╚═╝  ╚═══╝ ╚═════╝
BANNER
echo -e "${NC}"

if [[ -z "${OPENAI_API_KEY:-}" ]]; then
    echo -e "    ${BOLD}Startup diagnostics:${NC} OPENAI_API_KEY is required."
    exit 1
fi

IS_PROD_RUNTIME=true
if [[ "${RUNTIME_ENV:-prd}" == "dev" ]]; then
    IS_PROD_RUNTIME=false
fi

MISSING_JWT_CONFIG=false
if [[ -z "${JWT_VERIFICATION_KEY:-}" ]] && [[ -z "${JWT_JWKS_FILE:-}" ]]; then
    MISSING_JWT_CONFIG=true
fi

if [[ "$IS_PROD_RUNTIME" = true ]] && [[ "$MISSING_JWT_CONFIG" = true ]]; then
    echo -e "    ${BOLD}Startup diagnostics:${NC} JWT_VERIFICATION_KEY or JWT_JWKS_FILE required for auth in production."
    exit 1
fi

if [[ -n "${MCP_CONNECT_SECRET:-}" ]] && [[ ${#MCP_CONNECT_SECRET} -lt 16 ]]; then
    echo -e "    ${BOLD}Startup diagnostics:${NC} MCP_CONNECT_SECRET must be at least 16 characters."
    exit 1
fi

if [[ "$WAIT_FOR_DB" = true || "$WAIT_FOR_DB" = True ]]; then
    echo -e "    ${DIM}Waiting for database at ${DB_HOST}:${DB_PORT}...${NC}"
    dockerize -wait tcp://$DB_HOST:$DB_PORT -timeout 300s
    echo -e "    ${BOLD}Database ready.${NC}"
    echo ""
fi

case "$1" in
    chill)
        echo -e "    ${DIM}Mode: chill${NC}"
        echo -e "    ${BOLD}Container running.${NC}"
        echo ""
        while true; do sleep 18000; done
        ;;
    *)
        echo -e "    ${DIM}> $@${NC}"
        echo ""
        exec "$@"
        ;;
esac
