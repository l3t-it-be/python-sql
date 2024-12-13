CREATE_TABLE_USERS_DATA = """
    CREATE TABLE IF NOT EXISTS {table_name} (
    UserID INTEGER PRIMARY KEY,
    Login TEXT UNIQUE NOT NULL,
    Password TEXT NOT NULL,
    Code TEXT NOT NULL
);
"""

ASSERT_LOGIN_IN_SYSTEM = """
    SELECT Login, Password
    FROM {table_name}
    WHERE LOWER(Login) = ?
    LIMIT 1;
"""

ADD_NEW_USER = """
INSERT INTO {table_name}
    (Login, Password, Code)
VALUES
    (?, ?, ?);
"""

ASSERT_LOGIN_MATCHES_CODE = """
    SELECT 1
    FROM {table_name}
    WHERE LOWER(Login) = ? AND Code = ?
    LIMIT 1;
"""

UPDATE_PASSWORD = """
    UPDATE {table_name}
    SET Password = ?
    WHERE LOWER(Login) = ?;
"""
