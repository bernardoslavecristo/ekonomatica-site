# Ekonomática Premium — arquitetura e requisitos de produção

## Objetivo
Site bilíngue para Brasil e Paraguai, com experiência de alto nível, captação de oportunidades e demonstrações reais.

## Entregue no repositório
- Site institucional em `index.html` e apresentação para o Paraguai em `paraguai.html`.
- Portfólio com projetos e materiais existentes.
- Laboratório interativo em `ferramentas.html`: simulador de cenários, pré-diagnóstico, consultor guiado por regras e links de demonstração.
- Este laboratório **não executa IA generativa**; dados de formulários são entregues ao aplicativo de e-mail somente por ação do visitante.

## Arquitetura recomendada para operação comercial
- Frontend estático leve, com cache/CDN e acessibilidade.
- Backend de API com autenticação e proteção contra abuso (por exemplo FastAPI em infraestrutura com suporte a Python, ou Express/Next.js em hospedagem com Node.js).
- Agente real de IA conectado **apenas no servidor** a um provedor de LLM, com segredo em variável de ambiente; jamais incorporar chave no JavaScript do navegador.
- Ferramentas e base de conhecimento revisadas, limites por sessão, moderação, consentimento e tratamento de dados pessoais.
- Diagnóstico e contato via backend com armazenamento mínimo, opt-in, avisos de privacidade e integração por e-mail/CRM/n8n após confirmação do recebimento.
- Observabilidade, logs sem dados sensíveis, backups, fallback de contato humano e testes mobile.

## Hospedagem
GitHub Pages é adequado para protótipos, portfólios e demonstração, mas a documentação oficial proíbe sua utilização como hospedagem gratuita de negócio online ou site destinado principalmente a facilitar transações comerciais. Para a versão comercial final, migrar a hospedagem pública a provedor apto à operação empresarial. GitHub permanece repositório de código e automação de publicação.
Na Hostinger, `FastAPI/Python` requer VPS; hospedagem Business/Cloud selecionada pode receber apps Node.js, conforme plano e recursos oficiais. Comparar preço/limites com provedor gerenciado alternativo antes de contratar.
Não migrar antes de existir domínio registrado, credenciais e plano aprovado.

## Próximos marcos
1. Registrar `ekonomatica.com.br` (pedido preparado, pagamento pendente à última confirmação).
2. Validar domínio e publicar primeira versão em hospedagem comercial adequada; medir Core Web Vitals mobile do Brasil e do Paraguai.
3. Integrar backend e agente de IA real com resposta rastreável e encaminhamento ao humano.
4. Integrar captação real, CRM e propostas com consentimento e proteção de dados.
5. Publicar demonstrações isoladas, usando dados fictícios; conferir vídeos e autorização de terceiros.
6. Ativar analytics com transparência, monitoramento e SEO bilíngue.
