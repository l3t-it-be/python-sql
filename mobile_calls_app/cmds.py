CREATE_TABLE_MOBILE_BALANCE = """
CREATE TABLE IF NOT EXISTS {table_name}
(
    UserID INTEGER PRIMARY KEY,
    User TEXT UNIQUE NOT NULL,
    Balance INTEGER NOT NULL
);
"""

CREATE_TABLE_MOBILE_PRICE = """
CREATE TABLE IF NOT EXISTS {table_name}
(
    PriceID INTEGER PRIMARY KEY,
    Mts_Mts INTEGER NOT NULL,
    Mts_Tele2 INTEGER NOT NULL,
    Mts_Yota INTEGER NOT NULL
);
"""

ASSERT_USER_IN_SYSTEM = """
    SELECT 1
    FROM {table_name}
    WHERE LOWER(User) = ?
    LIMIT 1;
"""

SELECT_USER_ID = """
SELECT UserID 
FROM {table_name} 
WHERE LOWER(User) = ?;
"""

INSERT_USER_DATA = """
INSERT INTO {table_name}
    (User, Balance)
VALUES
    (?, ?);
"""

CHECK_PRICES_EXIST = """
    SELECT 1
    FROM {table_name}
    LIMIT 1;
"""

ADD_PRICES = """
INSERT INTO {table_name}
    (Mts_Mts, Mts_Tele2, Mts_Yota)
VALUES
    (?, ?, ?);
"""

GET_RANDOM_OPERATOR = """
SELECT *
FROM {table_name}
LIMIT 1;
"""

UPDATE_BALANCE = """
UPDATE {table_name}
SET Balance = Balance - ?
WHERE UserID = ?;
"""

GET_USER_BALANCE = """
SELECT Balance
FROM {table_name}
WHERE UserID = ?;
"""
