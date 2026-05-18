
import unicodedata


def _remover_acentos(texto):
    nfkd = unicodedata.normalize("NFKD", texto)
    return "".join(c for c in nfkd if not unicodedata.combining(c))


def normalizar_nome(nome):
    if not nome:
        return ""
    return nome.strip().title()


def normalizar_email(email):
    if not email:
        return ""
    return email.strip().lower()


def normalizar_cidade(cidade):
    if not cidade:
        return ""
    return _remover_acentos(cidade.strip()).title()


def transformar_cliente(cliente):
    return {
        "id": cliente["id"],
        "nome": normalizar_nome(cliente.get("nome", "")),
        "email": normalizar_email(cliente.get("email", "")),
        "idade": cliente["idade"],
        "cidade": normalizar_cidade(cliente.get("cidade", "")),
        "data_cadastro": cliente.get("data_cadastro", "").strip(),
    }


def transformar_transacao(transacao):
    return {
        "id": transacao["id"],
        "cliente_id": transacao["cliente_id"],
        "valor": transacao["valor"],
        "categoria": transacao.get("categoria", "").strip().lower(),
        "data": transacao.get("data", "").strip(),
        "status": transacao.get("status", "").strip().lower(),
    }


def transformar_clientes(clientes):
    return [transformar_cliente(c) for c in clientes]


def transformar_transacoes(transacoes):
    return [transformar_transacao(t) for t in transacoes]
