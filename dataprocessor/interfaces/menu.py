from pathlib import Path

from ..infra.fontes import FonteDadosArquivos
from ..infra.relatorios import criar_gerador
from ..services.processamento import executar_processamento


def processar():
    caminho_clientes = input(
        "Caminho do CSV de clientes [data/clientes.csv]: "
    ).strip() or "data/clientes.csv"
    caminho_transacoes = input(
        "Caminho do CSV de transações [data/transacoes.csv]: "
    ).strip() or "data/transacoes.csv"
    caminho_config = input(
        "Caminho do JSON de config [data/config.json]: "
    ).strip() or "data/config.json"

    fonte = FonteDadosArquivos(
        caminho_clientes,
        caminho_transacoes,
        caminho_config,
    )
    resultado = executar_processamento(fonte)
    print(f"Clientes válidos: {len(resultado.clientes)}")
    print(f"Transações válidas: {len(resultado.transacoes)}")
    return resultado


def exibir_relatorio(resultado):
    formato = input("Formato (texto/json/csv) [texto]: ").strip() or "texto"
    gerador = criar_gerador(formato)
    print(gerador.render(resultado))


def salvar_relatorio(resultado):
    formato = input("Formato (texto/json/csv) [texto]: ").strip() or "texto"
    gerador = criar_gerador(formato)
    relatorio = gerador.render(resultado)

    extensao = "txt" if formato == "texto" else formato
    caminho_padrao = Path("output") / f"relatorio.{extensao}"
    caminho = Path(
        input(f"Caminho do arquivo [{caminho_padrao}]: ").strip()
        or caminho_padrao
    )

    caminho.parent.mkdir(parents=True, exist_ok=True)
    caminho.write_text(relatorio, encoding="utf-8")
    print(f"Relatório salvo em: {caminho}")


def menu_principal():
    resultado = None

    while True:
        print("\n=== DataProcessor — Menu ===")
        print("1. Processar dados")
        print("2. Exibir relatório")
        print("3. Sair")
        print("4. Salvar relatório em arquivo")

        opcao = input("Escolha uma opção: ").strip()

        if opcao == "1":
            resultado = processar()
        elif opcao == "2":
            if resultado is None:
                print("Nenhum processamento realizado.")
                continue
            exibir_relatorio(resultado)
        elif opcao == "3":
            break
        elif opcao == "4":
            if resultado is None:
                print("Nenhum processamento realizado.")
                continue
            salvar_relatorio(resultado)


if __name__ == "__main__":
    menu_principal()
