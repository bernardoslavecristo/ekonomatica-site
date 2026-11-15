from fastapi.testclient import TestClient

from backend.main import app

client = TestClient(app)


def test_health():
    r = client.get("/api/health")
    assert r.status_code == 200
    assert r.json()["status"] == "ok"


def test_diagnostico_agentes():
    r = client.post("/api/diagnostico", json={
        "area": "Agentes autônomos de IA",
        "volume": "51 a 500 tarefas por mês",
        "urgencia": "Até 30 dias",
        "problema": "Executar tarefas com aprovacao humana",
    })
    assert r.status_code == 200
    assert "Agentes de IA" in r.json()["titulo"]
    assert r.json()["armazenado"] is False
    assert len(r.json()["proximos_passos"]) == 3


def test_diagnostico_rejeita_area_desconhecida():
    r = client.post("/api/diagnostico", json={
        "area": "x", "volume": "Ainda não sei",
        "urgencia": "Quero avaliar possibilidades",
    })
    assert r.status_code == 422


def test_estimativa():
    r = client.post("/api/estimativa", json={
        "pessoas": 3, "horas_semanais": 8,
        "custo_hora": 40, "taxa_hipotetica": 0.30,
    })
    assert r.status_code == 200
    assert r.json()["horas_recuperadas_mes"] == 31.18
    assert r.json()["armazenado"] is False


def test_estimativa_rejeita_dados_invalidos():
    r = client.post("/api/estimativa", json={
        "pessoas": 0, "horas_semanais": 1000,
        "custo_hora": 40, "taxa_hipotetica": 1.5,
    })
    assert r.status_code == 422
