import unittest
import servers


class Unix_Unit_Test(unittest.TestCase):
    server = servers.Unix(hostname="192.168.0.108",
                          credentials={"connection_type": "password", "username": "timba", "password": "mudar123",
                                       "ssh_pass": None})

    def test_connection(self):
        self.assertEqual(self.server.connected, True)

    def test_os(self):
        self.assertIn(self.server.get_os(), ["AIX", "Windows", "Linux"])

    def test_users(self):
        users = self.server.get_users()
        self.assertEqual(users["status"], "ok")

    def test_groups(self):
        users = self.server.get_groups()
        self.assertEqual(users["status"], "ok")


if __name__ == '__main__':
    unittest.main()
