CREATE DATABASE email_sender;

\c email_sender

CREATE TABLE emails (
    id serial NOT NULL,
    data timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
    assunto varchar(100) NOT NULL,
    mensagem varchar(250) NOT NULL
);