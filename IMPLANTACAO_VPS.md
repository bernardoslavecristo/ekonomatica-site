# Ekonomática — implantação dinâmica na VPS
## Objetivo
Hospedar a plataforma TECH da Ekonomática com HTTPS, frontend responsivo e backend real em FastAPI. O GitHub contém o código, não executa a produção. A versão inicial oferece diagnóstico por regras e estimativa ilustrativa por API; **ainda não é um agente autônomo generativo**.

## Pré-requisitos (pendentes)
- VPS Linux (KVM 2 Hostinger em avaliação), acesso SSH e Docker + Docker Compose instalados.
- Domínio `ekonomatica.com.br` adquirido e DNS gerenciado na Hostinger.
- DNS apontando para o IPv4 público da VPS **somente depois de ela estar pronta**.
- Portas TCP 80 e 443 liberadas no firewall da VPS.

## Procedimento em servidor novo
1. Instalar Docker e Compose pelos guias oficiais, configurar usuário de implantação e firewall.
2. Clonar o repositório oficial `bernardoslavecristo/ekonomatica-site`.
3. Criar `.env` a partir de `.env.example`; conferir `SITE_DOMAIN=ekonomatica.com.br`.
4. Validar código e imagem; não iniciar o serviço público até configurar corretamente o DNS, firewall e backup.
5. Para publicar: `docker compose up -d --build` e `docker compose ps`.
6. Alterar **apenas os registros A e www relevantes**, preservando MX/TXT e demais serviços; não usar 'Redefinir DNS'.
7. Confirmar HTTPS `https://ekonomatica.com.br`, `https://www.ekonomatica.com.br`, rota `/api/health` e formulário de diagnóstico real no Android.

## Segurança/privacidade
- O backend inicial é sem banco de dados e não armazena solicitações.
- O diagnóstico é por regras; nunca apresentar como IA generativa.
- Não expor portas internas do app, segredos, tokens ou dados de clientes no GitHub.
- Antes de colocar formulários públicos amplamente em uso: preparar proteção contra abuso/rate limiting, política de privacidade e controle de custos.
- Integrações n8n, CRM, agentes de IA externos e PostgreSQL serão adicionadas em entregas futuras com autenticação, consentimento, monitoramento e teste.
- Os custos de VPS não incluem chamadas pagas a modelos de IA.

## Testes
Com dependências de `backend/requirements.txt`, `httpx` e `pytest`:
`python -m pytest tests/test_api.py`

## Próxima etapa
Contratação e acesso à VPS, depois instalação e publicação com testes no Android. Nenhum DNS foi alterado neste commit.
