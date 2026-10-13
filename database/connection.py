# database/connection.py
import psycopg2
from config import DATABASE_URL


def get_connection():
    """Create a connection to PostgreSQL."""
    return psycopg2.connect(DATABASE_URL)


def run_query(sql):
    """Execute a SQL query and return results as list of dicts."""
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(sql)

        # Get column names
        columns = [desc[0] for desc in cursor.description]

        # Get all rows
        rows = cursor.fetchall()

        conn.close()

        # Convert to list of dicts
        results = []
        for row in rows:
            results.append(dict(zip(columns, row)))

        return {"success": True, "data": results, "row_count": len(results)}

    except Exception as e:
        return {"success": False, "error": str(e), "data": []}