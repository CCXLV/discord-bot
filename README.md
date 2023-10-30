
## How to set up the bot
1. **Make a bot**

Go [here](https://discord.com/developers/applications) create an application and get the token

2. **Install the requirements**

Install by running `pip install -r requirement.txt`

3. **Create the database in PostgreSQL**

```sql
CREATE DATABASE ccxlv OWNER ccxlv;
```
4. **Configure tables in the database**

Go to `tables.sql` which is located in `sql` folder and run them in the `psql` tool

5. **Setup configuration**

Now create a `config.py` file and fill in like the following template:

```py
token = '' # your bot's token
postgresql = 'postgresql://user:password@host/database' # your postgresql info
```

6. Start the bot by running `launcher.py` file


For questions dm me on discord `CCXLV#2179`
