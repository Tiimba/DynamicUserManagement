import socket
import paramiko
import random, string


class Unix:
    UX_CMDS = {
        "getos": "uname",
        "getusers": "cat /etc/passwd",
        "getusergroups": "groups",
        "getgroups": "cat /etc/group",
        "createuser": "useradd"
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

        self.sshcon.exec_command(command)
        print(command)
        if password:
            if password == 'random':
                password = self._generate_password()

            passwd_command = f"usermod --password $(echo {password} | openssl passwd -1 -stdin) {username}"
            self.sshcon.exec_command(passwd_command)

        user_created = {
            "username": username,
            "password": password,
            "groups": groups,
            "home": create_home,
            "shell": shell
        }
        return user_created

    def kill_connection(self):
        if self.connected:
            if self.sshcon:
                self.sshcon.close()
                print("Sessão foi morta")
            self.connected = False
        else:
            print("Não há sessão aberta")
    # TO_DO
    # def unlock_user(self, user):
    #

# if __name__ == '__main__':
#     amigo = Unix(hostname="192.168.0.108",
#                  credentials={"connection_type": "password", "username": "timba", "password": "mudar123",
#                               "ssh_pass": None})
#     print(amigo.create_user("testevazio2"))
    # print(amigo.get_users())
