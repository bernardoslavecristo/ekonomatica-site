# Ekonomática — Plataforma comercial TECH (em desenvolvimento)

**Posicionamento principal:** consultoria de tecnologia especializada em agentes autônomos de IA, automação empresarial com n8n e Python, integrações APIs/webhooks, sistemas inteligentes e inteligência de dados. O site final deverá ser dinâmico, interativo e orientado à demonstração funcional de soluções e conversão comercial. O frontend estático existente é apenas uma base inicial, não a entrega final.

**Experiência econômica (como Serra do Sossego/SUDAM):** parte complementar do histórico profissional e portfólio, não foco da comunicação nem da prospecção. Atendimentos econômicos podem ser considerados sob demanda.

## Conteúdo
- ChefLú — demonstração de atendimento conversacional e automação WhatsApp
- Kaggriculture AI — agente autônomo em simulação agrícola, protótipo
- Impact Hub — desafio técnico de automação de notas fiscais (não implica implantação comercial)
- Simulador de Aluguéis — projeto imobiliário com parâmetros e cenários de simulação
- Nilo — projeto em revisão de documentação pública

## Experiência cinematográfica 3D (prévia isolada)

A prévia está em `experiencia-3d.html`, com estilos em `experiencia-3d.css` e cena Three.js em `experiencia-3d.js`. Possui núcleo 3D original com órbitas, malhas, partículas, iluminação, rotação e movimentos coordenados com rolagem. Em dispositivos lentos e modo de movimento reduzido, há alternativa estática. A página `index.html` continua sendo a entrada pública anterior até a aprovação de uma nova versão.

A cena ainda precisa passar por verificação visual real no Android e no desktop antes de substituir a homepage. Os scripts do consultor generativo permanecem incluídos na prévia, utilizando apenas o backend próprio da Ekonomática.

## Publicação e hospedagem
**Produção: VPS Hostinger Ubuntu 24.04 em operação no domínio `https://ekonomatica.com.br`**. O GitHub é repositório do código, não hospedagem do site. Não habilitar GitHub Pages.

Validação automática do código: `.github/workflows/validate.yml` (GitHub Actions a cada push). Publicação: `.github/workflows/deploy-hostinger.yml` com disparo manual explícito e autenticação SSH. A publicação NÃO está funcionando automaticamente até que o repositório disponha dos secrets `VPS_HOST`, `VPS_USER`, `VPS_SSH_KEY` e `VPS_KNOWN_HOSTS`, com chave de implantação autorizada na VPS. Nunca guardar chave privada, chave OpenAI, tokens ou senhas no GitHub. Ao configurar, preferir usuário dedicado e autenticação por chave, conferir fingerprint do servidor por canal confiável, e restringir permissões da chave.

**O código enviado ao GitHub não entra automaticamente no site público.** Até a configuração segura do deploy remoto, a VPS mantém a última versão publicada. O script `deploy-hostinger.sh` está disponível para publicação controlada na própria VPS.

## Checklist editorial antes de divulgar
- [ ] Confirmar titularidade e informações comerciais (nome, e-mail, enquadramento empresarial e condições)
- [ ] Verificar acesso e autorização de compartilhamento dos vídeos
- [ ] Revisar textos de projetos antes de atribuir resultados ou clientes
- [ ] Confirmar detalhes e materiais do projeto Nilo
- [ ] Testar acessibilidade, visual no Android e links finais

Contato informado: ekonomatica.consultoria@gmail.com. Não publicar documentos internos, leads, credenciais ou valores sem autorização.

## Continuidade
As decisões de produto, escopo, DNS e próxima etapa estão em [`DECISOES_E_CONTINUIDADE.md`](DECISOES_E_CONTINUIDADE.md). Consultar antes de propor a próxima ação ou mudar prioridades.
