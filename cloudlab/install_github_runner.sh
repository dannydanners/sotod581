#!/usr/bin/env bash
set -euo pipefail

RUNNER_USER="github-runner"
RUNNER_BASE_DIR="/home/${RUNNER_USER}"
RUNNER_DIR="${RUNNER_BASE_DIR}/actions-runner"

: "${GH_PAT:?GH_PAT is required}"
: "${GH_OWNER:?GH_OWNER is required}"
: "${GH_REPO:?GH_REPO is required}"

echo "Installing GitHub Actions self-hosted runner for ${GH_OWNER}/${GH_REPO}"

apt-get update
apt-get install -y curl jq tar git ca-certificates

if ! id "$RUNNER_USER" >/dev/null 2>&1; then
  useradd -m -s /bin/bash "$RUNNER_USER"
fi

if getent group docker >/dev/null 2>&1; then
  usermod -aG docker "$RUNNER_USER"
fi

if [[ -d /local/repository ]]; then
  chown -R "${RUNNER_USER}:${RUNNER_USER}" /local/repository
fi

mkdir -p "$RUNNER_DIR"
chown -R "${RUNNER_USER}:${RUNNER_USER}" "$RUNNER_BASE_DIR"

RUNNER_TOKEN="$(curl -sL \
  -X POST \
  -H "Accept: application/vnd.github+json" \
  -H "Authorization: Bearer ${GH_PAT}" \
  -H "X-GitHub-Api-Version: 2022-11-28" \
  "https://api.github.com/repos/${GH_OWNER}/${GH_REPO}/actions/runners/registration-token" \
  | jq -r .token)"

unset GH_PAT

if [[ -z "$RUNNER_TOKEN" || "$RUNNER_TOKEN" == "null" ]]; then
  echo "Failed to get GitHub runner registration token."
  exit 1
fi

RUNNER_VERSION="$(curl -sL https://api.github.com/repos/actions/runner/releases/latest | jq -r .tag_name | sed 's/^v//')"

if [[ -z "$RUNNER_VERSION" || "$RUNNER_VERSION" == "null" ]]; then
  echo "Failed to determine latest GitHub Actions runner version."
  exit 1
fi

echo "Using GitHub Actions runner version ${RUNNER_VERSION}"

sudo -u "$RUNNER_USER" bash -c "
set -euo pipefail

cd '$RUNNER_DIR'

if [[ ! -f config.sh ]]; then
  curl -o actions-runner-linux-x64.tar.gz -L \
    'https://github.com/actions/runner/releases/download/v${RUNNER_VERSION}/actions-runner-linux-x64-${RUNNER_VERSION}.tar.gz'

  tar xzf actions-runner-linux-x64.tar.gz
fi

if [[ ! -f .runner ]]; then
  ./config.sh \
    --url 'https://github.com/${GH_OWNER}/${GH_REPO}' \
    --token '${RUNNER_TOKEN}' \
    --name 'cloudlab-'\"\$(hostname)\" \
    --labels 'cloudlab' \
    --work '_work' \
    --unattended
else
  echo 'Runner already configured; skipping config.sh.'
fi
"

cd "$RUNNER_DIR"

./svc.sh install "$RUNNER_USER" || true
./svc.sh start
./svc.sh status