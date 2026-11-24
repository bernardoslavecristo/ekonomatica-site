# Verificação da publicação — 23/11/2026

Produção deve continuar na VPS Hostinger, em https://ekonomatica.com.br. GitHub Pages permanece desativado.

## Preparado no código
- ChefLú: arquivo narrado original incorporado, 1280×864, 64,6 segundos, vídeo e áudio; controles nativos, tela cheia e carregamento sob demanda.
- Impact Hub: apresentação YouTube PSgtg2YDMK0 vinculada, sem abrir e-mail para assistir; descrição distingue protótipo e evoluções planejadas.
- Kaggriculture: demonstração preservada; página 360° com arrasto, rotação automática opcional e teclado.
- Menus de portfólio, vídeos e diagnóstico acessíveis em celular.
- Corrigidos atalhos antigos e âncoras quebradas das páginas Kaggriculture.
- Deploy deve falhar quando páginas, conteúdo da versão ou arquivo MP4 não forem encontrados.

## Confirmações necessárias na produção
- Publicar a revisão da main na VPS por deploy-hostinger.sh.
- Executar python3 scripts/verify_publication.py; só considerar publicado se finalizar com código zero.
- Conferir reprodução, áudio e legibilidade do ChefLú em tela cheia.
- Conferir reprodução dos vídeos externos em sessão sem login.
- Testar rotação e reset da identidade 360°.
- Testar formulário e notificações conforme configuração privada da VPS; não criar leads fictícios como se fossem reais.
- Conferir consultor generativo com a configuração existente, sem expor chaves ou alterar limites de uso.
- Testar em Android real. Emulação e prévia não confirmam execução no aparelho do usuário.

## Limite constatado nesta revisão
A consulta pública anterior à publicação encontrou /apresentacoes.html com HTTP 404. O navegador da Hostinger exigiu login. Commit no GitHub não comprova implantação na VPS.
