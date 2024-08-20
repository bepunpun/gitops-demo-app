#!/bin/sh
# Runs the steps of .github/workflows/ci.yml against local stand-ins:
#   registry localhost:5000 instead of GHCR, a bare git repo instead of the config repo on GitHub.
# Start those first with `make up` in the config repo.
set -eu
cd "$(dirname "$0")/.."

REGISTRY=${REGISTRY:-localhost:5000}
IMAGE_NAME=${IMAGE_NAME:-gitops-demo-app}
CONFIG_REMOTE=${CONFIG_REMOTE:-$PWD/../gitops-demo-config/local/.state/config.git}
[ -d "$CONFIG_REMOTE" ] || { echo "config remote not found: $CONFIG_REMOTE (run 'make up' in the config repo)" >&2; exit 1; }

tag=$(git rev-parse --short HEAD)
git diff --quiet HEAD || echo "warning: uncommitted changes are not part of tag $tag" >&2

echo "== test"
make test

echo "== image $REGISTRY/$IMAGE_NAME:$tag"
docker build -q --build-arg GIT_SHA="$tag" -t "$REGISTRY/$IMAGE_NAME:$tag" .
docker push -q "$REGISTRY/$IMAGE_NAME:$tag"

echo "== record the tag in the config repo"
work=$(mktemp -d)
trap 'rm -rf "$work"' EXIT
git clone -q "$CONFIG_REMOTE" "$work"
"$work/scripts/set-image-tag.sh" staging "$tag"
git -C "$work" -c user.name=gitops-ci-bot -c user.email=gitops-ci-bot@users.noreply.github.com \
    commit -q -am "ci: staging -> $tag"
git -C "$work" push -q origin HEAD:main
