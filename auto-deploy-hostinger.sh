#!/usr/bin/env bash
# Publicação automática da Ekonomática na própria VPS Hostinger.
# Requer instalação explícita pelo administrador, uma única vez.
set -Eeuo pipefail
exec 9>/var/lock/ekonomatica-deploy.lock
flock -n 9 || exit 0
cd /opt/ekonomatica-site
test -f .env || { echo "ERRO: .env privado não encontrado"; exit 1; }
git fetch --quiet origin main
local_sha="$(git rev-parse HEAD)"
remote_sha="$(git rev-parse origin/main)"
[ "$local_sha" != "$remote_sha" ] || { echo "Ekonomática: sem mudanças"; exit 0; }
state=/var/lib/ekonomatica-deploy
mkdir -p "$state"
if [ -f "$state/failed_sha" ] && [ "$(cat "$state/failed_sha")" = "$remote_sha" ]; then
  echo "Versão $remote_sha falhou anteriormente; aguardando nova revisão."
  exit 0
fi
if ! git diff --quiet || ! git diff --cached --quiet; then
  echo "ERRO: existem modificações locais, não sobrescrever"
  exit 1
fi
echo "Preparando deploy: $local_sha -> $remote_sha"
git merge --ff-only origin/main
if bash deploy-hostinger.sh; then
  rm -f "$state/failed_sha"
  echo "$remote_sha" > "$state/deployed_sha"
  echo "Publicação concluída: $remote_sha"
else
  echo "Falha de deploy. Restaurando versão anterior."
  printf '%s' "$remote_sha" > "$state/failed_sha"
  git reset --hard "$local_sha"
  if bash deploy-hostinger.sh; then
    echo "Versão anterior restaurada."
  else
    echo "ALERTA: rollback de serviços falhou. Intervenção técnica necessária."
  fi
  exit 1
fi
