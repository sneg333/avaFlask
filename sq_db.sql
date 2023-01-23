CREATE TABLE IF NOT EXISTS mainmenu (
id integer PRIMARY KEY AUTOINCREMENT,
title text NOT NULL,
url text NOT NULL
);

CREATE TABLE IF NOT EXISTS news (
id integer PRIMARY KEY AUTOINCREMENT,
title text NOT NULL,
full_text text NOT NULL
);

CREATE TABLE IF NOT EXISTS contact (
id integer PRIMARY KEY AUTOINCREMENT,
contact_text text NOT NULL
)