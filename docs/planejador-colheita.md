# Kaggriculture — módulo de colheita 0.2

Aplicação: `/colheita.html`. Endpoint: `POST /api/kaggriculture/colheita`. Estado: `GET /api/kaggriculture/status`. Sem gravação de entradas, sem LLM e sem ações externas. A interface não calcula um resultado alternativo nem informa conexão ativa quando a API falha.

## Integração e procedência

O módulo `backend/kaggriculture/field_pilot/harvest.py` estende o projeto experimental field_pilot para pés de alface, lotes divisíveis e sete datas. Preservamos `field_pilot/planner.py` e `__init__.py` da validação mínima da Entrega 02. Os conteúdos foram extraídos por AST e literal_eval do notebook, sem executar células. SHA-256 do planejador preservado: `4c0df3c901a90ce7bcb83de78eb80625ba8bfa03450a35117436be83216c4f72`. Fonte: `Kaggriculture_Entrega02_Validacao_Minima_Android.ipynb`; o notebook referencia a Entrega 02 do Drive `1jAuu8Qp0Ue97s8PCww9bGrfuENZ2gukR`.

O endpoint chama a extensão de colheita, não o otimizador original de lotes inteiros. A política treinada da competição Kaggle, seus pesos e previsões agronômicas continuam sem conexão. Esse limite aparece na interface, na resposta e no CSV. Não representa confirmação de execução Android nem resultado comercial.

## Entradas e regras

Semana de sete dias com data inicial; três canteiros e sete pedidos editáveis na interface. A API aceita até dez canteiros e trinta pedidos. Quantidades inteiras não negativas até 100.000; data de entrega dentro da semana; identificadores únicos; prontidão anterior ou igual ao prazo limite.

Mesma produção e capacidade nas duas rotinas. Rotina fixa tenta colher a meta diária; plano limita a colheita ao pedido do dia. Lotes prontos com prazo limite mais próximo têm prioridade, desempate por identificador. Sem estoque pós-colheita, sem carregar pedidos faltantes. Pedidos na mesma data dividem as entregas na ordem da entrada. Produção que vence após a semana permanece no saldo. Não é otimização global nem previsão biológica.

Conservação: produção = entregas + perdas + saldo. Pedidos = entregas + faltas. Cada data recebe explicações sobre seleção, falta de capacidade, disponibilidade e vencimento. Resultado inclui SHA-256 da entrada para rastreabilidade sem armazenar dados.

## Testes

`python -m pytest -q tests/test_api.py tests/test_harvest.py`; `node --test tests/colheita.test.cjs`; `python3 scripts/check_static.py`. Validar interface móvel, API, CSV e falha de conexão antes da publicação. A comparação inicial continua com 610 pés entregues na rotina fixa e 760 no plano, para dados fictícios.

Pendência preexistente de fonte: o vídeo Global Citizen está na VPS e foi preservado; não está versionado no repositório. Uma instalação limpa precisa desse arquivo para a checagem de todos os recursos. Não é dependência do módulo de colheita.


## Interface Semana da Colheita — 26/11/2026

O planejador agora é um aplicativo com três etapas: Minha semana, Meus canteiros e Meu plano. Mantém a API e as regras anteriores, oferece cartões diários e tabela completa, comparação e CSV. A tela de resultado só fica disponível após resposta válida; editar as entradas invalida o resultado. Campos inválidos levam à etapa correspondente. Interface própria em azul petróleo e lima, com navegação inferior no celular e acesso ao Colheita no Prazo. Dados fictícios e limitações seguem visíveis.
