#!/usr/bin/env bash

set -euo pipefail

browser_cdp_mode=headless
browser_cdp_bin="${BROWSER_CDP_BIN:-}"
browser_cdp_bin_argument=""

while (($#)); do
  case "$1" in
    headless|visible) browser_cdp_mode="$1" ;;
    --mode) shift; [[ $# -gt 0 ]] || { printf 'Usage: %s [headless|visible] [browser-binary]\n' "$0" >&2; exit 2; }; browser_cdp_mode="$1" ;;
    --mode=*) browser_cdp_mode="${1#--mode=}" ;;
    --browser|--binary) shift; [[ $# -gt 0 ]] || { printf 'Usage: %s [headless|visible] [browser-binary]\n' "$0" >&2; exit 2; }; browser_cdp_bin_argument="$1" ;;
    --browser=*|--binary=*) browser_cdp_bin_argument="${1#*=}" ;;
    --*) printf 'Unknown option: %s\n' "$1" >&2; exit 2 ;;
    *) [[ -z "$browser_cdp_bin_argument" ]] || { printf 'Only one browser binary may be specified.\n' >&2; exit 2; }; browser_cdp_bin_argument="$1" ;;
  esac
  shift
done

[[ "$browser_cdp_mode" == headless || "$browser_cdp_mode" == visible ]] || { printf 'Usage: %s [headless|visible] [browser-binary]\n' "$0" >&2; exit 2; }
[[ -z "$browser_cdp_bin_argument" ]] || browser_cdp_bin="$browser_cdp_bin_argument"

if [[ -z "$browser_cdp_bin" ]]; then
  for candidate in vivaldi google-chrome google-chrome-stable chromium chromium-browser brave-browser microsoft-edge; do
    if browser_cdp_candidate_path="$(command -v "$candidate" 2>/dev/null)"; then browser_cdp_bin="$browser_cdp_candidate_path"; break; fi
  done
fi

if [[ -z "$browser_cdp_bin" ]]; then
  printf 'No supported browser binary found; set BROWSER_CDP_BIN or pass a browser binary.\n' >&2
  exit 1
fi
if ! command -v "$browser_cdp_bin" >/dev/null 2>&1 && [[ ! -x "$browser_cdp_bin" ]]; then
  printf 'Browser binary not found or not executable: %s\n' "$browser_cdp_bin" >&2
  exit 1
fi

browser_cdp_tmpdir="${TMPDIR:-/tmp}"
browser_cdp_profile="$(mktemp -d "$browser_cdp_tmpdir/browser-cdp.XXXXXX")"
browser_cdp_pid=""

cleanup_browser_cdp() {
  if [[ -n "$browser_cdp_pid" ]]; then kill "$browser_cdp_pid" 2>/dev/null || true; wait "$browser_cdp_pid" 2>/dev/null || true; fi
  if [[ -d "$browser_cdp_profile" && "$browser_cdp_profile" == "$browser_cdp_tmpdir/browser-cdp.??????" ]]; then find "$browser_cdp_profile" -depth -delete; fi
}
trap cleanup_browser_cdp EXIT
trap 'exit 130' INT
trap 'exit 143' TERM

browser_cdp_mode_args=()
[[ "$browser_cdp_mode" == headless ]] && browser_cdp_mode_args=(--headless=new)

"$browser_cdp_bin" "${browser_cdp_mode_args[@]}" --user-data-dir="$browser_cdp_profile" --remote-debugging-address=127.0.0.1 --remote-debugging-port=0 --no-first-run --no-default-browser-check about:blank >"$browser_cdp_profile/browser.log" 2>&1 &
browser_cdp_pid=$!

for _ in {1..100}; do
  [[ -s "$browser_cdp_profile/DevToolsActivePort" ]] && break
  if ! kill -0 "$browser_cdp_pid" 2>/dev/null; then printf 'Browser exited before CDP became ready. Log:\n' >&2; sed -n '1,160p' "$browser_cdp_profile/browser.log" >&2; exit 1; fi
  sleep 0.1
done
if [[ ! -s "$browser_cdp_profile/DevToolsActivePort" ]]; then printf 'Timed out waiting for DevToolsActivePort. Log:\n' >&2; sed -n '1,160p' "$browser_cdp_profile/browser.log" >&2; exit 1; fi

browser_cdp_port="$(sed -n '1p' "$browser_cdp_profile/DevToolsActivePort")"
printf 'BROWSER_CDP_BROWSER_URL=http://127.0.0.1:%s\n' "$browser_cdp_port"
printf 'BROWSER_CDP_PROFILE=%s\n' "$browser_cdp_profile"
printf 'BROWSER_CDP_PID=%s\n' "$browser_cdp_pid"
printf 'BROWSER_CDP_BIN=%s\n' "$browser_cdp_bin"
printf 'Keep this command session running; send "stop" to stop the browser and remove the isolated profile.\n'

if [[ -t 0 ]]; then while kill -0 "$browser_cdp_pid" 2>/dev/null; do if IFS= read -r -t 1 browser_cdp_command && [[ "$browser_cdp_command" == stop ]]; then exit 0; fi; done; fi
wait "$browser_cdp_pid"
