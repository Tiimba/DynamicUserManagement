# DynamicUserManagement

## Usage

```
Backend:

1. python -m pip install -r requirements.txt
2. cd /backend/
3. uvicorn main:app --host 0.0.0.0 --reload
4. Use the Postman Collection to see the results.
```
### Docs
[Backend - server.py](backend/docs/servers.md)

[Backend - main.py](docs/main.md) - TODO

### ChangeLOG
```
0.0.4:
- Added MongoDB Database
- Added Authentication
- Fix Groups exit code and status showing when looking for the users
- UX_COMMANDS Dict remove from Unix Class


0.0.3: 
- Added the `get_user(self, username)` function to retrieve information about a user based on the provided username.
- The function checks if it is connected before executing the user retrieval command. If not connected, it returns a dictionary with a "nok" status and an error message.
- The function executes a system command to obtain information about the user using the provided username.
- The obtained information is returned in a dictionary that includes the username, password, user ID, group ID, comment, home directory, default shell, groups the user belongs to, and user lock state.
- If the user does not exist, a dictionary is returned indicating that no user was found, along with a message stating that the user does not exist.
- The operating system exit code is also returned in the return dictionary.
- Postman Reorganized.

0.0.2: Refatoraçao do servers.py
```
