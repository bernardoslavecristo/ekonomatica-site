# Planejador de colheita — demonstração comercial

Aplicação: `/colheita.html`. Escopo: uma cultura (alface), três canteiros, sete dias, pedidos e capacidade informados. A aplicação executa um modelo determinístico no navegador; não usa o agente Kaggriculture, previsão agronômica nem dados de fazendas reais.

## Regras

As duas rotinas usam o mesmo estoque e capacidade, priorizando lotes com vencimento mais próximo. Na rotina fixa, colhe-se até a meta diária. No plano, colhe-se até o pedido diário. Ambas respeitam capacidade e disponibilidade. Não há armazenamento pós-colheita nem transferência de pedidos. Excedente colhido e saldo no fim da janela são perdas hipotéticas. Todos os lotes encerram a janela até o dia 7.

A conservação deve ser respeitada: produção = entrega + perdas + saldo; pedidos = entrega + faltas. Não há promessa de melhora universal. As regras e limitações aparecem na interface. Alterar dados esconde resultados antigos até o recálculo. O CSV inclui entradas, plano, comparação e hipóteses.

## Caso inicial reproduzível

Produção: 830 pés; pedidos: 760; capacidade: 160/dia; meta fixa: 100/dia. Rotina fixa atende 610, com perdas de 220. Plano atende 760, com perdas de 70. Números ilustrativos, não evidência comercial ou de ganho de produtividade biológica. Com capacidade 70, ambos atendem 480 e perdem 350.

## Evolução para piloto

O piloto proposto começa por uma cultura e quatro semanas após avaliar uma amostra de uma semana. Coletar pedidos datados, disponibilidade/janelas, capacidade e registros de rotina. Definir critérios de entrega, descarte medido e tempo de planejamento, custos, investimento e suporte na proposta. Calibrar e comparar em campo antes de divulgar benefício comercial. Financiamento ou vínculo com Stellar não é declarado nesta demonstração.

## Verificação

- `node --test tests/colheita.test.cjs`
- `python3 scripts/check_static.py`
- `python3 -m pytest -q tests/test_api.py`
- `python3 scripts/verify_publication.py` após publicação

Dependência preexistente: `media/global-citizen-narrado.mp4` está presente na VPS e foi preservado na publicação. O arquivo foi recuperado também para a verificação local, mas não integra o envio de fontes pelo conector. Sua incorporação ao repositório permanece pendente; uma instalação limpa precisa desse arquivo para que a checagem de todas as páginas passe. Esta pendência não altera o cálculo nem os arquivos da aplicação de colheita.

Os scripts e estilos alterados usam uma versão na URL para evitar o reaproveitamento de arquivos anteriores pelo navegador após a publicação.
