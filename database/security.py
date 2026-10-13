# database/security.py

BLOCKED_KEYWORDS = ["DROP", "DELETE", "UPDATE", "ALTER", "TRUNCATE", "INSERT", "GRANT", "REVOKE"]


def validate_sql(sql):
    """Check if SQL is safe to execute. Returns (is_safe, reason)."""
    sql_upper = sql.upper().strip()

    for keyword in BLOCKED_KEYWORDS:
        # Check if keyword appears as a standalone word
        if keyword in sql_upper.split():
            return False, f"Blocked: contains {keyword} statement"

    # Must start with SELECT or WITH (for CTEs)
    if not (sql_upper.startswith("SELECT") or sql_upper.startswith("WITH")):
        return False, "Blocked: query must start with SELECT or WITH"

    return True, "Safe"