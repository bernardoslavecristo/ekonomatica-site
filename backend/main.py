"""Primeira API dinâmica da Ekonomática.

Diagnóstico comercial técnico e estimativa ilustrativa, sem gravação de dados.
Não é um agente generativo e não executa automações de terceiros.
"""
from __future__ import annotations

from pathlib import Path
from typing import Literal

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, Field

app = FastAPI(
    title="Ekonomática - API",
    version="0.1.0",
    docs_url=None,
    redoc_url=None,
    openapi_url=None,
)

Area = Literal[
    "Atendimento e WhatsApp",
    "Documentos e notas fiscais",
    "Vendas e CRM",
    "Integração entre sistemas",
    "Agentes autônomos de IA",
    "Dados e análise econômica",
    "Outro processo",
]
Volume = Literal[
    "Até 50 tarefas por mês",
    "51 a 500 tarefas por mês",
    "Mais de 500 tarefas por mês",
    "Ainda não sei",
]
Urgencia = Literal[
    "Quero avaliar possibilidades",
    "Até 30 dias",
    "Entre 1 e 3 meses",
    "Acima de 3 meses",
]


class DiagnosticoEntrada(BaseModel):
    area: Area
    volume: Volume
    urgencia: Urgencia
    problema: str = Field(default="", max_length=1200)


class EstimativaEntrada(BaseModel):
    pessoas: int = Field(ge=1, le=10000)
    horas_semanais: float = Field(ge=0, le=168, allow_inf_nan=False)
    custo_hora: float = Field(ge=0, le=100000, allow_inf_nan=False)
    taxa_hipotetica: float = Field(ge=0, le=1, allow_inf_nan=False)


SOLUCOES = {
    "Atendimento e WhatsApp": (
        "Atendimento inteligente e integração comercial",
        "Mapear mensagens recebidas, categorias, horários e regras de transferência para uma pessoa.",
        [
            "Identificar canais, volume e tempo médio de resposta",
            "Definir respostas automáticas seguras e passagem para atendimento humano",
            "Avaliar integração com CRM, WhatsApp e sistemas existentes",
        ],
        "ChefLú — demonstração de automação de atendimento",
    ),
    "Documentos e notas fiscais": (
        "Automação documental com aprovação humana",
        "Organizar entrada de documentos, extração de campos, validação e tratamento de exceções.",
        [
            "Mapear fontes de arquivos e campos que precisam ser extraídos",
            "Definir regras de conferência, proteção de dados e aprovação humana",
            "Prototipar um fluxo n8n/Python com histórico das decisões",
        ],
        "Impact Hub — protótipo técnico de automação documental",
    ),
    "Vendas e CRM": (
        "Automação do funil comercial",
        "Conectar canais de contato a cadastros, acompanhamento e rotinas comerciais.",
        [
            "Identificar a origem dos leads e os campos realmente necessários",
            "Desenhar etapas do funil e regras de acompanhamento",
            "Integrar WhatsApp, formulários e CRM com consentimento apropriado",
        ],
        "ChefLú — demonstração de atendimento automatizado",
    ),
    "Integração entre sistemas": (
        "Integrações e APIs para eliminar retrabalho",
        "Conectar sistemas por APIs e webhooks, com tratamento de falhas e rastreabilidade.",
        [
            "Inventariar sistemas, APIs disponíveis e permissões",
            "Definir eventos, regras de transformação e resposta a erros",
            "Validar uma integração piloto e seus registros de operação",
        ],
        "Projetos de integração n8n, Python e APIs",
    ),
    "Agentes autônomos de IA": (
        "Agentes de IA com ferramentas e supervisão",
        "Definir tarefas delegáveis, limites de atuação, métricas e pontos de validação humana.",
        [
            "Especificar objetivo, ferramentas autorizadas e dados disponíveis",
            "Prototipar planejamento e execução em ambiente controlado",
            "Testar exceções, custo de inferência, auditoria e supervisão",
        ],
        "Kaggriculture AI — protótipo de agente em simulação",
    ),
    "Dados e análise econômica": (
        "Inteligência de dados para decisões",
        "Estruturar dados, indicadores, cenários e relatórios, conforme a questão empresarial.",
        [
            "Definir qual decisão precisa de apoio e as fontes de dados",
            "Conferir qualidade, periodicidade e permissões de acesso",
            "Desenvolver indicadores e um painel ou simulador verificável",
        ],
        "Global Citizen e Simulador de Aluguéis — experiências analíticas",
    ),
    "Outro processo": (
        "Mapeamento técnico e descoberta de oportunidades",
        "Conhecer o processo atual antes de sugerir uma tecnologia específica.",
        [
            "Descrever as etapas, responsáveis e ferramentas utilizadas",
            "Identificar tarefas repetitivas, falhas e integrações possíveis",
            "Definir escopo e critérios mensuráveis de um piloto",
        ],
        "Portfólio de automação e sistemas inteligentes",
    ),
}


@app.get("/api/health")
def health() -> dict[str, str]:
    return {"status": "ok", "service": "ekonomatica-api", "version": "0.1.0"}


@app.post("/api/diagnostico")
def diagnostico(dados: DiagnosticoEntrada) -> dict:
    titulo, explicacao, passos, exemplo = SOLUCOES[dados.area]
    return {
        "titulo": titulo,
        "orientacao": explicacao,
        "proximos_passos": passos,
        "exemplo_portfolio": exemplo,
        "contexto": {
            "area": dados.area,
            "volume": dados.volume,
            "urgencia": dados.urgencia,
        },
        "aviso": (
            "Pré-diagnóstico automatizado por regras. Não substitui análise humana "
            "nem significa que houve contratação, implantação ou economia comprovada."
        ),
        "armazenado": False,
    }


@app.post("/api/estimativa")
def estimativa(dados: EstimativaEntrada) -> dict:
    horas = dados.pessoas * dados.horas_semanais * 4.33 * dados.taxa_hipotetica
    valor_mensal = horas * dados.custo_hora
    return {
        "horas_recuperadas_mes": round(horas, 2),
        "valor_equivalente_mes": round(valor_mensal, 2),
        "valor_equivalente_ano": round(valor_mensal * 12, 2),
        "aviso": (
            "Cenário hipotético. Valor de horas não é economia financeira comprovada. "
            "Não inclui implantação, operação, supervisão ou custos de APIs."
        ),
        "armazenado": False,
    }


# Publica somente arquivos estáticos selecionados durante o build.
# Não expõe .env, código Python, documentação interna ou histórico do Git.
STATIC_DIR = Path(__file__).resolve().parent.parent / "public"
if STATIC_DIR.is_dir():
    app.mount("/", StaticFiles(directory=str(STATIC_DIR), html=True), name="public")
