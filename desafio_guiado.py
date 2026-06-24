from transformador import transformar_cliente

clientes = [
    {
        "id": 1,
        "nome": "  JOÃO SILVA  ",
        "email": "Joao.Silva@Email.com",
        "idade": 34,
        "cidade": "JOINVILLE",
        "data_cadastro": "2023-01-10"
    },
    {
        "id": 4,
        "nome": " ANA LIMA ",
        "email": "Ana.Lima@Email.com",
        "idade": 45,
        "cidade": "JOINVILLE",
        "data_cadastro": "2023-01-25"
    }
]

print("=== TRANSFORMAÇÃO ===")
print()

for cliente in clientes:
    print("ANTES:")
    print(
        f'  nome: "{cliente["nome"]}" | '
        f'email: "{cliente["email"]}" | '
        f'cidade: "{cliente["cidade"]}"'
    )

    transformado = transformar_cliente(cliente)

    print()
    print("DEPOIS:")
    print(
        f'  nome: "{transformado["nome"]}" | '
        f'email: "{transformado["email"]}" | '
        f'cidade: "{transformado["cidade"]}"'
    )

    print("-" * 40)