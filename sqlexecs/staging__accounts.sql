-- Drop the existing table if it exists
CREATE TABLE IF NOT EXISTS staging__accounts (
    account_id                          text,
    mask                                text,
    name                                text,
    official_name                       text,
    type                                text,
    subtype                             text,
    balances_available                  double precision,
    balances_current                    double precision,
    balances_limit                      double precision,
    balances_iso_currency_code          text,
    balances_unofficial_currency_code   text,
    insertDate                          timestamp
);

TRUNCATE TABLE staging__accounts;


INSERT INTO staging__accounts
SELECT
    account_id,
    mask,
    name,
    official_name,
    type,
    subtype,
    "balances.available" ,
    "balances.current" ,
    "balances.limit",
    "balances.iso_currency_code" ,
    "balances.unofficial_currency_code",
    max("insertDate") as insertdate
FROM base_accounts
GROUP BY
    account_id,
    mask,
    name,
    official_name,
    type,
    subtype,
    "balances.available" ,
    "balances.current" ,
    "balances.limit",
    "balances.iso_currency_code" ,
    "balances.unofficial_currency_code";