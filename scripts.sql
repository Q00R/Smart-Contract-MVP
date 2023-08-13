CREATE SCHEMA IF NOT EXISTS valify_internship;

CREATE TABLE IF NOT EXISTS valify_internship.users(
user_id SERIAL NOT NULL,
email TEXT NOT NULL,
password TEXT NOT NULL,
username TEXT,
nid TEXT,
phone_number TEXT,
CONSTRAINT users_pkey PRIMARY KEY(user_id)
);

CREATE TABLE IF NOT EXISTS valify_internship.documents (
document_id SERIAL,
document_hash TEXT NOT NULL,
user_id INTEGER NOT NULL,
timestamp TIMESTAMP NOT NULL,
is_completed BOOLEAN NOT NULL,
CONSTRAINT documents_pkey PRIMARY KEY(document_id, user_id),
FOREIGN KEY(user_id) REFERENCES valify_internship.Users
);

CREATE TABLE IF NOT EXISTS valify_internship.documents_shared (
doc_id INTEGER NOT NULL,
owner_id INTEGER NOT NULL,
parties_id INTEGER,
PRIMARY KEY (doc_id, owner_id),
FOREIGN KEY (doc_id, owner_id) REFERENCES valify_internship.Documents(document_id, user_id) ON DELETE CASCADE,
FOREIGN KEY (parties_id) REFERENCES valify_internship.Users(user_id) ON DELETE CASCADE
);