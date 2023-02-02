# Make sure do to all this before you run the bot.

CREATE TABLE IF NOT EXISTS tags (
  guild_id BIGINT PRIMARY KEY,
  name TEXT,
  content TEXT
);

CREATE TABLE IF NOT EXISTS modlog (
  guild_id BIGINT PRIMARY KEY,
  channel_id BIGINT
);

CREATE TABLE IF NOT EXISTS welcoming (
  guild_id BIGINT PRIMARY KEY,
  channel_id BIGINT
);
