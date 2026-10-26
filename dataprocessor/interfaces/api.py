from pathlib import Path
from typing import Literal

from fastapi import FastAPI, Response

from ..core.entidades import Cliente, Transacao
from ..infra.fontes import FonteDadosMemoria, fonte_a_partir_de_caminhos
from ..infra.relatorios import criar_gerador
from ..services.processamento import executar_processamento
from .schemas import (
    ClienteSchema,
    MetricasSchema,
    ProcessamentoEntrada,
    TransacaoSchema,
)

app = FastAPI(
    title="DataProcessor API",
    description="API para processar clientes e transações.",
    version="1.0.0",
)

DATA_DIR = Path(__file__).resolve().parents[2] / "data"
MEDIA_TYPES = {
    "texto": "text/plain",
    "json": "application/json",
    "csv": "text/csv",
}


def carregar_resultado():
    """Carrega os arquivos padrão e executa o processamento uma vez por chamada."""
    fonte = fonte_a_partir_de_caminhos(
        DATA_DIR / "clientes.csv",
        DATA_DIR / "transacoes.csv",
        DATA_DIR / "config.json",
    )
    return executar_processamento(fonte)


def resumir(resultado) -> MetricasSchema:
    return MetricasSchema(
        clientes_validos=len(resultado.clientes),
        clientes_invalidos=len(resultado.clientes_invalidos),
        transacoes_validas=len(resultado.transacoes),
        transacoes_invalidas=len(resultado.transacoes_invalidas),
        media_idade=resultado.media_idade,
        total_aprovado=resultado.total_aprovado,
    )


@app.get("/clientes", response_model=list[ClienteSchema], tags=["Clientes"])
def listar_clientes():
    return carregar_resultado().clientes


@app.get("/metricas", response_model=MetricasSchema, tags=["Métricas"])
def metricas():
    return resumir(carregar_resultado())


@app.get("/transacoes", response_model=list[TransacaoSchema], tags=["Transações"])
def listar_transacoes(
    status: Literal["aprovado", "pendente", "recusado"] | None = None,
    categoria: str | None = None,
    cliente_id: int | None = None,
):
    transacoes = carregar_resultado().transacoes
    if status is not None:
        transacoes = [transacao for transacao in transacoes if transacao.status == status]
    if categoria is not None:
        transacoes = [
            transacao for transacao in transacoes if transacao.categoria == categoria
        ]
    if cliente_id is not None:
        transacoes = [
            transacao for transacao in transacoes if transacao.cliente_id == cliente_id
        ]
    return transacoes


@app.get("/relatorio/{formato}", tags=["Relatórios"])
def relatorio_formatado(formato: Literal["texto", "json", "csv"]):
    conteudo = criar_gerador(formato).render(carregar_resultado())
    return Response(content=conteudo, media_type=MEDIA_TYPES[formato])


@app.post("/processar", response_model=MetricasSchema, tags=["Processamento"])
def processar(entrada: ProcessamentoEntrada):
    fonte = FonteDadosMemoria(
        clientes=[Cliente(**cliente.model_dump()) for cliente in entrada.clientes],
        transacoes=[
            Transacao(**transacao.model_dump()) for transacao in entrada.transacoes
        ],
        config=entrada.config.model_dump(),
    )
    return resumir(executar_processamento(fonte))
