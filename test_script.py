import sqlite3


def get_db_connection():
    conn = sqlite3.connect("database.db")
    print("Connected to database successfully")
    conn.row_factory = sqlite3.Row
    return conn

def delete_db():
    pass

def get_record(room_number):
    with get_db_connection() as conn:
        cursor = conn.cursor()

        # First, find the entry to update
        find_query = """
        SELECT * FROM HotelManagement
        WHERE invoice_no IS NULL AND room_no = ?
        """
        cursor.execute(find_query, (room_number,))
        results = cursor.fetchall()
        for result in results:
            print(list(result))
        # result_list = [list(row[0]) for row in results]
        # print(result_list)
        print("resultslen", len(results))

def main():
    get_record('103 - xcvbh')
    # with get_db_connection() as conn:
    #     cursor = conn.cursor()

        # delete_query = """
        #     DELETE FROM HotelManagement
        #     WHERE id IN (3, 4, 5);
        # """

        # cursor.execute(delete_query)

main()
