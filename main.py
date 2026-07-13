from dataprocessor.pipeline import executar_pipeline

def main():
    resultado = executar_pipeline(
        "data/clientes.csv",
        "data/transacoes.csv",
        "data/config.json",
    )

    print("=== DataProcessor ===")
    print(f"Clientes válidos: {len(resultado['clientes'])}")
    print(f"Clientes inválidos: {len(resultado['clientes_invalidos'])}")
    print(f"Transações válidas: {len(resultado['transacoes'])}")
    print(f"Transações inválidas: {len(resultado['transacoes_invalidas'])}")

    media = resultado["metricas"]["media_idade"]
    total = resultado["metricas"]["total_aprovado"]

    print(f"Média de idade: {media:.1f}")
    print(f"Total aprovado: R$ {total:.2f}")


if __name__ == "__main__":
    main()