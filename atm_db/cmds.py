CREATE_TABLE_USERS_DATA = """
  CREATE TABLE IF NOT EXISTS {table_name}
  (
    UserID INTEGER PRIMARY KEY,
    CardNumber INTEGER UNIQUE NOT NULL,
    PinCode INTEGER NOT NULL,
    Balance INTEGER NOT NULL,
    IsBlocked BOOLEAN DEFAULT FALSE
  );
"""

SELECT_CARD_NUMBER_IF_EXISTS = """
    SELECT CardNumber
    FROM {table_name}
    WHERE CardNumber = ?
    LIMIT 1;
"""

INSERT_USERS_DATA = """
INSERT INTO {table_name}
    (CardNumber, PinCode, Balance)
VALUES
    (?, ?, ?);
"""

SELECT_CARD_NUMBER_AND_IsBlocked = """
SELECT CardNumber, IsBlocked
FROM {table_name}
WHERE CardNumber = ?
LIMIT 1;
"""

SELECT_PIN_CODE = """
SELECT PinCode
FROM {table_name}
WHERE CardNumber = ?
LIMIT 1;
"""

BLOCK_CARD_NUMBER = """
UPDATE {table_name}
SET IsBlocked = True
WHERE CardNumber = ?;
"""

SHOW_BALANCE = """
SELECT Balance
FROM {table_name}
WHERE CardNumber = ?
LIMIT 1;
"""

REDUCE_BALANCE = """
UPDATE {table_name}
SET Balance = Balance - {amount}
WHERE CardNumber = ?;
"""

INCREASE_BALANCE = """
UPDATE {table_name}
SET Balance = Balance + {amount}
WHERE CardNumber = ?;
"""

TRANSFER_MONEY = """
UPDATE {table_name}
SET Balance = Balance - {amount}
WHERE CardNumber = ?;
UPDATE {table_name}
SET Balance = Balance + {amount}
WHERE CardNumber = ?;
"""
