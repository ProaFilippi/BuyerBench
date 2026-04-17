# Phase 01: Create start.sh Full Stack Launcher

This phase creates `start.sh` in the BuyerBench root — a single entry-point that starts the Next.js web dashboard in the background, opens it in the browser, then hands the terminal to the BuyerBench TUI. It mirrors the exact structure of `athen-ai/start.sh`: colored banner, pre-flight checks, background service with health-check wait, cleanup trap, summary table, and foreground `exec` at the end.

## Tasks

- [ ] Read `/home/superiora/Documents/CODE/athen-ai/start.sh` in full to internalize the exact structure, color helper names, trap pattern, health-check loop, and summary table layout before writing anything. Do not skip this step.

- [ ] Write `/home/superiora/Documents/CODE/BuyerBench/start.sh` with the following content verbatim (section by section, assembled into one file):

  **Header comment block:**
  ```
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
  #   --tui session    Launch session TUI (default when results/ is empty)
  #   --tui dashboard  Launch dashboard TUI (default when results/ has content)
  #   --skip-check     Skip pre-flight checks
  #   -h, --help       Show this help
  #
  # ENVIRONMENT VARIABLES
  #   WEB_PORT     Next.js port (default: 3001)
  #   SKIP_WEB     Set to 1 to skip web dashboard startup
  #   SKIP_TUI     Set to 1 to skip TUI launch
  #   SKIP_CHECK   Set to 1 to skip pre-flight checks
  #   TUI_CMD      Override TUI command: session | dashboard
  # =============================================================================
  ```

  **Boilerplate + colors + helpers** (same names as athen-ai):
  ```bash
  set -euo pipefail
  SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
  ROOT_DIR="$SCRIPT_DIR"

  RED='\033[0;31m'; GREEN='\033[0;32m'; YELLOW='\033[1;33m'
  BLUE='\033[0;34m'; CYAN='\033[0;36m'; BOLD='\033[1m'; RESET='\033[0m'

  step()  { echo -e "${BOLD}${BLUE}[▶]${RESET} $*"; }
  ok()    { echo -e "${GREEN}[✓]${RESET} $*"; }
  warn()  { echo -e "${YELLOW}[!]${RESET} $*"; }
  fail()  { echo -e "${RED}[✗]${RESET} $*" >&2; exit 1; }
  ```

  **Defaults, smart TUI selection, Python binary, arg parsing:**
  ```bash
  SKIP_WEB="${SKIP_WEB:-0}"
  SKIP_TUI="${SKIP_TUI:-0}"
  SKIP_CHECK="${SKIP_CHECK:-0}"
  WEB_PORT="${WEB_PORT:-3001}"
  WEB_PID=""
  WEB_LOG="${WEB_LOG:-/tmp/buyerbench-web.log}"

  # Smart TUI default: dashboard if results/ has content, otherwise session
  if [[ -z "${TUI_CMD:-}" ]]; then
    if [[ -d "$ROOT_DIR/results" ]] && compgen -G "$ROOT_DIR/results/*" > /dev/null 2>&1; then
      TUI_CMD="dashboard"
    else
      TUI_CMD="session"
    fi
  fi

  # Python binary — prefer venv
  if [[ -x "$ROOT_DIR/.venv/bin/python3" ]]; then
    PYTHON_BIN="$ROOT_DIR/.venv/bin/python3"
  else
    PYTHON_BIN="python3"
  fi

  while [[ $# -gt 0 ]]; do
    case "$1" in
      --no-web)     SKIP_WEB=1; shift ;;
      --no-tui)     SKIP_TUI=1; shift ;;
      --skip-check) SKIP_CHECK=1; shift ;;
      --web-port)   WEB_PORT="$2"; shift 2 ;;
      --tui)        TUI_CMD="$2"; shift 2 ;;
      -h|--help)
        sed -n '/^# USAGE/,/^# ====/p' "$0" | grep -v "^# ====" | sed 's/^# \?//'
        exit 0 ;;
      *) warn "Unknown option: $1"; shift ;;
    esac
  done
  ```

  **Banner** (bold cyan):
  ```bash
  echo -e "${BOLD}${CYAN}"
  echo "  ╔══════════════════════════════════════════════════╗"
  echo "  ║      BuyerBench — AI Buyer Agent Benchmark       ║"
  echo "  ╚══════════════════════════════════════════════════╝"
  echo -e "${RESET}"
  ```

  **Pre-flight checks** (guarded by `$SKIP_CHECK`):
  ```bash
  if [[ "$SKIP_CHECK" == "0" ]]; then
    step "Pre-flight checks"

    # Python
    if [[ ! -x "$PYTHON_BIN" ]] && ! command -v "$PYTHON_BIN" &>/dev/null; then
      fail "Python not found at $PYTHON_BIN — activate venv or install Python 3"
    fi
    ok "Python: $("$PYTHON_BIN" --version 2>&1)"

    # buyerbench package
    if ! "$PYTHON_BIN" -m buyerbench --help &>/dev/null; then
      fail "buyerbench package not installed — run: pip install -e \".[dev]\""
    fi
    ok "buyerbench package installed"

    # Node + npm
    if ! command -v node &>/dev/null; then
      fail "node not found — install Node.js to run the web dashboard"
    fi
    if ! command -v npm &>/dev/null; then
      fail "npm not found — install Node.js to run the web dashboard"
    fi
    ok "Node $(node --version) / npm $(npm --version)"

    # node_modules
    if [[ ! -d "$ROOT_DIR/web/node_modules" ]]; then
      warn "web/node_modules missing — run: cd web && npm install"
    else
      ok "web/node_modules present"
    fi

    # Optional API key warning
    if [[ -z "${OPENROUTER_API_KEY:-}" ]]; then
      warn "OPENROUTER_API_KEY not set — OpenRouter agents will be unavailable"
    fi
  fi
  ```

  **Cleanup trap** (must be defined before the web process starts):
  ```bash
  cleanup() {
    if [[ -n "$WEB_PID" ]] && kill -0 "$WEB_PID" 2>/dev/null; then
      echo ""; warn "Stopping web dashboard (PID $WEB_PID)..."
      kill "$WEB_PID" 2>/dev/null || true
      wait "$WEB_PID" 2>/dev/null || true
      ok "Web dashboard stopped"
    fi
  }
  trap cleanup EXIT INT TERM
  ```

  **Next.js web dashboard** (background, guarded by `$SKIP_WEB`):
  ```bash
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
    xdg-open "http://localhost:${WEB_PORT}" &>/dev/null &
    ok "Browser open requested → http://localhost:${WEB_PORT}"
  fi
  ```

  **Summary table:**
  ```bash
  echo ""
  echo -e "${BOLD}${GREEN}  BuyerBench services ready:${RESET}"
  [[ "$SKIP_WEB" == "0" ]] && \
    echo -e "  ${GREEN}✓${RESET} Web Dashboard   http://localhost:${WEB_PORT}"
  echo -e "  ${CYAN}ℹ${RESET}  TUI            $PYTHON_BIN -m buyerbench ${TUI_CMD}"
  echo ""
  ```

  **Foreground TUI** (guarded by `$SKIP_TUI`, launched with `exec`):
  ```bash
  if [[ "$SKIP_TUI" == "0" ]]; then
    step "Launching BuyerBench TUI: ${TUI_CMD}"
    echo ""
    cd "$ROOT_DIR"
    exec "$PYTHON_BIN" -m buyerbench "$TUI_CMD"
  else
    ok "Services up. Run: $PYTHON_BIN -m buyerbench session"
    [[ -n "$WEB_PID" ]] && wait "$WEB_PID" 2>/dev/null || true
  fi
  ```

- [ ] Make the script executable: `chmod +x /home/superiora/Documents/CODE/BuyerBench/start.sh`

- [ ] Smoke test the script — run all three commands and confirm each exits cleanly:
  - `bash -n /home/superiora/Documents/CODE/BuyerBench/start.sh` — must print nothing and exit 0 (syntax check)
  - `cd /home/superiora/Documents/CODE/BuyerBench && ./start.sh --help` — must print usage block with OPTIONS and ENVIRONMENT VARIABLES sections and exit 0
  - `cd /home/superiora/Documents/CODE/BuyerBench && ./start.sh --no-web --no-tui --skip-check` — must print banner + summary table and exit 0 without hanging

  If any test fails, fix `start.sh` before proceeding.
