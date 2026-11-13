# Domínios comerciais — Ekonomática (Brasil e Paraguai)

## Status da verificação — 13/11/2026
- Repositório e workflow do Pages existentes; implantação pública ainda não confirmada.
- Registro.br confirma que a compra exige consulta oficial de disponibilidade e CPF/CNPJ do titular. Consulta de disponibilidade do nome específico **não foi conclusiva** nesta execução.
- NIC-PY confirma categoria `.com.py` e necessidade de contato local para registro por empresa estrangeira. Consulta de disponibilidade do nome específico **não foi conclusiva** nesta execução.
- **Nenhum domínio registrado, comprado ou configurado no DNS.**
- Não declarar qualquer domínio como disponível antes de consultar os registradores na tela de cadastro.

## Objetivo
Manter a hospedagem de GitHub Pages e apresentar um domínio comercial ao cliente. A existência de URLs pretendidas abaixo NÃO comprova sua disponibilidade nem propriedade.

- **Brasil (principal pretendido):** `ekonomatica.com.br`
- **Paraguai (domínio secundário pretendido):** `ekonomatica.com.py`
- **Presença no Paraguai antes do segundo registro:** página em espanhol `paraguai.html` do domínio brasileiro, após registro.

## Dependências antes de qualquer ativação
1. Consultar disponibilidade em https://registro.br/ e https://www.nic.py/.
2. Registrar o domínio brasileiro no CPF/CNPJ autorizado, e guardar comprovante e acesso.
3. Para .com.py, confirmar requisitos e, se pessoa jurídica estrangeira, a necessidade de contato/representante residente no Paraguai; registrar pelo NIC-PY conforme seus procedimentos.
4. Confirmar a publicação do GitHub Pages em Settings → Pages → Source: GitHub Actions.
5. Em Settings → Pages → Custom domain, inserir o domínio **já registrado e sob controle do titular** (ex.: `www.ekonomatica.com.br`), salvar e ativar HTTPS depois de DNS válido.
6. Configurar no DNS do domínio brasileiro, **após controle do domínio**:
   - `www` → CNAME `bernardoslavecristo.github.io`
   - `@` → registros A `185.199.108.153`, `185.199.109.153`, `185.199.110.153`, `185.199.111.153`
7. Após propagação e certificado HTTPS, alterar URLs canônicas, sitemap, robots e hreflang no site para o domínio efetivo.
8. Somente depois de controlar o .com.py, definir redirecionamento HTTP 301/308 seguro via provedor que suporte redirecionamento HTTPS para domínio secundário (registro DNS, sozinho, não efetua redirecionamento): `ekonomatica.com.py` → `https://www.ekonomatica.com.br/paraguai.html`. O GitHub Pages de um repositório não aceita dois domínios apex independentes como domínio personalizado.
9. Testar www, domínio raiz, HTTPS, versão em espanhol e envio de e-mail de contato.

**Nunca criar um CNAME no GitHub para um domínio ainda não registrado.** No workflow customizado GitHub Actions, arquivo `CNAME` não configura o domínio; é necessário usar Settings → Pages.

## Observações
- Custo, disponibilidade e registro devem ser confirmados diretamente pelos registradores.
- O registro é uma compra separada da hospedagem gratuita do GitHub Pages.
- O conteúdo para clientes no Paraguai não pressupõe estabelecimento fiscal no Paraguai ou prestação de assessoria tributária/jurídica.
- Fontes: https://docs.github.com/en/pages/configuring-a-custom-domain-for-your-github-pages-site/managing-a-custom-domain-for-your-github-pages-site ; https://www.nic.py/ayuda.php ; https://www.nic.py/politicas-de-delegacion.php
