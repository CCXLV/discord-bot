
## How to set up the bot
1. **Make a bot**

Go [here](https://discord.com/developers/applications) create an application and get the token

2. **Install the requirements**

Install by running `pip install -r requirement.txt`

3. **Create the database in PostgreSQL**

Note

4. **Setup configuration**

Now locate to `config.py` file and fill in like the following template:

```py
token = '' # your bot's token
postgresql = 'postgresql://user:password@host/database' # your postgresql info
```

5. Start the bot by running `launcher.py` file

