# Colheita no Prazo — decisão sobre mão de obra

Aplicação `/equipe.html`, endpoint `POST /api/kaggriculture/equipe`. Interface própria de aplicativo, com etapas operação/equipe/decisão, navegação móvel e análise CSV. Destaque na abertura e no portfólio do site.

## Dor selecionada

Escassez de mão de obra na horticultura, documentada pela Hortifruti Brasil/Cepea em 14/08/2026: pesquisa com 105 produtores e agentes da cadeia. Fonte: https://www.hfbrasil.org.br/br/escassez-de-mao-de-obra-redefine-o-hortifruti-hf-brasil-269.aspx . A publicação contextualiza o problema, não valida ou endossa este produto. Os números comerciais do exemplo são fictícios e não vêm da pesquisa.

## Motor conectado

Usa `evaluate_helper` da Entrega 02, extraído do notebook de validação mínima. SHA-256 original de labor.py: `8f4050ca0f7f5182c718c0760d14076923c27856f4e54bd7ebdc4426144baa06`. Única alteração de adaptação no arquivo: import do planejador transformado em relativo (`from .planner import plan`). A lógica foi preservada e os seis casos de aceite da Entrega 02 foram conferidos pelo endpoint. O modelo treinado da competição não é usado.

## Regras e limites

Decisão de um dia, zero/um ajudante, lotes inteiros e kg inteiros. Otimiza contribuição após custos informados. Cobra diária inteira, deduzindo-a do caixa antes da receita. Transporte e comprador permanecem fixos. Reforço só é indicado com disponibilidade confirmada, caixa viável e diferença estritamente positiva. Empate mantém a equipe atual. A API limita a oito lotes para manter a enumeração exata pequena.

Custos e preços são dados de entrada. Resultado não é lucro líquido, garantia de renda nem previsão de perdas. Não contrata pessoas ou controla equipamentos. Não usa API generativa e não grava a entrada. Um lote fora do plano não é perda física comprovada.

## Exemplo

Caixa R$ 300; equipe 240 minutos; transporte 200 kg; comprador 180 kg. Ajudante disponível, 240 minutos, custo total R$ 100. Sem reforço: tomate A, resultado R$ 310. Com reforço: tomate A e alface B, receita R$ 700, custos R$ 240 e resultado R$ 460. Diferença R$ 150. Os resultados mudam quando diária, prontidão, caixa ou outros limites mudam.

## Verificação

`python -m pytest -q tests/test_api.py tests/test_harvest.py tests/test_crew.py`; `python3 scripts/check_static.py`; `node --check equipe.js`; teste visual em 390 pixels, decisões positiva/negativa/indisponibilidade e CSV antes da publicação.
