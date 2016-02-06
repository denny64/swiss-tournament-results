-- Table definitions for the tournament project.
--
-- Put your SQL 'create table' statements in this file; also 'create view'
-- statements if you choose to use it.
--
-- You can write comments in this file by starting them with two dashes, like
-- these lines here.

-- Drop the database if it already exists - otherwise create and connect to the database
DROP DATABASE IF EXISTS tournament;
CREATE DATABASE tournament;
\c tournament;

CREATE TABLE players (
	id SERIAL PRIMARY KEY,
	name TEXT,
  wins INTEGER,
  total_matches INTEGER
);

CREATE TABLE matches (
  id SERIAL PRIMARY KEY,
  winner INTEGER REFERENCES players(id),
  loser INTEGER REFERENCES players(id)
);

-- Create standings view
CREATE VIEW standings AS
SELECT players.id, players.name, players.wins, players.total_matches
FROM players;
