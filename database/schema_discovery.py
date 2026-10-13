# database/schema_discovery.py
from database.connection import get_connection


def discover_schema():
    """Auto-discover all tables, columns, types, and relationships from the database."""
    conn = get_connection()
    cursor = conn.cursor()

    # Step 1: Get all tables in the public schema
    cursor.execute("""
        SELECT table_name 
        FROM information_schema.tables 
        WHERE table_schema = 'public' 
        AND table_type = 'BASE TABLE'
        ORDER BY table_name
    """)
    tables = [row[0] for row in cursor.fetchall()]

    schema = {}

    for table in tables:
        # Step 2: Get columns, data types, and nullable info
        cursor.execute("""
            SELECT column_name, data_type, is_nullable, column_default
            FROM information_schema.columns
            WHERE table_schema = 'public' AND table_name = %s
            ORDER BY ordinal_position
        """, (table,))

        columns = []
        for col_name, data_type, nullable, default in cursor.fetchall():
            columns.append({
                "name": col_name,
                "type": data_type,
                "nullable": nullable == "YES",
                "has_default": default is not None
            })

        # Step 3: Get foreign keys (relationships)
        cursor.execute("""
            SELECT
                kcu.column_name,
                ccu.table_name AS foreign_table,
                ccu.column_name AS foreign_column
            FROM information_schema.table_constraints AS tc
            JOIN information_schema.key_column_usage AS kcu
                ON tc.constraint_name = kcu.constraint_name
            JOIN information_schema.constraint_column_usage AS ccu
                ON ccu.constraint_name = tc.constraint_name
            WHERE tc.constraint_type = 'FOREIGN KEY'
            AND tc.table_name = %s
        """, (table,))

        foreign_keys = []
        for col, foreign_table, foreign_col in cursor.fetchall():
            foreign_keys.append({
                "column": col,
                "references_table": foreign_table,
                "references_column": foreign_col
            })

        # Step 4: Get row count
        cursor.execute(f"SELECT COUNT(*) FROM {table}")
        row_count = cursor.fetchone()[0]

        # Step 5: Get sample data (first 3 rows)
        cursor.execute(f"SELECT * FROM {table} LIMIT 3")
        sample_columns = [desc[0] for desc in cursor.description]
        sample_rows = []
        for row in cursor.fetchall():
            sample_rows.append(dict(zip(sample_columns, row)))

        schema[table] = {
            "columns": columns,
            "foreign_keys": foreign_keys,
            "row_count": row_count,
            "sample_data": sample_rows
        }

    conn.close()
    return schema


def schema_to_prompt_text(schema):
    """Convert discovered schema into text that goes into the LLM system prompt."""
    lines = []
    lines.append("DATABASE SCHEMA:")
    lines.append("=" * 50)

    for table_name, info in schema.items():
        lines.append(f"\nTable: {table_name} ({info['row_count']} rows)")
        lines.append("-" * 40)

        # Columns
        lines.append("Columns:")
        for col in info["columns"]:
            nullable = "nullable" if col["nullable"] else "not null"
            lines.append(f"  - {col['name']} ({col['type']}, {nullable})")

        # Foreign keys
        if info["foreign_keys"]:
            lines.append("Relationships:")
            for fk in info["foreign_keys"]:
                lines.append(
                    f"  - {fk['column']} → {fk['references_table']}.{fk['references_column']}"
                )

        # Sample data
        if info["sample_data"]:
            lines.append("Sample data (first 3 rows):")
            for row in info["sample_data"]:
                lines.append(f"  {row}")

    return "\n".join(lines)


# Quick test
if __name__ == "__main__":
    print("Discovering schema...")
    schema = discover_schema()
    prompt_text = schema_to_prompt_text(schema)
    print(prompt_text)