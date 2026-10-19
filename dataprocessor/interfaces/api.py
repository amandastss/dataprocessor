from fastapi import FastAPI

from ..infra. fontes import fonte_a_partir_de_caminhos
from ..services.processamento import executar_processamento

app = FastAPI()

@app.get("/relatórios")
def relatorio():
    fonte = fonte_a_partir_de_caminhos(
        "data/clientes.csv",
        "data/transacoes.csv",
        "data/config.json"
    )
    resultado = executar_processamento(fonte)
    return resultado.to_dict()