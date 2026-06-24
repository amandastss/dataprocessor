from leitor import carregar_clientes, carregar_transacoes, carregar_config
from validador import validar_cliente, validar_transacao, separar_registros
from transformador import transformar_clientes, transformar_transacoes
from processador import total_aprovado, media_idade, clientes_por_cidade

print("=== DataProcessor CLI ===")
print()

# LEITURA
clientes_raw = carregar_clientes("data/clientes.csv")
transacoes_raw = carregar_transacoes("data/transacoes.csv")
config = carregar_config("data/config.json")

print("[LEITURA]")
print(f"  clientes.csv ............. {len(clientes_raw)} registros")
print(f"  transacoes.csv ........... {len(transacoes_raw)} registros")
print("  config.json .............. OK")
print()

# VALIDAÇÃO
clientes_validos, clientes_invalidos = separar_registros(
    clientes_raw,
    validar_cliente
)

ids_validos = {c["id"] for c in clientes_validos}

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

# TRANSFORMAÇÃO
clientes = transformar_clientes(clientes_validos)
transacoes = transformar_transacoes(transacoes_validas)

print("[TRANSFORMAÇÃO]")
print(f"  {len(clientes)} clientes normalizados")
print(f"  {len(transacoes)} transações normalizadas")
print()

# MÉTRICAS
total = total_aprovado(transacoes)
media = media_idade(clientes)
por_cidade = clientes_por_cidade(clientes)

# RELATÓRIO FINAL
print("=== RELATÓRIO FINAL — DataProcessor ===")
print()

print(
    f"CLIENTES PROCESSADOS ({len(clientes)} válidos de {len(clientes_raw)})"
)

for c in clientes:
    print(
        f"  ID {c['id']} | {c['nome']} | "
        f"{c['email']} | {c['idade']} anos | {c['cidade']}"
    )

print()

print(f"CLIENTES REJEITADOS ({len(clientes_invalidos)})")

for item in clientes_invalidos:
    print(
        f"  ID {item['registro']['id']} - "
        f"{', '.join(item['erros'])}"
    )

print()

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

print(f"TRANSAÇÕES REJEITADAS ({len(transacoes_invalidas)})")

for item in transacoes_invalidas:
    print(
        f"  ID {item['registro']['id']} - "
        f"{', '.join(item['erros'])}"
    )

print()

print("MÉTRICAS")
print(f"  Total aprovado: R$ {total:.2f}")
print(f"  Média de idade (válidos): {media:.1f}")

print("  Clientes por cidade:")
for cidade, qtd in sorted(por_cidade.items()):
    print(f"    {cidade}: {qtd}")