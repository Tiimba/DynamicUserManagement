import unittest
import paramiko
from servers import Unix


class TestUnixClass(unittest.TestCase):
    # MockVars
    credentials = {"username": "timba", "password": "mudar123", "connection_type": "password"}
    hostname = "192.168.0.116"

    def test_init(self):
        # Testa se o objeto Unix é iniciado corretamente

        unix = Unix(self.hostname, self.credentials)
        self.assertEqual(unix.hostname, self.hostname)
        self.assertIsInstance(unix.sshcon, paramiko.SSHClient)

    def test_connect_success(self):
        # Testa se a conexão é bem-sucedida
        unix = Unix(self.hostname, self.credentials)
        self.assertTrue(unix.connected)

    def test_connect_failure(self):
        # Testa se a conexão falha
        hostname = "invalid_hostname"
        unix = Unix(hostname, self.credentials)
        self.assertFalse(unix.connected)
        self.assertIsNotNone(unix.error_msg)

    def test_get_os(self):
        # Testa se o método get_os retorna o sistema operacional correto
        unix = Unix(self.hostname, self.credentials)
        result = unix.get_os()
        self.assertEqual(result["status"], "ok")

    def test_get_users(self):
        # Testa se o método get_users retorna a lista de usuários correta
        unix = Unix(self.hostname, self.credentials)
        result = unix.get_users()
        self.assertIn("status", result)
        self.assertEqual(result["status"], "ok")
        self.assertIn("users", result)
        self.assertIsInstance(result["users"], list)

    def test_get_groups(self):
        # Testa se o método get_groups retorna a lista de grupos correta
        unix = Unix(self.hostname, self.credentials)
        result = unix.get_groups()
        self.assertIn("status", result)
        self.assertEqual(result["status"], "ok")
        self.assertIn("groups", result)
        self.assertIsInstance(result["groups"], list)
