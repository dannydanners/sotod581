#!/usr/bin/env bash
set -euo pipefail

exec > >(tee -a /var/log/cloudlab-bootstrap.log) 2>&1
set -x

GH_PAT="$(geni-get 'param gh_pat' || true)"
GH_OWNER="$(geni-get 'param gh_owner' || true)"
GH_REPO="$(geni-get 'param gh_repo' || true)"

export GH_PAT GH_OWNER GH_REPO

bash /local/repository/cloudlab/install_docker.sh

if [[ -n "$GH_PAT" && -n "$GH_OWNER" && -n "$GH_REPO" ]]; then
  bash /local/repository/cloudlab/install_github_runner.sh
else
  echo "Skipping GitHub runner setup because GitHub parameters were not fully provided."
fi


cd /local/repository/cloudlab/docker
docker compose pull
docker compose up -d


unset GH_PAT