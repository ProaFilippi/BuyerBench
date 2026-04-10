# BUYERBENCH-START-01 — Create start.sh Full Stack Launcher

## Goal
Create a `start.sh` in the BuyerBench root that follows the same structure as the
`athen-ai/start.sh` pattern: colored banner, pre-flight checks, background Next.js web
dashboard (with browser auto-open), cleanup trap, summary table, and foreground TUI
launched with `exec`.

## Context
- Next.js web dashboard lives in `web/` — defaults to port **3001** (`:3000` is taken on
  this machine)
- Python entry point: use `.venv/bin/python3` if present, fallback to `python3`
- TUI commands (from `python3 -m buyerbench --help`):
  - `session`   — interactive session builder (primary TUI)
  - `dashboard` — browse results (used when results already exist)
- Follow the same flag/env-var conventions as `athen-ai/start.sh`

---

## Tasks

- [x] **Read athen-ai/start.sh** to internalize the exact pattern before writing anything.
  ```
  cat /home/superiora/Documents/CODE/athen-ai/start.sh
  ```

- [x] **Create `start.sh`** in `/home/superiora/Documents/CODE/BuyerBench/start.sh` with
  the following structure (all sections required):

  ### 1. Header block (comment)
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
  #   --tui session    Launch `session` TUI (default when no results found)
  #   --tui dashboard  Launch `dashboard` TUI (default when results/ has content)
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

  ### 2. Boilerplate
  ```bash
  set -euo pipefail
  SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
  ROOT_DIR="$SCRIPT_DIR"
  ```

  ### 3. Color helpers (same names as athen-ai)
  ```bash
  RED='\033[0;31m'; GREEN='\033[0;32m'; YELLOW='\033[1;33m'
  BLUE='\033[0;34m'; CYAN='\033[0;36m'; BOLD='\033[1m'; RESET='\033[0m'

  step()  { echo -e "${BOLD}${BLUE}[▶]${RESET} $*"; }
  ok()    { echo -e "${GREEN}[✓]${RESET} $*"; }
  warn()  { echo -e "${YELLOW}[!]${RESET} $*"; }
  fail()  { echo -e "${RED}[✗]${RESET} $*" >&2; exit 1; }
  ```

  ### 4. Defaults & arg parsing
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
  ```

  ### 5. Banner
  Print a colored ASCII banner:
  ```
  ╔══════════════════════════════════════════════════╗
  ║        BuyerBench — AI Buyer Agent Benchmark     ║
  ╚══════════════════════════════════════════════════╝
  ```
  Use `$BOLD$CYAN` for the banner.

  ### 6. Pre-flight checks (guarded by `SKIP_CHECK`)
  Check for:
  - `$PYTHON_BIN` exists and is executable (`command -v` or test -x)
  - `python3 -m buyerbench --help` exits 0 (i.e. package is installed)
  - `node` and `npm` are available (for Next.js)
  - `web/node_modules` exists (warn if not, don't fail — suggest `npm install`)
  - Optional: warn if `OPENROUTER_API_KEY` is not set (needed for OpenRouter agents)
  On failure: `fail "..."` with a clear message.

  ### 7. Next.js web dashboard (background, guarded by `SKIP_WEB`)
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
  ```

  ### 8. Cleanup trap
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

  ### 9. Summary table
  ```bash
  echo ""
  echo -e "${BOLD}${GREEN}  BuyerBench services ready:${RESET}"
  [[ "$SKIP_WEB" == "0" ]] && \
    echo -e "  ${GREEN}✓${RESET} Web Dashboard   http://localhost:${WEB_PORT}"
  echo -e "  ${CYAN}ℹ${RESET}  TUI            python3 -m buyerbench ${TUI_CMD}"
  echo ""
  ```

  ### 10. Foreground TUI (guarded by `SKIP_TUI`)
  ```bash
  if [[ "$SKIP_TUI" == "0" ]]; then
    step "Launching BuyerBench TUI: ${TUI_CMD}"
    echo ""
    cd "$ROOT_DIR"
    exec "$PYTHON_BIN" -m buyerbench "$TUI_CMD"
  else
    ok "Services up. Run: python3 -m buyerbench session"
    [[ -n "$WEB_PID" ]] && wait "$WEB_PID" 2>/dev/null || true
  fi
  ```

- [x] **Make executable:**
  ```bash
  chmod +x /home/superiora/Documents/CODE/BuyerBench/start.sh
  ```

- [x] **Smoke test (dry run):**
  ```bash
  cd /home/superiora/Documents/CODE/BuyerBench
  bash -n start.sh && echo "Syntax OK"
  ./start.sh --help
  ./start.sh --no-tui --no-web --skip-check  # should print banner + summary and exit 0
  ```

- [x] **Verify port-conflict handling:** confirm `--web-port 3001` is the default (not 3000)
  and that the help text documents it clearly.

---

## Success Criteria
- `./start.sh --help` prints usage without error
- `bash -n start.sh` passes (no syntax errors)
- `./start.sh --no-tui --no-web` exits cleanly after printing banner and summary
- `./start.sh --no-web` launches `python3 -m buyerbench session` (or `dashboard` if results exist) in the foreground
- `./start.sh` (full) starts Next.js on :3001, opens browser, then execs TUI
- Ctrl-C kills the web background process cleanly via the trap
