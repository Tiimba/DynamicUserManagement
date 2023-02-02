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
        "unlockuser": "passwd -u",
        "lockuser": "passwd -L",
        "deleteuser": "userdel"
    }

    def __init__(self, hostname, credentials: dict):
        self.hostname = hostname
        self.sshcon = paramiko.SSHClient()
        self.sshcon.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        self.os = None
        self.error_msg = None
        self.connected = self._connect(credentials=credentials)

    def _connect(self, credentials: dict):
        try:
            if credentials["connection_type"] == "private_key":
                connect_method = paramiko.RSAKey.from_private_key_file(credentials["ssh_key"])
            elif credentials["connection_type"] == "password":
                connect_method = credentials["password"]

            self.sshcon.connect(self.hostname, username=credentials["username"].lower(),
                                password=connect_method, timeout=20)
            print("Conectado com sucesso!")
            return True

        except paramiko.ssh_exception.AuthenticationException as error:
            print("Error ao autenticar, usuário sem acesso.")
            self.error_msg = f"Error ao autenticar, usuário sem acesso. {str(error)}"
            return False
        except paramiko.ssh_exception.NoValidConnectionsError as error:
            self.error_msg = str(error)
            return False
        except socket.gaierror as error:
            print(f"O Servidor {self.hostname} não foi encontrado.\n{str(error)}")
            self.error_msg = f"O Servidor {self.hostname} não foi encontrado.\n{str(error)}"
            return False
        except Exception as error:
            print(f"Erro inesperado.\n{str(error)}")
            self.error_msg = str(error)
            return False

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
        if not self.connected:
            return {
                "status": "nok",
                "message": self.error_msg
            }

        (stdin, stdout, stderr) = self.sshcon.exec_command(self.UX_CMDS["getusers"])
        stdout._set_mode("rb")
        lines = stdout.readlines()
        exit_code = stdout.channel.recv_exit_status()

        users = []
        for line in lines:
            user_obj = {}
            str_line = line.decode('latin1')
            user_obj["username"], user_obj["password"], user_obj["uid"], user_obj["gid"], user_obj["comment"], user_obj[
                "homedirectory"], user_obj["shell"] = str_line.split(':')
            user_obj["groups"] = self.get_groups(user_obj["username"])
            users.append(user_obj)

        return {"users": users, "status": "ok" if exit_code == 0 else "nok", "os_exit_code": exit_code}

    def get_groups(self, username=None):
        if self.connected:
            if username:
                (stdin, stdout, stderr) = self.sshcon.exec_command(f"{self.UX_CMDS['getusergroups']} {username}")
                exit_code = stdout.channel.recv_exit_status()
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
                    return {
                        "groups": groups,
                        "status": "ok",
                        "os_exit_code": exit_code
                    }
                else:
                    return {
                        "status": "no",
                        "os_exit_code": exit_code
                    }
        else:
            return {
                "status": "nok",
                "message": self.error_msg
            }

    def _generate_password(self):
        password = ''.join(random.choice(string.printable) for i in range(8))
        return password

    def create_user(self, username, password=None, comments=None, groups=None, create_home: bool = False, shell=None):
        command = f"sudo useradd"
        if comments:
            command += f' -c "{comments}"'
        command += " -m" if create_home else ""
        shell = shell if shell else "/bin/bash"
        command += f" -s {shell}"
        if groups:
            command += f" -G {','.join(groups)}"
            groups = ','.join(groups)

        command += f" {username}"

        (stdin, stdout, stderr) = self.sshcon.exec_command(command)
        exit_code = stdout.channel.recv_exit_status()
        status_dict = {
            0: "Created",
            9: "User already exists",
            None: "Error on creating"
        }

        status = status_dict.get(exit_code, "Error on creating")
        password_status = None
        if exit_code == 0 and password:
            if password == 'random':
                password = self._generate_password()

            passwd_command = f'echo -e "{password}\n{password}" | sudo passwd {username}'
            (stdin, stdout, stderr) = self.sshcon.exec_command(passwd_command)
            password_exit_code = stdout.channel.recv_exit_status()

            password_status_dict = {
                0: "password set",
                None: "password was not set"
            }

            password_status = password_status_dict.get(password_exit_code, "password was not set")

        return {
            "username": username,
            "password": password,
            "comments": comments,
            "groups": groups,
            "home": create_home,
            "shell": shell,
            "status": status,
            "password_status": password_status,
            "os_exit_code": exit_code
        }

    def unlock_user(self, user):
        if self.connected:
            (stdin, stdout, stderr) = self.sshcon.exec_command(f"sudo {self.UX_CMDS['unlockuser']} {user}")
            exit_code = stdout.channel.recv_exit_status()
            if exit_code == 0:
                return {
                    "username": user,
                    "status": "Unlocked",
                    "os_exit_code": exit_code
                }
            elif exit_code == 1:
                return {
                    "username": user,
                    "status": "User does not exist",
                    "os_exit_code": exit_code
                }
            else:
                return {
                    "username": user,
                    "status": "Error while unlocking",
                    "os_exit_code": exit_code
                }
        else:
            return self.error_msg

    def lock_user(self, user):
        if self.connected:
            (stdin, stdout, stderr) = self.sshcon.exec_command(f"sudo {self.UX_CMDS['unlockuser']} {user}")
            exit_code = stdout.channel.recv_exit_status()
            if exit_code == 0:
                return {
                    "username": user,
                    "status": "Locked",
                    "os_exit_code": exit_code
                }
            elif exit_code == 1:
                return {
                    "username": user,
                    "status": "User does not exist",
                    "os_exit_code": exit_code
                }
            else:
                return {
                    "username": user,
                    "status": "Error while locking",
                    "os_exit_code": exit_code
                }
        else:
            return self.error_msg

    def delete_user(self, user):
        if self.connected:
            (stdin, stdout, stderr) = self.sshcon.exec_command(f"sudo {self.UX_CMDS['deleteuser']} {user}")
            exit_code = stdout.channel.recv_exit_status()

            if exit_code == 0:
                return {
                    "username": user,
                    "status": "deleted",
                    "os_exit_code": exit_code
                }

            elif exit_code == 6:
                return {
                    "username": user,
                    "status": "User does not exist",
                    "os_exit_code": exit_code
                }
            else:
                return {
                    "username": user,
                    "status": f"Error on delete user.\n{stderr.readline()}",
                    "os_exit_code": exit_code
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
