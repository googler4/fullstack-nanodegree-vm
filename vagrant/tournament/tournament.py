#!/usr/bin/env python
#
# tournament.py -- implementation of a Swiss-system tournament
#

import psycopg2
import time

_Current_Tournament = 0


def connect():
    """Connect to the PostgreSQL database.  Returns a database connection."""
    try:
        connection = psycopg2.connect("dbname=tournament")
        return connection
    except:
        print "Unable to connect"

# PSYCOGP2 - query and data, also excutemany if needed


def execute_psqls(query, data):
    conn = None

    try:
        # print "commit"
        conn = connect()
        cursor = conn.cursor()

        cursor.execute(query, data)
        conn.commit()
        # print "INSERT ONE"

    except psycopg2.DatabaseError, e:
        if conn:
            conn.rollback()
        print '+Error+ %s' % e
        # sys.exit(1)

    finally:
        if conn:
            conn.close()

# PSYCOGP2 - query and data, also excutemany if needed


def execute_psqls_return(query, data):
    conn = None
    output = None
    try:
        # print "commit"
        conn = connect()
        cursor = conn.cursor()

        cursor.execute(query, data)
        output = cursor.fetchall()

        conn.commit()
        # print "INSERT ONE"

    except psycopg2.DatabaseError, e:
        if conn:
            conn.rollback()
        print '+Error+ %s' % e
        # sys.exit(1)

    finally:
        if conn:
            conn.close()
        return output

# PSYCOGP2 - query with error output


def execute_psql(query):
    conn = None

    try:
        conn = connect()
        cursor = conn.cursor()
        cursor.execute(query)

        conn.commit()

    except psycopg2.DatabaseError, e:
        if conn:
            conn.rollback()
        print 'Error %s' % e

        # sys.exit(1)

    finally:
        if conn:
            conn.close()

# PSYCOGP2 - query, with single variable return


def execute_psql_return(query, *data):
    conn = None
    output = None

    if not data:
        data = ''
    else:
        data = data[0]

    try:
        conn = connect()
        cursor = conn.cursor()
        cursor.execute(query, data)

        output = cursor.fetchall()
        print output

        conn.commit()

        return output[0][0]

    except psycopg2.DatabaseError, e:
        if conn:
            conn.rollback()
        print '++Error++ %s' % e

        # sys.exit(1)

    finally:
        if conn:
            conn.close()
        # return output
        # print "uploaded"

# Start Tournament, create DB entry


def startTournament():
    # build query
    query = "INSERT INTO tournaments(time) VALUES (now()) RETURNING id"

    # execute query, return Tournament ID (#)
    _Current_Tournament = execute_psql_return(query)

# Change or update tournament


def selectTournament(selected_Tourn):
    data = ([selected_Tourn])
    query = "SELECT COALESCE ((SELECT COUNT(*) as c FROM tournament WHERE id = %s), 0)"
    validTourn = execute_psqls_return(query, data)

    if(validTourn == 1):
        _Current_Tournament = selected_Tourn
        print "Tournament: " + _Current_Tournament + " Selected"
    else:
        # build query
        query = "INSERT INTO tournaments(time) VALUES (now()) RETURNING id"

        # execute query
        _Current_Tournament = execute_psql_return(query)


def deleteMatches():
    """Remove all the match records from the database."""

    query = "DELETE FROM matches"
    execute_psql(query)


def deletePlayers():
    """Remove all the player records from the database."""

    query = "DELETE FROM players"
    execute_psql(query)


def countPlayers():
    """Returns the number of players currently registered."""

    query = "SELECT COALESCE ((SELECT COUNT(*) as c FROM players), 0)"

    return execute_psql_return(query)


def registerPlayer(name):
    """Adds a player to the tournament database.

    The database assigns a unique serial id number for the player.  (This
    should be handled by your SQL database schema, not in your Python code.)

    Args:
      name: the player's full name (need not be unique).
    """
    data = ([name])
    # build query
    query = "INSERT INTO players(name, time) VALUES (%s, now())"

    # execute query
    execute_psqls(query, data)


def playerStandings():
    """Returns a list of the players and their win records, sorted by wins.

    The first entry in the list should be the player in first place, or a player
    tied for first place if there is currently a tie.

    Returns:
      A list of tuples, each of which contains (id, name, wins, matches):
        id: the player's unique id (assigned by the database)
        name: the player's full name (as registered)
        wins: the number of matches the player has won
        matches: the number of matches the player has player
    """

    conn = None
    try:
        # print "commit"
        conn = connect()
        cursor = conn.cursor()

        query = ("SELECT id, name, (SELECT COUNT(*) FROM matches WHERE winner = p.id) "
                 "AS wins, (SELECT COUNT(*) FROM matches WHERE winner = p.id OR loser = p.id) "
                 "FROM players p ORDER BY wins desc, name")
        #query = "SELECT id, name, wins, wins+loses FROM players ORDER BY wins, name"
        # query = "SELECT winner, (SELECT name FROM players WHERE id = matches.winner), count(*) FROM matches GROUP BY winner"

        cursor.execute(query)
        rows = cursor.fetchall()
        print rows
        # for row in rows:
        #     print row

    except psycopg2.DatabaseError, e:
        if conn:
            conn.rollback()
        print 'Error %s' % e
        # sys.exit(1)

    finally:
        if conn:
            conn.close()

        return rows

# This function is created to avoid changes to the reportMatch function


def reportTieMatch(player1, player2):
    """Records the outcome of a ties between two players.

    Args:
      winner:  the id number of the player who won
      loser:  the id number of the player who lost
    """
    data = ([player1])
    query = "SELECT name FROM players WHERE id = %s"
    player1_name = execute_psql_return(query, data)

    data = ([player2])
    query = "SELECT name FROM players WHERE id = %s"
    player2_name = execute_psql_return(query, player2)

    title = player1_name + " tied " + player2_name

    data = ([title, [winner, loser], [loser, winner], _Current_Tournament])
    # print len(data)

    query = ("INSERT INTO matches (title, ties, player_ids, tourn_id, time) "
             "VALUES (%s, %s, %s, %s, %s, now())")
    # print query

    execute_psqls(query, data)


def reportMatch(winner, loser):
    """Records the outcome of a single match between two players.

    Args:
      winner:  the id number of the player who won
      loser:  the id number of the player who lost
    """
    data = ([winner])
    query = "SELECT name FROM players WHERE id = %s"
    winner_name = execute_psql_return(query, data)

    data = ([loser])
    query = "SELECT name FROM players WHERE id = %s"
    loser_name = execute_psql_return(query, data)

    title = winner_name + " vs " + loser_name

    data = ([title, winner, loser, [loser, winner], _Current_Tournament])
    # print len(data)

    query = ("INSERT INTO matches "
             "(title, winner, loser, player_ids, tourn_id, time) "
             "VALUES (%s, %s, %s, %s, %s, now())")
    # print query

    execute_psqls(query, data)


def replay(player1, player2):
    data = ([player1, player2, player2, player1])
    query = ("SELECT COALESCE ("
             "(SELECT COUNT(*) FROM matches "
             "WHERE (winner = %s AND loser = %S) OR (winner = %s AND loser = %S)), 0)")
    rematch = execute_psqls_return(query, data)
    print rematch

    if(rematch != 0):
        return True
    else:
        return False


def reportPrePairings():
    """Returns a list of pairs of players for the next round of a match.

        Query winners and loser count, then list by wins. This is faster as a 
        SQL query. Then Pair for pre-pairing.
    """
    conn = None
    try:
        # print "commit"
        conn = connect()
        cursor = conn.cursor()

        query = ("SELECT id, name, "
                 "(SELECT COUNT(*) FROM matches WHERE winner = p.id) AS wins, "
                 "(SELECT COUNT(*) FROM matches WHERE winner = p.id OR loser = p.id), "
                 "(SELECT COUNT(*) FROM matches WHERE p.id = ANY(ties))"
                 "FROM players p ORDER BY wins desc, name")

        cursor.execute(query)
        rows = cursor.fetchall()
        print rows
        # for row in rows:
        #     print row

    except psycopg2.DatabaseError, e:
        if conn:
            conn.rollback()
        print 'Error %s' % e
        # sys.exit(1)

    finally:
        if conn:
            conn.close()

        return rows

    execute_psql_reutrn


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

    # First locate all scores including
    reportPP = reportPrePairings()

    nextRound = []


# Select the highest player, start working down the list looking for a match

    for i in range(0, len(reportPP), 2):
        print "i = " + str(i)

        for ii in range(i + 1, len(reportPP)):
            player1 = reportPP[i][0]
            # print player1
            player2 = reportPP[ii][0]
            print str(player1) + " vs " + str(player2)

            # If there is a rematch we will interate until we find a worth match
            # Once that is done we will spawn the positions of the match,
            # Jump i by 2 and continue pairing.

            # feels oddly similar to bubble sort

            if(replay(player1, player2)):
                print "match found"

                while ii > i + 1:
                    # swap until paired
                    reportPP[
                        ii - 1], reportPP[ii] = reportPP[ii], reportPP[ii - 1]
                    ii -= 1
                # break loop
                break

        nextRound.append((reportPP[i][0], reportPP[i][1], reportPP[
                         i + 1][0], reportPP[i + 1][1]))
        # i = i+1

    print nextRound
    return nextRound
