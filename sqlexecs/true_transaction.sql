CREATE TABLE IF NOT EXISTS true_transaction (
    transaction_id         VARCHAR(255),
    date                   DATE,
    name                   VARCHAR(255),
    category               VARCHAR(255),
    subcategory            VARCHAR(255),
    actual_amount          NUMERIC(10, 2),
    insert_date            TIMESTAMP
);