#!/usr/bin/env bash
set -euo pipefail
#
# Sync .agent/ from the central blueprint template repo.
# Pulls structural updates while preserving local project-specific customizations.
#
# Usage:
#   bash .agent/automation/sync-from-template.sh
#   bash .agent/automation/sync-from-template.sh --dry-run
#

TEMPLATE_REPO="git@github.com:iamwilco/agent-blueprint.git"
TEMPLATE_BRANCH="main"
AGENT_DIR=".agent"
TEMP_DIR=$(mktemp -d)
DRY_RUN=false

for arg in "$@"; do
  case $arg in
    --dry-run) DRY_RUN=true ;;
  esac
done

cleanup() { rm -rf "${TEMP_DIR}"; }
trap cleanup EXIT

echo "=== Agent Blueprint Sync ==="
echo "Template: ${TEMPLATE_REPO} (${TEMPLATE_BRANCH})"
echo "Target:   ${AGENT_DIR}/"
echo ""

# Step 1: Clone template into temp dir (shallow)
echo "[1/4] Cloning template..."
git clone --depth 1 --branch "${TEMPLATE_BRANCH}" "${TEMPLATE_REPO}" "${TEMP_DIR}/blueprint" 2>/dev/null

if [ ! -d "${TEMP_DIR}/blueprint/.agent" ]; then
  echo "ERROR: Template repo does not contain .agent/ directory."
  exit 1
fi

# Step 2: Identify new/updated files
echo "[2/4] Comparing files..."
NEW_FILES=()
UPDATED_FILES=()
PRESERVE_FILES=(
  "README.md"
  "initialize.md"
  "update.md"
  "system/architecture.md"
  "system/database-schema.md"
  "system/api-endpoints.md"
  "learning/memory.json"
  "learning/reflection-log.md"
  "agents/config.yaml"
)

while IFS= read -r -d '' file; do
  rel_path="${file#${TEMP_DIR}/blueprint/.agent/}"
  local_path="${AGENT_DIR}/${rel_path}"

  # Skip project-specific files
  skip=false
  for preserve in "${PRESERVE_FILES[@]}"; do
    if [ "${rel_path}" = "${preserve}" ]; then
      skip=true
      break
    fi
  done

  if [ "${skip}" = true ]; then
    echo "  SKIP (project-specific): ${rel_path}"
    continue
  fi

  if [ ! -f "${local_path}" ]; then
    NEW_FILES+=("${rel_path}")
    echo "  NEW:  ${rel_path}"
  elif ! diff -q "${file}" "${local_path}" > /dev/null 2>&1; then
    UPDATED_FILES+=("${rel_path}")
    echo "  UPD:  ${rel_path}"
  fi
done < <(find "${TEMP_DIR}/blueprint/.agent" -type f -print0)

# Step 3: Apply changes (or dry-run)
echo ""
echo "[3/4] Applying changes..."
if [ "${DRY_RUN}" = true ]; then
  echo "  DRY RUN — no files modified."
else
  for rel_path in "${NEW_FILES[@]+"${NEW_FILES[@]}"}"; do
    mkdir -p "$(dirname "${AGENT_DIR}/${rel_path}")"
    cp "${TEMP_DIR}/blueprint/.agent/${rel_path}" "${AGENT_DIR}/${rel_path}"
    echo "  Copied: ${rel_path}"
  done
  for rel_path in "${UPDATED_FILES[@]+"${UPDATED_FILES[@]}"}"; do
    cp "${TEMP_DIR}/blueprint/.agent/${rel_path}" "${AGENT_DIR}/${rel_path}"
    echo "  Updated: ${rel_path}"
  done
fi

# Step 4: Summary
echo ""
echo "[4/4] Summary"
echo "  New files:     ${#NEW_FILES[@]}"
echo "  Updated files: ${#UPDATED_FILES[@]}"
echo "  Preserved:     ${#PRESERVE_FILES[@]} project-specific files"
echo ""
echo "Done. Review changes with: git diff --stat"
