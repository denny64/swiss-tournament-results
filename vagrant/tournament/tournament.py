#!/usr/bin/env python
#
# tournament.py -- implementation of a Swiss-system tournament
#

import psycopg2


def connect():
    """Connect to the PostgreSQL database.  Returns a database connection."""
    return psycopg2.connect("dbname=tournament")

def simpleConnection(query, *arg):
    """
    Establishes a simple connection, execution and commits to the database.
    Accepts multiple arguments and is also protected against SQL injection attacks.
    """
    db = connect()
    c = db.cursor()
    c.execute(query, arg)
    db.commit()
    db.close()

def returnConnection(query):
    """
    Establishes a simple connection, executes a query to the database
    and returns the results. No commit is made the the database.
    """
    db = connect()
    c = db.cursor()
    c.execute(query)
    result = c.fetchall()
    db.close()
    return result

def deleteMatches():
    """Remove all the match records from the database."""
    query = """TRUNCATE matches CASCADE;
    UPDATE players SET total_matches = 0, wins = 0;
    """
    simpleConnection(query)

def deletePlayers():
    """Remove all the player records from the database."""
    query = "TRUNCATE players CASCADE;"
    simpleConnection(query)

def countPlayers():
    """Returns the number of players currently registered."""
    query = "SELECT COUNT(*) From players;"
    count = returnConnection(query)
    return count[0][0]

def registerPlayer(name):
    """Adds a player to the tournament database.

    The database assigns a unique serial id number for the player.  (This
    should be handled by your SQL database schema, not in your Python code.)

    Args:
      name: the player's full name (need not be unique).
    """
    query = "INSERT INTO players VALUES (default, (%s), 0, 0);"
    simpleConnection(query, (name,))

def playerStandings():
    """Returns a list of the players and their win records, sorted by wins.

    The first entry in the list should be the player in first place, or a player
    tied for first place if there is currently a tie.

    Returns:
      A list of tuples, each of which contains (id, name, wins, matches):
        id: the player's unique id (assigned by the database)
        name: the player's full name (as registered)
        wins: the number of matches the player has won
        matches: the number of matches the player has played
    """
    query = "select * from standings;"
    return returnConnection(query)


def reportMatch(winner, loser):
    """Records the outcome of a single match between two players.

    Args:
      winner:  the id number of the player who wons
      loser:  the id number of the player who lost
    """
    query = """UPDATE players
               SET total_matches = total_matches + 1, wins = wins + 1
               WHERE id = (%s);
            """
    query2 = """UPDATE players
                SET total_matches = total_matches + 1
                WHERE id = (%s);
            """
    simpleConnection(query, (winner,))
    simpleConnection(query2, (loser,))

def swissPairings():
    """Returns a list of pairs of players for the next round of a match.

    Assuming that there are an even number of players registered, each player
    appears exactly once in the pairings.  Each player is paired with another
    player with an equal or nearly-equal win record, that is, a player adjacent
    to him or her in the standings.

    Returns:
      A list of tuples, each of which contains (id1, name1, id2, name2)
        id1: the first player's unique id
        name1: the first player's name
        id2: the second player's unique id
        name2: the second player's name
    """
    query = "SELECT id, name from standings ORDER BY wins DESC;"
    standings = returnConnection(query)

    pairs = []
    total_players = len(standings)
    for i in range(0, total_players, 2):
        pairs.append(standings[i] + standings[i+1])
    return pairs
