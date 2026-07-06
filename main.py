from leitor import carregar_clientes, carregar_transacoes, carregar_config
from validador import validar_cliente, validar_transacao, separar_registros
from transformador import transformar_clientes, transformar_transacoes
from processador import total_aprovado, media_idade, clientes_por_cidade


print("=== DataProcessor CLI ===")
print()


#todos os dados ficam carregados na memória.

clientes_raw = carregar_clientes("data/clientes.csv")
transacoes_raw = carregar_transacoes("data/transacoes.csv")
config = carregar_config("data/config.json")

print("[LEITURA]")
print(f"  clientes.csv ............. {len(clientes_raw)} registros")
print(f"  transacoes.csv ........... {len(transacoes_raw)} registros")
print("  config.json .............. OK")
print()



# Cada cliente é enviado para validar_cliente e vai enviar like two listas de green e red

clientes_validos, clientes_invalidos = separar_registros(
    clientes_raw,
    validar_cliente
)



ids_validos = {c["id"] for c in clientes_validos} #valida a trsansacao criando um conjunto de idds


transacoes_validas, transacoes_invalidas = separar_registros(
    transacoes_raw,
    validar_transacao,
    ids_clientes=ids_validos,
    config=config
)

print("[VALIDAÇÃO]")
print(f"  Clientes válidos: {len(clientes_validos)} / {len(clientes_raw)}")
print(f"  Transações válidas: {len(transacoes_validas)} / {len(transacoes_raw)}")
print()

clientes = transformar_clientes(clientes_validos)
transacoes = transformar_transacoes(transacoes_validas)

print("[TRANSFORMAÇÃO]")
print(f"  {len(clientes)} clientes normalizados")
print(f"  {len(transacoes)} transações normalizadas")
print()



# Calcula info apenas com registros válido, soma as transações e calcula a media de idade alem decontar quantos cli p cdd.

total = total_aprovado(transacoes)
media = media_idade(clientes)
por_cidade = clientes_por_cidade(clientes)


# Exibe todas as informações processadas pelo sistema.

print("=== RELATÓRIO FINAL — DataProcessor ===")
print()


# Mostra apenas os clientes aprovados na validação.

print(
    f"CLIENTES PROCESSADOS ({len(clientes)} válidos de {len(clientes_raw)})"
)

for c in clientes:
    print(
        f"  ID {c['id']} | {c['nome']} | "
        f"{c['email']} | {c['idade']} anos | {c['cidade']}"
    )

print()



# Mostra os clientes inválidos e o motivo da rejeição.

print(f"CLIENTES REJEITADOS ({len(clientes_invalidos)})")

for item in clientes_invalidos:
    registro = item["registro"]
    erros = ", ".join(item["erros"])

    print(
        f"  ID {registro['id']} - "
        f"{registro['nome']}: {erros}"
    )

print()

# Exibe apenas as transações aprovadas na validação.

print(
    f"TRANSAÇÕES PROCESSADAS "
    f"({len(transacoes)} válidas de {len(transacoes_raw)})"
)

for t in transacoes:
    print(
        f"  ID {t['id']} | cliente {t['cliente_id']} | "
        f"R$ {t['valor']:.2f} | {t['categoria']} | {t['status']}"
    )

print()

# Exibe as transações inválidas e seus respectivos erros.

print(f"TRANSAÇÕES REJEITADAS ({len(transacoes_invalidas)})")

for item in transacoes_invalidas:
    print(
        f"  ID {item['registro']['id']} - "
        f"{', '.join(item['erros'])}"
    )

print()


# Mostra os cálculos realizados durante o processamento.

print("MÉTRICAS")
print(f"  Total aprovado: R$ {total:.2f}")
print(f"  Média de idade (válidos): {media:.1f}")

print("  Clientes por cidade:")
for cidade, qtd in sorted(por_cidade.items()):
    print(f"    {cidade}: {qtd}")