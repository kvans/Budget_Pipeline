-- Drop the existing table if it exists
CREATE TABLE IF NOT EXISTS staging__transactions (
    account_id             VARCHAR(255),
    account_owner          VARCHAR(255),
    amount                 NUMERIC(10, 2),
    authorized_date        DATE,
    category               VARCHAR(255),
    subcategory               VARCHAR(255),
    category_id            VARCHAR(255),
    date                   DATE,
    iso_currency_code      VARCHAR(3),
    merchant_name          VARCHAR(255),
    name                   VARCHAR(255),
    payment_channel        VARCHAR(255),
    pending                BOOLEAN,
    pending_transaction_id VARCHAR(255),
    transaction_id         VARCHAR(255),
    transaction_type       VARCHAR(255),
    mask                   VARCHAR(255),
    insertdate             TIMESTAMP
);

TRUNCATE TABLE staging__transactions;

-- Create the new table based on a query

with updated_account_infos as (SELECT t.account_id
                                    , sa.mask
                                    , min(CAST(authorized_date as DATE)) as starting_date
                                    , max(CAST(authorized_date as DATE)) as ending_date
                               FROM base_transactions t
                                        INNER JOIN staging__accounts sa
                                                   ON sa.account_id = t.account_id
                               group by 1, 2
                               ORDER BY sa.mask, starting_date
                               ),
correct_account_ids_for_time_period as (SELECT account_id,
                                               mask,
                                               CASE
                                                   WHEN lag(ending_date) OVER (PARTITION BY mask ORDER BY ending_date) IS NULL
                                                       THEN starting_date
                                                   ELSE lag(ending_date) OVER (PARTITION BY mask ORDER BY ending_date)
                                                   END as start_ending,
                                               ending_date
                                        FROM updated_account_infos),
semi_structered_transactions as (SELECT bt.*
                                      , ca.mask
                                 FROM base_transactions bt
                                          INNER JOIN correct_account_ids_for_time_period ca
                                                     ON ca.account_id = bt.account_id
                                                         AND CAST(bt.authorized_date as date) >= ca.start_ending
                                                         and CAST(bt.authorized_date as date) <= ca.ending_date
                                )
INSERT INTO staging__transactions
SELECT
    account_id,
    account_owner,
    amount,
    CAST(authorized_date as date) as authorized_date,
    --Wanted to split out categories to make it easier to query
    split_part(trim(both '{}' from category), ',', 1) AS category,
    split_part(trim(both '{}' from category), ',', 2) AS subcategory,
    category_id,
    CAST(date as date) as date,
    iso_currency_code,
    merchant_name,
    name,
    payment_channel,
    pending,
    pending_transaction_id,
    transaction_id,
    transaction_type,
    mask,
    max("insertDate") as insertdate
from semi_structered_transactions
WHERE authorized_date <= '2023-06-14'
GROUP BY account_id, account_owner, amount, CAST(authorized_date as date), split_part(trim(both '{}' from category), ',', 1), split_part(trim(both '{}' from category), ',', 2), category_id, CAST(date as date), iso_currency_code, merchant_name, name, payment_channel, pending, pending_transaction_id, transaction_id, transaction_type, mask
ORDER BY authorized_date desc
