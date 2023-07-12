CREATE OR REPLACE VIEW v_true_staging_transactions AS
with most_recent_true_transactions AS (SELECT t.transaction_id,
                                              t.actual_amount,
                                              max(t.insert_date)
                                       FROM true_transaction t
                                       GROUP BY t.transaction_id, t.actual_amount
                                       )
SELECT st.account_id,
       st.account_owner,
       CASE WHEN mrtt.actual_amount IS NOT NULL THEN mrtt.actual_amount
            ELSE st.amount
           END as amount,
       st.authorized_date,
       st.category,
       st.subcategory,
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
    LEFT OUTER JOIN most_recent_true_transactions mrtt
        ON mrtt.transaction_id = st.transaction_id