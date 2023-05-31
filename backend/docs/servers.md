# Unix Class

The `Unix` class provides functionality to interact with a remote Unix system using SSH and Paramiko. It allows performing various operations such as getting the OS information, retrieving user and group details, creating users, locking and unlocking users, deleting users, and checking user lock states.

## Constructor

### \_\_init__(self, hostname, credentials: dict)

- Initializes a new instance of the `Unix` class.
- Parameters:
  - `hostname` (string): Hostname or IP address of the remote Unix system.
  - `credentials` (dict): Dictionary containing the connection credentials, including the username, password or SSH key path, and connection type ("password" or "private_key").

## Methods

### get_os(self)

- Retrieves the operating system information of the remote Unix system.
- Returns:
  - A dictionary with the following keys:
    - `status` (string): Status of the operation ("ok" or "nok").
    - `os` (string): Operating system information.

### get_users(self)

- Retrieves the list of users on the remote Unix system.
- Returns:
  - A dictionary with the following keys:
    - `users` (list): List of dictionaries, each containing information about a user.
      - `username` (string): Username of the user.
      - `password` (string): Encrypted password of the user.
      - `uid` (string): User ID.
      - `gid` (string): Group ID of the user.
      - `comment` (string): Additional comments or description of the user.
      - `homedirectory` (string): Home directory path of the user.
      - `shell` (string): Login shell of the user.
      - `groups` (list): List of group names to which the user belongs.
      - `locked` (string): Lock state of the user ("Unlocked" or "Locked").
    - `status` (string): Status of the operation ("ok" or "nok").
    - `os_exit_code` (int): Exit code of the command execution.

### get_groups(self, username=None)

- Retrieves the list of groups on the remote Unix system.
- Parameters:
  - `username` (string, optional): If provided, retrieves the groups of the specified user.
- Returns:
  - A dictionary with the following keys:
    - If `username` is provided:
      - `groups` (list): List of group names to which the user belongs.
      - `status` (string): Status of the operation ("ok" or "nok").
      - `os_exit_code` (int): Exit code of the command execution.
    - If `username` is not provided:
      - `groups` (list): List of dictionaries, each containing information about a group.
        - `groupname` (string): Name of the group.
        - `password` (string): Password (usually 'x') associated with the group.
        - `gid` (string): Group ID.
        - `members` (list): List of usernames of the group members.
      - `status` (string): Status of the operation ("ok" or "nok").
      - `os_exit_code` (int): Exit code of the command execution.

### create_user(self, username, password=None, comments=None, groups=None, create_home: bool = False, shell=None)

- Creates a new user on the remote Unix system.
- Parameters:
  - `username` (string): Username for the new user.
  - `password` (string, optional): Password for the new user. If not provided, a random password will be generated.
  - `comments` (string, optional): Additional comments or description for the new user.
  - `groups` (list, optional): List of group names to which the new user should belong.
  - `create_home` (bool, optional): Specifies whether to create a home directory for the new user.
  - `shell` (string, optional): Login shell for the new user. If not provided, '/bin/bash' will be used.
- Returns:
  - A dictionary with the following keys:
    - `username` (string): Username of the created user.
    - `password` (string): Password of the created user (randomly generated if not provided).
    - `comments` (string): Additional comments or description of the created user.
    - `groups` (list): List of group names to which the created user belongs.
    - `home` (bool): Indicates whether a home directory was created for the user.
    - `shell` (string): Login shell of the created user.
    - `status` (string): Status of the operation ("Created", "User already exists", or "Error on creating").
    - `password_status` (string, optional): Status of setting the password for the user ("password set" or "password was not set").
    - `os_exit_code` (int): Exit code of the command execution.

### unlock_user(self, user)

- Unlocks a user on the remote Unix system.
- Parameters:
  - `user` (string): Username of the user to unlock.
- Returns:
  - A dictionary with the following keys:
    - `username` (string): Username of the unlocked user.
    - `status` (string): Status of the operation ("Unlocked", "User does not exist", or "Error while unlocking").
    - `os_exit_code` (int): Exit code of the command execution.

### lock_user(self, user)

- Locks a user on the remote Unix system.
- Parameters:
  - `user` (string): Username of the user to lock.
- Returns:
  - A dictionary with the following keys:
    - `username` (string): Username of the locked user.
    - `status` (string): Status of the operation ("Locked", "User does not exist", or "Error while locking").
    - `os_exit_code` (int): Exit code of the command execution.

### delete_user(self, user)

- Deletes a user from the remote Unix system.
- Parameters:
  - `user` (string): Username of the user to delete.
- Returns:
  - A dictionary with the following keys:
    - `username` (string): Username of the deleted user.
    - `status` (string): Status of the operation ("deleted", "User does not exist", or an error message).
    - `os_exit_code` (int): Exit code of the command execution.

### kill_connection(self)

- Closes the SSH connection to the remote Unix system.
- Prints a message indicating the session has been closed.

### get_user_lock_state(self, username)

- Retrieves the lock state of a user on the remote Unix system.
- Parameters:
  - `username` (string): Username of the user.
- Returns:
  - The lock state of the user ('Unlocked', 'Locked', or 'Status Not Mapped').

---

Please note that the provided documentation is generated based on the code analysis and may not fully reflect the functionality or behavior of the actual implementation. It is recommended to review the code for more precise details and consult additional resources as needed.
