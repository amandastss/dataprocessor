


def total_aprovado(transacoes):
    return sum(t["valor"] for t in transacoes if t.get("status") == "aprovado")


def media_idade(clientes):
    idades = [c["idade"] for c in clientes if c.get("idade") is not None]
    if not idades:
        return 0
    return sum(idades) / len(idades)


def clientes_por_cidade(clientes):
    contagem = {}
    for c in clientes:
        cidade = c.get("cidade", "Desconhecida")
        contagem[cidade] = contagem.get(cidade, 0) + 1
    return contagem
