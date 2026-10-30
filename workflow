#!/usr/bin/env bash
set -euo pipefail

WORKFLOW_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
exec python3 "$WORKFLOW_ROOT/tools/workflowctl.py" "$@" --source "$WORKFLOW_ROOT"
