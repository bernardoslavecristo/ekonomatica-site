#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")"
echo "Ekonomática | Atualização da VPS Hostinger"
if [[ ! -f .env ]]; then cp .env.example .env; fi
if ! grep -q '^EKONOMATICA_ADMIN_TOKEN=' .env; then
  printf '\nEKONOMATICA_ADMIN_TOKEN=%s\n' "$(openssl rand -hex 24)" >> .env
  chmod 600 .env
  echo "Token administrativo gerado na .env privada da VPS."
fi
docker compose config --quiet
echo "[1/3] Construindo a versão atualizada..."
docker compose build app
echo "[2/3] Validando a importação da API antes de publicar..."
docker compose run --rm --no-deps app python -c 'from backend.main import app; print("VALIDACAO API: importacao OK")'
echo "[3/3] Publicando os serviços..."
docker compose up -d
docker compose ps
echo "SITE: https://ekonomatica.com.br"
echo "CAIXA DE CONTATOS: https://ekonomatica.com.br/caixa.html"
if grep -Eq "^OPENAI_API_KEY=sk-[A-Za-z0-9_-]+" .env; then
  echo "OpenAI: chave configurada (nao confirma saldo ou sucesso da API)."
else
  echo "OpenAI: chave ainda nao configurada. Chat vai orientar o visitante a usar o formulario."
fi
echo "Telegram: notificacoes dependem de configuracao do bot separada."
