from database.DB_connect import DBConnect
from model.airport import Airport
from model.tratta import Tratta


class DAO():

    @staticmethod
    def getAllNodes(n, idMap):
        conn = DBConnect.get_connection()

        result = []

        # Il numero di voli per i nodi lo prendo da flights

        cursor = conn.cursor(dictionary=True)
        query = """select t.ID, t.iata_code, count(*) as N
                    from (select a.ID , a.IATA_CODE , f.AIRLINE_ID, count(*) as N
                    from airports a , flights f 
                    where a.ID = f.ORIGIN_AIRPORT_ID 
                    or a.ID  = f.DESTINATION_AIRPORT_ID
                    group by a.ID , a.IATA_CODE , f.AIRLINE_ID) t
                    group by t.ID, t.iata_code
                    having  N >= %s
                    order by N asc"""

        cursor.execute(query, (n,))

        for row in cursor:
            result.append(idMap[row["ID"]])

        cursor.close()
        conn.close()
        return result

    @staticmethod
    def getAllAirports():
        conn = DBConnect.get_connection()

        result = []

        cursor = conn.cursor(dictionary=True)
        query = """SELECT * \
                   from airports a \
                   order by a.AIRPORT asc"""

        cursor.execute(query)

        for row in cursor:
            result.append(Airport(**row))

        cursor.close()
        conn.close()
        return result

    @staticmethod
    def getAllEdgesV1(idMap):
        conn = DBConnect.get_connection()

        result = []

        cursor = conn.cursor(dictionary=True)
        query = """select f.ORIGIN_AIRPORT_ID , f.DESTINATION_AIRPORT_ID , count(*) as peso
                    from flights f
                    group by f.ORIGIN_AIRPORT_ID, f.DESTINATION_AIRPORT_ID 
                    order by f.ORIGIN_AIRPORT_ID, f.DESTINATION_AIRPORT_ID"""

        cursor.execute(query)

        for row in cursor:
            # result.append((idMap[row["ORIGIN_AIRPORT_ID"]], idMap[row["DESTINATION_AIRPORT_ID"]], row["peso"]))

            result.append(Tratta(idMap[row["ORIGIN_AIRPORT_ID"]], idMap[row["DESTINATION_AIRPORT_ID"]], row["peso"]))

        cursor.close()
        conn.close()
        return result

    @staticmethod
    def getAllEdgesV2(idMap):
        conn = DBConnect.get_connection()

        result = []

        cursor = conn.cursor(dictionary=True)
        query = """select t1.origin_airport_id as A1, t1.destination_airport_id as A2, COALESCE(t1.n,0) + COALESCE(t2.n,0) as peso
                    from (select f.ORIGIN_AIRPORT_ID , f.DESTINATION_AIRPORT_ID , count(*) as n
                    from flights f
                    group by f.ORIGIN_AIRPORT_ID, f.DESTINATION_AIRPORT_ID 
                    order by f.ORIGIN_AIRPORT_ID, f.DESTINATION_AIRPORT_ID) t1
                    left join (select f.ORIGIN_AIRPORT_ID , f.DESTINATION_AIRPORT_ID , count(*) as n
                    from flights f
                    group by f.ORIGIN_AIRPORT_ID, f.DESTINATION_AIRPORT_ID 
                    order by f.ORIGIN_AIRPORT_ID, f.DESTINATION_AIRPORT_ID) t2
                    on t1.origin_airport_id = t2.destination_airport_id and t1.destination_airport_id = t2.origin_airport_id 
                    where t1.origin_airport_id < t1.destination_airport_id or t2.origin_airport_id is Null"""

        cursor.execute(query)

        for row in cursor:
            # result.append((idMap[row["ORIGIN_AIRPORT_ID"]], idMap[row["DESTINATION_AIRPORT_ID"]], row["peso"]))

            result.append(Tratta(idMap[row["A1"]], idMap[row["A2"]], row["peso"]))

        cursor.close()
        conn.close()
        return result