"""Primeira API dinâmica da Ekonomática.

Diagnóstico comercial técnico e estimativa ilustrativa, sem gravação de dados.
Não é um agente generativo e não executa automações de terceiros.
"""
from __future__ import annotations

from pathlib import Path
from typing import Literal

from fastapi import FastAPI
from backend.ai_agent import router as ai_router
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, Field

app = FastAPI(
    title="Ekonomática - API",
    version="0.1.0",
    docs_url=None,
    redoc_url=None,
    openapi_url=None,
)

app.include_router(ai_router)

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


# Caixa de mensagens comerciais com retenção limitada e notificação Telegram opcional.
# Não é chat ao vivo; credenciais e dados ficam fora do repositório Git.
import os
import re
import sqlite3
import time
from datetime import datetime, timedelta, timezone
from threading import Lock, Thread
from urllib.parse import urlencode
from urllib.request import Request as URLRequest, urlopen
from fastapi import Header, HTTPException, Request, Response
from pydantic import field_validator

DB_PATH = os.environ.get("EKONOMATICA_CONTACT_DB", "/app/data/contatos.sqlite3")
_contact_lock = Lock()
_recent_requests: list[float] = []


class ContatoEntrada(BaseModel):
    nome: str = Field(min_length=2, max_length=100)
    contato: str = Field(min_length=6, max_length=160)
    assunto: str = Field(min_length=2, max_length=120)
    mensagem: str = Field(min_length=10, max_length=2000)
    consentimento: bool
    idioma: Literal["pt", "es"] = "pt"
    website: str = Field(default="", max_length=250)

    @field_validator("contato")
    @classmethod
    def validar_contato(cls, value: str) -> str:
        value = value.strip()
        email = re.fullmatch(r"[^\s@]+@[^\s@]+\.[^\s@]+", value)
        telegram = re.fullmatch(r"@[a-zA-Z0-9_]{5,32}", value)
        if not (email or telegram):
            raise ValueError("Informe um e-mail ou identificador do Telegram válido")
        return value


def _db() -> sqlite3.Connection:
    from pathlib import Path
    Path(DB_PATH).parent.mkdir(parents=True, exist_ok=True)
    con = sqlite3.connect(DB_PATH, timeout=5)
    con.execute("CREATE TABLE IF NOT EXISTS contatos (id INTEGER PRIMARY KEY AUTOINCREMENT, criado_utc TEXT NOT NULL, nome TEXT NOT NULL, contato TEXT NOT NULL, assunto TEXT NOT NULL, mensagem TEXT NOT NULL, idioma TEXT NOT NULL)")
    return con


@app.post("/api/contato", status_code=201)
def receber_contato(dados: ContatoEntrada, request: Request) -> dict:
    if not dados.consentimento:
        raise HTTPException(status_code=422, detail="Consentimento necessário")
    # Honeypot antispam: nenhum registro, resposta não reveladora.
    if dados.website:
        return {"recebido": True}
    # Limite global de carga para proteger uma VPS pequena (sem armazenar IP).
    now = time.monotonic()
    with _contact_lock:
        _recent_requests[:] = [x for x in _recent_requests if now - x < 60]
        if len(_recent_requests) >= 40:
            raise HTTPException(status_code=429, detail="Muitas solicitações. Tente novamente.")
        _recent_requests.append(now)
    try:
        with _contact_lock:
            with _db() as con:
                # Retenção automática de 90 dias no envio de novas solicitações.
                cutoff = (datetime.now(timezone.utc) - timedelta(days=90)).isoformat()
                con.execute("DELETE FROM contatos WHERE criado_utc < ?", (cutoff,))
                cursor = con.execute(
                    "INSERT INTO contatos(criado_utc,nome,contato,assunto,mensagem,idioma) VALUES (?,?,?,?,?,?)",
                    (datetime.now(timezone.utc).isoformat(), dados.nome.strip(), dados.contato,
                     dados.assunto.strip(), dados.mensagem.strip(), dados.idioma),
                )
                contact_id = cursor.lastrowid
    except sqlite3.Error:
        raise HTTPException(status_code=503, detail="Serviço temporariamente indisponível")

    # Opcional: informe token e chat_id SOMENTE no .env da VPS; nenhuma credencial no Git.
    token = os.environ.get("TELEGRAM_BOT_TOKEN", "").strip()
    chat_id = os.environ.get("TELEGRAM_CHAT_ID", "").strip()
    if token and chat_id:
        try:
            notify = (
                f"Ekonomática: novo contato #{contact_id}\n"
                f"Nome: {dados.nome[:100]}\nCanal: {dados.contato[:160]}\n"
                f"Assunto: {dados.assunto[:120]}\n"
                f"Mensagem: {dados.mensagem[:1200]}"
            )
            body = urlencode({"chat_id": chat_id, "text": notify}).encode("utf-8")
            req = URLRequest(
                f"https://api.telegram.org/bot{token}/sendMessage",
                data=body, method="POST",
            )
            with urlopen(req, timeout=4):
                pass
        except Exception:
            # A entrega da mensagem no DB independe de alerta externo.
            pass
    return {"recebido": True, "referencia": contact_id}


@app.get("/api/admin/contatos")
def listar_contatos(response: Response, x_admin_token: str | None = Header(default=None)) -> dict:
    import secrets
    response.headers["Cache-Control"] = "no-store"
    expected = os.environ.get("EKONOMATICA_ADMIN_TOKEN", "")
    if not expected or not x_admin_token or not secrets.compare_digest(expected, x_admin_token):
        raise HTTPException(status_code=404, detail="Não encontrado")
    with _contact_lock:
        with _db() as con:
            con.row_factory = sqlite3.Row
            rows = con.execute(
                "SELECT id, criado_utc, nome, contato, assunto, mensagem, idioma FROM contatos ORDER BY id DESC LIMIT 100"
            ).fetchall()
    return {"contatos": [dict(row) for row in rows]}

def _retencao_periodica() -> None:
    """Remove mensagens antigas a cada seis horas enquanto a API estiver no ar."""
    while True:
        try:
            cutoff = (datetime.now(timezone.utc) - timedelta(days=90)).isoformat()
            with _contact_lock:
                with _db() as con:
                    con.execute("DELETE FROM contatos WHERE criado_utc < ?", (cutoff,))
        except (OSError, sqlite3.Error):
            pass
        time.sleep(6 * 60 * 60)


@app.on_event("startup")
def iniciar_retencao() -> None:
    Thread(target=_retencao_periodica, name="retencao-contatos", daemon=True).start()


# Publica somente arquivos estáticos selecionados durante o build.
# Não expõe .env, código Python, documentação interna ou histórico do Git.
STATIC_DIR = Path(__file__).resolve().parent.parent / "public"
if STATIC_DIR.is_dir():
    app.mount("/", StaticFiles(directory=str(STATIC_DIR), html=True), name="public")

