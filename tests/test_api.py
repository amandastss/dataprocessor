import unittest

from fastapi.testclient import TestClient

from dataprocessor.interfaces.api import app


client = TestClient(app)


class ApiTestCase(unittest.TestCase):
    def test_clientes_devolve_clientes_validos(self):
        resposta = client.get("/clientes")

        self.assertEqual(resposta.status_code, 200)
        self.assertEqual(len(resposta.json()), 2)
        self.assertIn("nome", resposta.json()[0])

    def test_metricas_devolve_resumo(self):
        resposta = client.get("/metricas")

        self.assertEqual(resposta.status_code, 200)
        self.assertEqual(resposta.json()["total_aprovado"], 150.5)
        self.assertEqual(resposta.json()["clientes_validos"], 2)

    def test_transacoes_filtra_por_status_e_cliente(self):
        resposta = client.get("/transacoes", params={"status": "aprovado", "cliente_id": 1})

        self.assertEqual(resposta.status_code, 200)
        self.assertTrue(
            all(
                transacao["status"] == "aprovado" and transacao["cliente_id"] == 1
                for transacao in resposta.json()
            )
        )

    def test_status_invalido_retorna_422(self):
        resposta = client.get("/transacoes", params={"status": "inexistente"})

        self.assertEqual(resposta.status_code, 422)

    def test_formato_invalido_retorna_422(self):
        resposta = client.get("/relatorio/xml")

        self.assertEqual(resposta.status_code, 422)

    def test_relatorio_csv_define_content_type(self):
        resposta = client.get("/relatorio/csv")

        self.assertEqual(resposta.status_code, 200)
        self.assertTrue(resposta.headers["content-type"].startswith("text/csv"))
        self.assertIn("nome", resposta.text)

    def test_post_processar_usa_fonte_em_memoria(self):
        entrada = {
            "clientes": [
                {
                    "id": 1,
                    "nome": "Ana",
                    "email": "ana@email.com",
                    "idade": 30,
                    "cidade": "Joinville",
                    "data_cadastro": "2023-01-10",
                }
            ],
            "transacoes": [
                {
                    "id": 1,
                    "cliente_id": 1,
                    "valor": 10.5,
                    "categoria": "livros",
                    "data": "2023-05-10",
                    "status": "aprovado",
                }
            ],
            "config": {
                "categorias_validas": ["livros"],
                "status_validos": ["aprovado", "pendente", "recusado"],
            },
        }

        resposta = client.post("/processar", json=entrada)

        self.assertEqual(resposta.status_code, 200)
        self.assertEqual(resposta.json()["total_aprovado"], 10.5)
        self.assertEqual(resposta.json()["transacoes_validas"], 1)

    def test_post_processar_rejeita_tipo_incorreto(self):
        entrada = {
            "clientes": [{"id": 1, "nome": "Ana", "idade": "trinta"}],
            "transacoes": [],
            "config": {"categorias_validas": [], "status_validos": []},
        }

        resposta = client.post("/processar", json=entrada)

        self.assertEqual(resposta.status_code, 422)


if __name__ == "__main__":
    unittest.main()
