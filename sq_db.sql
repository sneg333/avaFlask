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
contact_text text NOT NULL,
adress text NOT NULL,
phone text NOT NULL,
mail text NOT NULL
);

CREATE TABLE IF NOT EXISTS product (
id integer PRIMARY KEY AUTOINCREMENT,
title_product text NOT NULL,
body_product text NOT NULL,
url text NOT NULL
);

CREATE TABLE IF NOT EXISTS adminpanel (
id integer PRIMARY KEY AUTOINCREMENT,
title text NOT NULL,
url text NOT NULL
);
