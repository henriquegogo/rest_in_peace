CREATE TABLE users (
  id    INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
  name  TEXT
);

INSERT INTO users (name) VALUES
  ('Henrique'),
  ('Daiane'),
  ('Leticia'),
  ('Pedro Lucas'),
  ('Mateus');
