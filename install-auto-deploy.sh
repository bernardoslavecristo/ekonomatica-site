#!/usr/bin/env bash
# Executar UMA vez no Web Console da VPS Hostinger como root.
set -Eeuo pipefail
if [ "$(id -u)" != "0" ]; then echo "Execute como root"; exit 1; fi
cd /opt/ekonomatica-site
test -f .env || { echo "Arquivo .env privado ausente"; exit 1; }
install -d -m 0755 /etc/systemd/system
cat > /etc/systemd/system/ekonomatica-auto-deploy.service <<'EOF'
[Unit]
Description=Ekonomática | Publicar código GitHub na Hostinger
After=network-online.target docker.service
Wants=network-online.target
[Service]
Type=oneshot
WorkingDirectory=/opt/ekonomatica-site
ExecStart=/usr/bin/bash /opt/ekonomatica-site/auto-deploy-hostinger.sh
TimeoutStartSec=600
StandardOutput=journal
StandardError=journal
EOF
cat > /etc/systemd/system/ekonomatica-auto-deploy.timer <<'EOF'
[Unit]
Description=Ekonomática | Verificar e publicar mudanças a cada 10 minutos
[Timer]
OnBootSec=2min
OnUnitInactiveSec=10min
Persistent=true
Unit=ekonomatica-auto-deploy.service
[Install]
WantedBy=timers.target
EOF
systemctl daemon-reload
systemctl enable --now ekonomatica-auto-deploy.timer
systemctl start ekonomatica-auto-deploy.service
echo "AUTO-DEPLOY: INSTALADO"
systemctl --no-pager list-timers ekonomatica-auto-deploy.timer
echo "Novos commits na main serão publicados automaticamente em até 10 minutos, desde que os testes do deploy passem."
echo "Logs: journalctl -u ekonomatica-auto-deploy.service -n 40 --no-pager"
