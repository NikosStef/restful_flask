DROP TABLE users;
DROP TABLE notes;

CREATE TABLE users(
  username TEXT NOT NULL,
  password TEXT NOT NULL,
  email TEXT NOT NULL UNIQUE PRIMARY KEY
);

CREATE TABLE notes (
  context TEXT NOT NULL,
  archived INTEGER NOT NULL,
  ownerEmail TEXT NOT NULL,
  FOREIGN KEY(ownerEmail) REFERENCES users(email)
);

INSERT INTO users(username, password, email) VALUES('admin', 'admin', 'admin@gmail.com');
INSERT INTO users(username, password, email) VALUES('user', 'xrhsths', 'webappuom@gmail.com');
INSERT INTO users(username, password, email) VALUES('root', 'root', 'nikstef024@gmail.com');

INSERT INTO notes(context, archived, ownerEmail)
VALUES('MyNote0', 0, (SELECT email FROM Users WHERE username = 'user'));
INSERT INTO notes(context, archived, ownerEmail)
VALUES('MyNote1', 1, (SELECT email FROM Users WHERE username = 'root'));
INSERT INTO notes(context, archived, ownerEmail)
VALUES('MyNote0', 0, (SELECT email FROM Users WHERE username = 'admin'));
INSERT INTO notes(context, archived, ownerEmail)
VALUES('MyNote0', 1, (SELECT email FROM Users WHERE username = 'user'));
