import unittest

from dataprocessor.interfaces.menu import processar_caminhos


class ProcessarCaminhosTestCase(unittest.TestCase):
    def test_processa_dataset_padrao(self):
        resultado = processar_caminhos(
            "data/clientes.csv",
            "data/transacoes.csv",
            "data/config.json",
        )
        self.assertEqual(resultado.total_aprovado, 150.50)


if __name__ == "__main__":
    unittest.main()
