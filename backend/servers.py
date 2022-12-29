import socket
import paramiko
import random, string


class Unix:
    UX_CMDS = {
        "getos": "uname",
        "getusers": "cat /etc/passwd",
        "getusergroups": "groups",
        "getgroups": "cat /etc/group",
        "createuser": "useradd",
        "unlockuser": "usermod -u"
    }

    def __init__(self, hostname, credentials: dict):
        self.hostname = hostname
        self.sshcon = paramiko.SSHClient()
        self.sshcon.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        self.os = None
        self.connected = False
        self.error_msg = None
        self._connect(credentials=credentials)

    def _connect(self, credentials: dict):
        try:
            if credentials["connection_type"] == "private_key":
                self.sshcon.connect(self.hostname, username=credentials["username"].lower(),
                                    pkey=credentials["ssh_key"], timeout=20)
                print("Conectado com sucesso! Metodo private key")
            elif credentials["connection_type"] == "password":
                self.sshcon.connect(self.hostname, username=credentials["username"].lower(),
                                    password=credentials["password"], timeout=20)
                print("Conectado com sucesso! Metodo password")
            self.connected = True

        except paramiko.ssh_exception.AuthenticationException as error:
            print("Error ao autenticar, usuário sem acesso.")
            print(str(error))
            self.connected = False
        except paramiko.ssh_exception.NoValidConnectionsError as error:
            self.connected = False
            self.error_msg = str(error)
        except socket.gaierror as error:
            print(f"O Servidor {self.hostname} não foi encontrado.\n{str(error)}")
            self.error_msg = str(error)
            self.connected = False
        except Exception as error:
            print(f"Erro inesperado.\n{str(error)}")
            self.error_msg = str(error)
            self.connected = False

    def get_os(self):
        if self.connected:
            try:
                (stdin, stdout, stderr) = self.sshcon.exec_command(self.UX_CMDS["getos"])
                return stdout.readline().strip()
            except paramiko.ssh_exception.SSHException as error:
                print(f"Error.\n{str(error)}")
        else:
            return self.error_msg

    def get_users(self):
        if self.connected:
            (stdin, stdout, stderr) = self.sshcon.exec_command(self.UX_CMDS["getusers"])

            stdout._set_mode("rb")
            lines = stdout.readlines()
            exit_code = stdout.channel.recv_exit_status()

            if exit_code == 0:
                users = []
                for line in lines:
                    user_obj = dict()
                    str_line = line.decode('latin1')
                    user_obj["username"] = str_line.split(':')[0]
                    user_obj["password"] = str_line.split(':')[1]
                    user_obj["uid"] = str_line.split(':')[2]
                    user_obj["gid"] = str_line.split(':')[3]
                    user_obj["comment"] = str_line.split(':')[4]
                    user_obj["homedirectory"] = str_line.split(':')[5]
                    user_obj["shell"] = str_line.split(':')[6]
                    user_obj["groups"] = self.get_groups(user_obj["username"])
                    users.append(user_obj)

                return users
        else:

            return self.error_msg

    def get_groups(self, username=None):
        if self.connected:
            groups = None
            if username:
                (stdin, stdout, stderr) = self.sshcon.exec_command(f"{self.UX_CMDS['getusergroups']} {username}")
                groups = stdout.readline().strip().split(":")[1].strip().split(" ")
            else:
                (stdin, stdout, stderr) = self.sshcon.exec_command(self.UX_CMDS["getgroups"])

                stdout._set_mode("rb")
                lines = stdout.readlines()
                exit_code = stdout.channel.recv_exit_status()

                if exit_code == 0:
                    groups = []
                    for line in lines:
                        group_obj = dict()
                        str_line = line.decode('latin1')
                        group_obj["groupname"] = str_line.split(':')[0]
                        group_obj["password"] = str_line.split(':')[1]
                        group_obj["gid"] = str_line.split(':')[2]

                        group_obj["members"] = str_line.split(':')[3].splitlines()

                        groups.append(group_obj)
            return groups
        else:
            return self.error_msg

    def _generate_password(self):
        password = ''.join(random.choice(string.printable) for i in range(8))
        return password

    def create_user(self, username, password=None, groups=None, create_home: bool = False, shell=None):
        command = f"sudo useradd"
        if create_home:
            command += " -m"
            create_home = "created"
        else:
            create_home = "not created"
        if shell:
            command += f" -s {shell}"
        else:
            shell = "/bin/bash"
        if groups:
            command += f" -G {','.join(groups)}"
            groups = ','.join(groups)

        command += f" {username}"

        (stdin, stdout, stderr) = self.sshcon.exec_command(command)
        exit_code = stdout.channel.recv_exit_status()
        if exit_code == 0:
            if password:
                if password == 'random':
                    password = self._generate_password()

                passwd_command = f"usermod --password $(echo {password} | openssl passwd -1 -stdin) {username}"
                (stdin, stdout, stderr) = self.sshcon.exec_command(passwd_command)

            return_data = {
                "username": username,
                "password": password,
                "groups": groups,
                "home": create_home,
                "shell": shell,
                "status": "Created"
            }
        elif exit_code == 9:
            return_data = {
                "username": username,
                "status": "User already exists"
            }
        else:
            return_data = {
                "username": username,
                "status": "Error on creating"
            }

        return return_data

    def unlock_user(self, user):
        if self.connected:
            print(f"{self.UX_CMDS['unlockuser']} {user}")
            (stdin, stdout, stderr) = self.sshcon.exec_command(f"sudo {self.UX_CMDS['unlockuser']} {user}")
            exit_code = stdout.channel.recv_exit_status()
            print(stderr.readline())
            if exit_code == 0:
                return {
                    "username": user,
                    "status": "Unlocked"
                }
            elif exit_code == 3:
                return {
                    "username": user,
                    "status": "User does not exist"
                }
            else:
                return {
                    "username": user,
                    "status": "Error while unlocking"
                }
        else:
            return self.error_msg

    def kill_connection(self):
        if self.connected:
            if self.sshcon:
                self.sshcon.close()
                print("Sessão foi morta")
            self.connected = False
        else:
            print("Não há sessão aberta")

# if __name__ == '__main__':
#     amigo = Unix(hostname="192.168.0.108",
#                  credentials={"connection_type": "password", "username": "timba", "password": "mudar123",
#                               "ssh_pass": None})
#     print(amigo.create_user("testevazio2"))
# print(amigo.get_users())
