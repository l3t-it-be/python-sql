CREATE_TABLE_USERS_BALANCE = """
  CREATE TABLE IF NOT EXISTS {table_name}
  (
    UserID INTEGER PRIMARY KEY,
    Balance_RUB FLOAT NOT NULL,
    Balance_USD FLOAT,
    Balance_EUR FLOAT
  );
"""

ADD_USER = """
INSERT INTO {table_name}
    (BALANCE_RUB, BALANCE_USD, BALANCE_EUR)
VALUES
    (?, ?, ?);
"""

ASSERT_USER_IN_SYSTEM = """
SELECT 1 
FROM {table_name} 
WHERE UserID = ?
LIMIT 1;
"""

SHOW_BALANCE = """
SELECT BALANCE_RUB, BALANCE_USD, BALANCE_EUR
FROM {table_name}
WHERE UserID = ?
LIMIT 1;
"""

UPDATE_BALANCE_RUB_TO_USD = """
UPDATE {table_name}
SET Balance_RUB = Balance_RUB - {amount_to_withdraw},
Balance_USD = Balance_USD + {amount_to_receive}
WHERE UserID = ?
"""

UPDATE_BALANCE_RUB_TO_EURO = """
UPDATE {table_name}
SET Balance_RUB = Balance_RUB - {amount_to_withdraw},
Balance_EUR = Balance_EUR + {amount_to_receive}
WHERE UserID = ?
"""

UPDATE_BALANCE_USD_TO_RUB = """
UPDATE {table_name}
SET Balance_USD = Balance_USD - {amount_to_withdraw},
Balance_RUB = Balance_RUB + {amount_to_receive}
WHERE UserID = ?
"""

UPDATE_BALANCE_USD_TO_EUR = """
UPDATE {table_name}
SET Balance_USD = Balance_USD - {amount_to_withdraw},
Balance_EUR = Balance_EUR + {amount_to_receive}
WHERE UserID = ?
"""

UPDATE_BALANCE_EUR_TO_RUB = """
UPDATE {table_name}
SET Balance_EUR = Balance_EUR - {amount_to_withdraw},
Balance_RUB = Balance_RUB + {amount_to_receive}
WHERE UserID = ?
"""

UPDATE_BALANCE_EUR_TO_USD = """
UPDATE {table_name}
SET Balance_EUR = Balance_EUR - {amount_to_withdraw},
Balance_USD = Balance_USD + {amount_to_receive}
WHERE UserID = ?
"""
