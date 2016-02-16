-- Table definitions for the tournament project.
--
-- Put your SQL 'create table' statements in this file; also 'create view'
-- statements if you choose to use it.
--
-- You can write comments in this file by starting them with two dashes, like
-- these lines here.
DROP TABLE IF EXISTS players;
CREATE TABLE players ( name TEXT,
                     tourn_ids integer[],
                     time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                     id SERIAL );

DROP TABLE IF EXISTS matches;
CREATE TABLE matches ( title TEXT,
                     player_ids integer[],
                     tourn_id integer,
                     winner integer,
                     loser integer,
                     ties integer [],
                     time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                     id SERIAL );

DROP TABLE IF EXISTS tournaments;
CREATE TABLE tournaments (
                     tourn_name TEXT,
                     tourn_live BOOLEAN,
                     time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                     id SERIAL );

DROP TABLE IF EXISTS leaderboards;
CREATE TABLE leaderboards ( player_name TEXT,
                     tourn_id integer,
                     player_id integer,
                     score integer,
                     time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                     id SERIAL );