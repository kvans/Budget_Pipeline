CREATE OR REPLACE VIEW v_true_staging_transactions AS
with most_recent_true_transactions AS (SELECT t.transaction_id,
                                              max(t.insert_date) as max_insert_date
                                       FROM true_transaction t
                                       GROUP BY t.transaction_id
                                       ),
    max_most_recent_true_transactions as (
            SELECT
                tt.transaction_id,
                tt.actual_amount,
                tt.category,
                tt.subcategory,
                tt.insert_date
            FROM most_recent_true_transactions mrtt
                INNER JOIN true_transaction tt
                    ON mrtt.transaction_id = tt.transaction_id
                        AND mrtt.max_insert_date = tt.insert_date
        )
SELECT st.account_id,
       st.account_owner,
       CASE WHEN mrtt.actual_amount > 0.00 THEN mrtt.actual_amount
            ELSE st.amount
           END as amount,
       st.authorized_date,
       CASE WHEN mrtt.category != '' THEN mrtt.category
            ELSE st.category
            END as category,
       CASE WHEN mrtt.subcategory != '' THEN mrtt.subcategory
            ELSE st.subcategory
            END as subcategory,
       st.category_id,
       st.date,
       st.iso_currency_code,
       st.merchant_name,
       st.name,
       st.payment_channel,
       st.pending,
       st.pending_transaction_id,
       st.transaction_id,
       st.transaction_type,
       st.mask,
       st.insertdate
FROM staging__transactions st
    LEFT OUTER JOIN max_most_recent_true_transactions mrtt
        ON mrtt.transaction_id = st.transaction_id