from database.DB_connect import DBConnect
from model.team import Team

class DAO:
    @staticmethod
    def get_teams(year):
        conn = DBConnect.get_connection()

        result = []

        cursor = conn.cursor(dictionary=True)
        query = """ 
        SELECT s.team_id AS t1, s.team_code AS t2, SUM(s.salary) as salario, t.name
        FROM salary s, team t
        WHERE s.year > %s AND t.id = s.team_id
        GROUP BY s.team_id , s.team_code, t.name
        ORDER BY salario DESC
         """

        cursor.execute(query,(year,))

        for row in cursor:
            result.append(Team(row["t1"], row["t2"], row["salario"], row["name"]))

        cursor.close()
        conn.close()
        return result

    @staticmethod
    def get_all_years():
        conn = DBConnect.get_connection()

        result = []

        cursor = conn.cursor(dictionary=True)
        query = """ 
         SELECT DISTINCT year
        FROM salary  
        WHERE year > 1980
         """

        cursor.execute(query)

        for row in cursor:
            result.append(row["year"])

        cursor.close()
        conn.close()
        return result

    @staticmethod
    def get_connections(teams, year):
        # teams = dizionario {id_team: oggetto_team}
        conn = DBConnect.get_connection()

        result = []

        cursor = conn.cursor(dictionary=True)
        query = """ 
               SELECT  DISTINCT t1.id as team1, t2.id AS team2
               FROM team t1, team t2
               WHERE t1.id > t2.id AND t1.year > 1980 AND t2.year > %s
                 """

        cursor.execute(query,(year,))

        for row in cursor:
            t1 = teams.get(row["team1"])
            t2 = teams.get(row["team2"])
            if t1 is not None and t2 is not None:
                salary1 = t1.salario
                salary2 = t2.salario
                salary = salary1 + salary2

                result.append((t1.id, t2.id, salary))

        cursor.close()
        conn.close()
        return result