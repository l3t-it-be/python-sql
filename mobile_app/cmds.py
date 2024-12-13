CREATE_TABLE_MOBILE_USERS = """
CREATE TABLE IF NOT EXISTS {table_name} 
(
        UserID INTEGER PRIMARY KEY,
        User_name TEXT UNIQUE NOT NULL,
        Balance INTEGER NOT NULL,
        Mobile_tariff_ref INTEGER,
        Activity TEXT DEFAULT 'Yes'
    );
"""

CREATE_TABLE_MOBILE_TARIFFS = """
CREATE TABLE IF NOT EXISTS {table_name} 
(
        TariffID INTEGER PRIMARY KEY,
        Tariff TEXT UNIQUE NOT NULL,
        Price INTEGER NOT NULL
    );
"""

ASSERT_USER_NAME_IN_SYSTEM = """
    SELECT 1
    FROM {table_name}
    WHERE LOWER(User_name) = ?
    LIMIT 1;
"""

ASSERT_TARIFF_IN_SYSTEM = """
    SELECT 1
    FROM {table_name}
    WHERE LOWER(Tariff) = ?
    LIMIT 1;
"""

INSERT_USERS_DATA = """
INSERT INTO {table_name}
    (User_name, Balance, Mobile_tariff_ref)
VALUES
    (?, ?, ?);
"""

ADD_TARIFF = """
INSERT INTO {table_name}
    (Tariff, Price)
VALUES
    (?, ?);
"""

GET_ACTIVE_USERS = """
SELECT UserID, User_name, Balance, Mobile_tariff_ref
FROM {table_name}
WHERE Activity = 'Yes';
"""

GET_TARIFF_INFO = """
SELECT Tariff, Price FROM {table_name} 
WHERE TariffID = ?
LIMIT 1;
"""

UPDATE_USER_BALANCE = """
UPDATE {table_name} 
SET Balance = ? 
WHERE UserID = ?;
"""

UPDATE_USER_ACTIVITY = """
UPDATE {table_name} 
SET Activity = 'No' 
WHERE UserID = ?;
"""
