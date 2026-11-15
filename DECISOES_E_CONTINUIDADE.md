# Ekonomática — Decisões de produto e continuidade
Atualizado em 14/11/2026 (horário de São Paulo). Documento de referência para continuar o projeto sem repetir decisões já tomadas.

## 1. Objetivo já decidido (não reabrir sem solicitação)
A Ekonomática **não** deve ser apenas um site institucional estático ou vitrine de portfólio. Deve ser uma **plataforma comercial dinâmica e interativa**, com experiência de usuário de alto nível, para que empresários experimentem as soluções, entendam benefícios reais e tenham vontade de contratar.
O critério de sucesso inicial é **qualidade da experiência e conversão comercial**, não suportar centenas de acessos simultâneos. A marca ainda está em fase de divulgação.
Hospedagem no GitHub Pages **não atende sozinha** ao produto desejado; GitHub permanece como repositório do código. Não voltar a sugerir GitHub Pages como solução principal de execução do produto.

## Posicionamento comercial — DECISÃO PRIORITÁRIA
**A Ekonomática é uma consultoria TECH, não uma consultoria econômica generalista.**
Sua atividade principal, marca, marketing, experiência do site, demonstrações, chamadas comerciais e prospecção devem vender **agentes autônomos de IA, automação com n8n e Python, integrações de APIs, sistemas inteligentes e inteligência de dados**.
As experiências de economia, estudos de viabilidade, engenharia econômica e projeto de incentivo fiscal Serra do Sossego devem permanecer como **itens complementares do currículo/portfólio**, sem protagonismo no site, sem orientarem o funil comercial e sem virar eixo principal da consultoria.
Trabalhos econômicos podem ser considerados **apenas se aparecer demanda compatível**, sem campanha prioritária ou mudança do foco TECH. Não interpretar a explicação do objetivo de um projeto do portfólio como mudança do objetivo da empresa.
Na ordem visual e comercial, mostrar primeiro soluções TECH e demonstrações interativas, depois histórico complementar.

## 2. Funcionalidades a construir
- Frontend premium, rápido e intuitivo, com navegação otimizada para Android e desktop.
- Português e espanhol, para atuação no Brasil e foco especial em empresários brasileiros e clientes no Paraguai.
- Consultor virtual de IA que compreende necessidades do empresário e recomenda soluções da Ekonomática.
- Diagnóstico guiado de negócio, simuladores de economia, produtividade e ROI com hipóteses transparentes.
- **Demonstrações interativas funcionais**, em que o visitante possa testar, ver etapas, operações e resultados — não apenas ler textos ou assistir vídeos.
- Portfólio técnico com provas reais, vídeos demonstrativos e estado de maturidade honesto (protótipos/demonstrações versus implantações comerciais).
- Conversão: captar leads, oferecer diagnóstico/proposta e contato por WhatsApp, com permissões e proteção de dados adequadas.
- Integrações reais com backend, automações e eventualmente CRM/n8n.
- Experiência envolvente e confiável, sem exagerar capacidades ou resultados.

## 3. Arquitetura e custos
- Domínio principal: **ekonomatica.com.br**, compra já confirmada pelo usuário em 14/11/2026.
- Hostinger gerencia atualmente nameservers e registros DNS.
- GitHub: repositório principal **bernardoslavecristo/ekonomatica-site** (branch main).
- **Hospedagem de execução**: VPS Hostinger (plano KVM 2 em consideração) ou infraestrutura equivalente capaz de rodar aplicações; decisão de avaliar custo/condições antes de contratar. Não tratar VPS como já comprada.
- Frontend e backend podem ser separados; backend poderá usar Python/FastAPI, PostgreSQL e n8n quando implementados e adequados. Consumo de APIs de IA e manutenção têm custos adicionais.
- Não prometer hospedagem de modelos pesados localmente ou alto volume sem dimensionamento.
- Não mudar DNS para GitHub Pages: o plano de hospedagem de produção foi reconsiderado e o endereço deve apontar para a infraestrutura escolhida **quando ela estiver pronta**.

## 4. Situação do DNS observada em prints da Hostinger em 14/11/2026
- Nameservers: `artemis.dns-parking.com` e `hermes.dns-parking.com`.
- Registro A: nome `@`, conteúdo `2.57.91.91` (Hostinger), TTL mostrado `50`.
- Registro CNAME: nome `www`, conteúdo `ekonomatica.com.br`, TTL `300`.
- **Nada foi comprovadamente alterado**. Não remover/redefinir DNS prematuramente. Preservar registros de e-mail e demais serviços, caso existam.

## 5. Portfólio e atuação que devem permanecer no escopo
- ChefLú — automação/assistente comercial no WhatsApp, demonstração real.
- Kaggriculture AI — agente autônomo/experimentos em simulação agrícola; comunicar estágio de protótipo.
- Impact Hub — desafio/protótipo de automação de notas fiscais; não apresentar como implantação comercial.
- Nilo — agente de IA/Python com testes, incluir explicitamente nas demos.
- Simulador de Aluguéis — simulador de cenários para decisões imobiliárias.
- **Mineração Serra do Sossego S/A (Carajás/PA, 2000)**: projeto de lavra e beneficiamento de cobre com objetivo principal de **pleitear incentivo fiscal junto à SUDAM**. Bernardo integrou a equipe técnica de elaboração, como economista (CORECON/PA nº 3719), atuando na avaliação econômico-financeira/viabilidade. Acompanhamento formal do pleito foi designado a outro consultor; não apresentar como incentivo aprovado ou captado. Documento-fonte na biblioteca: `RESPONSABILIDADE TECNICA PERANTE A SUDAM.docx`.
- **Histórico econômico complementar**: incentivos fiscais ao investimento, engenharia econômica, modelagem financeira, análise de investimentos e impactos de empreendimentos. Manter no portfólio de experiências; **não promover como linha principal de serviços da Ekonomática**.
- Projeto de inteligência de dados **Global Citizen** (grafia corrigida pelo usuário; não confundir com Global Cities), com aplicações na construção civil e outras áreas a confirmar.
- Projetos adicionais somente se houver evidência ou descrição confirmada.
- **Posicionamento exclusivo de protagonismo comercial:** tecnologia, agentes autônomos de IA, automação n8n/Python, APIs/webhooks, desenvolvimento de sistemas inteligentes e inteligência de dados. Economia é competência complementar, eventualmente oferecida sob demanda.

## 6. Modo de trabalho estabelecido
- Continuar exatamente de onde parou; **não fazer perguntas já respondidas, nem propor novamente decisões encerradas**.
- Conduzir etapa por etapa pelo Android, com instruções simples e verificações objetivas.
- Separar confirmado de pendente; nunca afirmar publicação, pagamento, contratação, mudança DNS ou integração sem evidência.
- Priorizar a construção do produto utilizável e excelente para usuários, depois SEO/campanhas e escala.
- Não executar a rota de GitHub Pages como hospedagem final por inércia; revisar o plano diante da decisão de produto dinâmico.

## 7. Situação e próximo passo
Confirmados: domínio comprado; repositório existe; conceito de plataforma dinâmica, interativa e comercial definido; DNS atual visto nos prints.
Pendentes: contratar/configurar serviço de execução, determinar arquitetura operacional, implantar backend e demos, configurar domínio/HTTPS após infraestrutura pronta, testar experiência Android e fluxos de conversão.
**Próxima ação:** revisar a oferta vigente de VPS da Hostinger, custos reais de contratação e renovação, e preparar um plano técnico de implantação sem mexer no DNS prematuramente.

Este documento é uma referência de projeto no GitHub, e não substitui a memória pessoal do ChatGPT.
