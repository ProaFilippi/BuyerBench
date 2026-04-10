#!/usr/bin/env bash
# =============================================================================
# start.sh — BuyerBench Full Stack Launcher
# =============================================================================
#
# Brings up BuyerBench services in the correct order:
#
#   1. Pre-flight: verifies Python venv, Node/npm, and key env vars.
#   2. Next.js Web Dashboard — npm run dev on port WEB_PORT (default 3001)
#   3. Browser auto-open    — xdg-open http://localhost:WEB_PORT
#   4. BuyerBench TUI       — python3 -m buyerbench session | dashboard
#
# USAGE
#   ./start.sh [options]
#
# OPTIONS
#   --no-web         Skip starting the Next.js dashboard
#   --no-tui         Start web only; skip launching TUI
#   --web-port N     Override Next.js port (default: 3001)
#   --tui home       Launch home screen TUI (default — researcher navigates from here)
#   --tui session    Launch `session` wizard directly
#   --tui dashboard  Launch `dashboard` TUI directly
#   --skip-check     Skip pre-flight checks
#   -h, --help       Show this help
#
# ENVIRONMENT VARIABLES
#   WEB_PORT     Next.js port (default: 3001)
#   SKIP_WEB     Set to 1 to skip web dashboard startup
#   SKIP_TUI     Set to 1 to skip TUI launch
#   SKIP_CHECK   Set to 1 to skip pre-flight checks
#   TUI_CMD      Override TUI command: home (default) | session | dashboard
# =============================================================================

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ROOT_DIR="$SCRIPT_DIR"

# ─── Colors ───────────────────────────────────────────────────────────────────
RED='\033[0;31m'; GREEN='\033[0;32m'; YELLOW='\033[1;33m'
BLUE='\033[0;34m'; CYAN='\033[0;36m'; BOLD='\033[1m'; RESET='\033[0m'

step()  { echo -e "${BOLD}${BLUE}[▶]${RESET} $*"; }
ok()    { echo -e "${GREEN}[✓]${RESET} $*"; }
warn()  { echo -e "${YELLOW}[!]${RESET} $*"; }
fail()  { echo -e "${RED}[✗]${RESET} $*" >&2; exit 1; }

# ─── Defaults ─────────────────────────────────────────────────────────────────
SKIP_WEB="${SKIP_WEB:-0}"
SKIP_TUI="${SKIP_TUI:-0}"
SKIP_CHECK="${SKIP_CHECK:-0}"
WEB_PORT="${WEB_PORT:-3001}"
WEB_PID=""
WEB_LOG="${WEB_LOG:-/tmp/buyerbench-web.log}"

# Default TUI: always launch the home screen — researcher navigates to Reports/Sessions from there
if [[ -z "${TUI_CMD:-}" ]]; then
  TUI_CMD="home"
fi

# Python binary — prefer venv
if [[ -x "$ROOT_DIR/.venv/bin/python3" ]]; then
  PYTHON_BIN="$ROOT_DIR/.venv/bin/python3"
else
  PYTHON_BIN="python3"
fi

# ─── Arg parsing ──────────────────────────────────────────────────────────────
while [[ $# -gt 0 ]]; do
  case "$1" in
    --no-web)      SKIP_WEB=1; shift ;;
    --no-tui)      SKIP_TUI=1; shift ;;
    --skip-check)  SKIP_CHECK=1; shift ;;
    --web-port)    WEB_PORT="$2"; shift 2 ;;
    --tui)         TUI_CMD="$2"; shift 2 ;;
    -h|--help)
      sed -n '/^# USAGE/,/^# ====/p' "$0" | grep -v "^# ====" | sed 's/^# \?//'
      exit 0 ;;
    *) warn "Unknown option: $1"; shift ;;
  esac
done

# ─── Banner ───────────────────────────────────────────────────────────────────
echo -e "${BOLD}${CYAN}"
echo "  ╔══════════════════════════════════════════════════╗"
echo "  ║        BuyerBench — AI Buyer Agent Benchmark     ║"
echo "  ╚══════════════════════════════════════════════════╝"
echo -e "${RESET}"

# ─── Pre-flight ───────────────────────────────────────────────────────────────
if [[ "$SKIP_CHECK" == "0" ]]; then
  step "Pre-flight checks"

  # Python binary
  if [[ -x "$ROOT_DIR/.venv/bin/python3" ]]; then
    ok "Python ($("$PYTHON_BIN" --version 2>&1 | awk '{print $2}')) — .venv"
  elif command -v python3 &>/dev/null; then
    ok "Python ($(python3 --version 2>&1 | awk '{print $2}')) — system"
  else
    fail "python3 not found. Install Python 3.10+ or create a venv."
  fi

  # BuyerBench package installed?
  if ! "$PYTHON_BIN" -m buyerbench --help &>/dev/null; then
    fail "buyerbench package not importable. Run: pip install -e ."
  fi
  ok "buyerbench package importable"

  # Node / npm
  if command -v node &>/dev/null; then
    ok "node $(node --version)"
  else
    warn "node not found — web dashboard will be unavailable"
    SKIP_WEB=1
  fi

  if command -v npm &>/dev/null; then
    ok "npm $(npm --version)"
  else
    warn "npm not found — web dashboard will be unavailable"
    SKIP_WEB=1
  fi

  # web/node_modules
  if [[ ! -d "$ROOT_DIR/web/node_modules" ]]; then
    warn "web/node_modules missing — run: cd web && npm install"
  else
    ok "web/node_modules present"
  fi

  # Optional API key
  if [[ -z "${OPENROUTER_API_KEY:-}" ]]; then
    warn "OPENROUTER_API_KEY not set — OpenRouter agents will be unavailable"
  else
    ok "OPENROUTER_API_KEY set"
  fi
fi

# ─── Next.js Web Dashboard (:WEB_PORT) ────────────────────────────────────────
if [[ "$SKIP_WEB" == "0" ]]; then
  step "Next.js Web Dashboard (:${WEB_PORT})"

  # Kill any existing process on this port
  EXISTING_PID=$(lsof -ti tcp:"${WEB_PORT}" 2>/dev/null || true)
  if [[ -n "$EXISTING_PID" ]]; then
    warn "Port ${WEB_PORT} in use (PID $EXISTING_PID) — stopping it..."
    kill "$EXISTING_PID" 2>/dev/null || true
    sleep 1
  fi

  : > "$WEB_LOG"
  (
    # shellcheck source=/dev/null
    source "$ROOT_DIR/.env" 2>/dev/null || true
    cd "$ROOT_DIR/web"
    npm run dev -- -p "$WEB_PORT" >> "$WEB_LOG" 2>&1
  ) &
  WEB_PID=$!

  step "Waiting for web dashboard..."
  for i in $(seq 1 30); do
    if ! kill -0 "$WEB_PID" 2>/dev/null; then
      echo "Web process exited. Logs:"
      tail -n 30 "$WEB_LOG" || true
      fail "Next.js crashed on startup"
    fi
    if curl -sf "http://localhost:${WEB_PORT}" &>/dev/null; then
      ok "Web dashboard ready → http://localhost:${WEB_PORT}"
      echo -e "  ${CYAN}Log:${RESET} $WEB_LOG  (PID $WEB_PID)"
      break
    fi
    [[ $i -eq 30 ]] && {
      tail -n 30 "$WEB_LOG" || true
      fail "Web dashboard health check timed out (30s)"
    }
    sleep 1
  done

  # Auto-open browser
  step "Opening browser..."
  xdg-open "http://localhost:${WEB_PORT}" &>/dev/null || \
    warn "Could not auto-open browser — visit http://localhost:${WEB_PORT}"
fi

# ─── Cleanup trap ─────────────────────────────────────────────────────────────
cleanup() {
  if [[ -n "$WEB_PID" ]] && kill -0 "$WEB_PID" 2>/dev/null; then
    echo ""; warn "Stopping web dashboard (PID $WEB_PID)..."
    kill "$WEB_PID" 2>/dev/null || true
    wait "$WEB_PID" 2>/dev/null || true
    ok "Web dashboard stopped"
  fi
}
trap cleanup EXIT INT TERM

# ─── Summary ──────────────────────────────────────────────────────────────────
echo ""
echo -e "${BOLD}${GREEN}  BuyerBench services ready:${RESET}"
[[ "$SKIP_WEB" == "0" ]] && \
  echo -e "  ${GREEN}✓${RESET} Web Dashboard   http://localhost:${WEB_PORT}"
if [[ "$TUI_CMD" == "home" ]]; then
  echo -e "  ${CYAN}ℹ${RESET}  TUI            python3 -m buyerbench  (home screen)"
else
  echo -e "  ${CYAN}ℹ${RESET}  TUI            python3 -m buyerbench ${TUI_CMD}"
fi
echo ""

# ─── Foreground TUI ───────────────────────────────────────────────────────────
if [[ "$SKIP_TUI" == "0" ]]; then
  step "Launching BuyerBench TUI: ${TUI_CMD}"
  echo ""
  cd "$ROOT_DIR"
  if [[ "$TUI_CMD" == "home" ]]; then
    exec "$PYTHON_BIN" -m buyerbench
  elif [[ "$TUI_CMD" == "dashboard" ]]; then
    exec "$PYTHON_BIN" -m buyerbench dashboard --results-dir "$ROOT_DIR/results"
  else
    exec "$PYTHON_BIN" -m buyerbench "$TUI_CMD"
  fi
else
  ok "Services up. Run: python3 -m buyerbench"
  [[ -n "$WEB_PID" ]] && wait "$WEB_PID" 2>/dev/null || true
fi
