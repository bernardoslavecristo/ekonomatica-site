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
docker compose run --rm --no-deps app python -c 'from pathlib import Path; from backend.main import app; pub=Path("/app/public"); required=["index.html","portfolio.html","experiencia-3d.css","experiencia-3d.js","ai-chat.js","contact-widget.js","galeria-3d.html","galeria-3d.js","chef-lu-360.html","chef-lu-360.js","kaggriculture-360.html","apresentacoes.html","impact-hub-desafio.svg","como-trabalhamos.html"]; missing=[x for x in required if not (pub/x).is_file()]; assert not missing, "Faltam arquivos: "+", ".join(missing); assert "id=\"ek3d\"" in (pub/"index.html").read_text(), "Cena 3D ausente na homepage"; print("VALIDACAO API, GALERIA 3D E SITE: OK")'
echo "[3/3] Publicando os serviços..."
docker compose up -d
docker compose ps
echo "[4/4] Verificando acesso publico a paginas essenciais..."
ok_pages=0
for page in / /portfolio.html /galeria-3d.html /apresentacoes.html /kaggriculture-360.html; do
  http_code="$(curl -sS -L --max-time 12 -o /dev/null -w '%{http_code}' "https://ekonomatica.com.br${page}" || true)"
  if [[ "$http_code" == "200" ]]; then
    echo "OK HTTP 200: ${page}"
    ok_pages=$((ok_pages + 1))
  else
    echo "ATENCAO HTTP ${http_code:-indisponivel}: ${page}"
  fi
done
echo "PAGINAS PUBLICADAS: ${ok_pages}/5 verificadas com HTTP 200."
echo "Esta verificacao nao confirma reproducao do video nem entrega de mensagens Telegram."
echo "SITE: https://ekonomatica.com.br"
echo "CAIXA DE CONTATOS: https://ekonomatica.com.br/caixa.html"
if grep -Eq "^OPENAI_API_KEY=sk-[A-Za-z0-9_-]+" .env; then
  echo "OpenAI: chave configurada (nao confirma saldo ou sucesso da API)."
else
  echo "OpenAI: chave ainda nao configurada. Chat vai orientar o visitante a usar o formulario."
fi
echo "Telegram: notificacoes dependem de configuracao do bot separada."
