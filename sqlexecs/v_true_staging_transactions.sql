
CREATE OR REPLACE VIEW v_true_staging_transactions AS
with most_recent_true_transactions AS (SELECT t.transaction_id,
                                              t.actual_amount,
                                              max(t.insert_date)
                                       FROM true_transaction t
                                       GROUP BY t.transaction_id, t.actual_amount
                                       )
    ,most_recent_category as (
        SELECT
            c.name,
            c.category,
            c.subcategory,
            max(c.insert_date)
        FROM true_category c
        WHERE c.subcategory IS NOT NULL
        GROUP BY name, category, subcategory
    ),
    most_recent_true_category as (
        SELECT
            c.name,
            c.category,
            c.subcategory,
            tc.updatedCategory,
            tc.updatedSubcategory
        FROM most_recent_category c
            INNER JOIN true_category tc
                ON tc.name = c.name
                AND tc.category = c.category
                AND tc.subcategory = c.subcategory
    )
SELECT st.account_id,
       st.account_owner,
       CASE WHEN mrtt.actual_amount IS NOT NULL THEN mrtt.actual_amount
            ELSE st.amount
           END as amount,
       st.authorized_date,
       CASE WHEN cat.updatedCategory IS NOT NULL THEN cat.updatedCategory
            ELSE st.category
            END as category,
       CASE WHEN cat.updatedSubCategory IS NOT NULL THEN cat.updatedSubCategory
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
    LEFT OUTER JOIN most_recent_true_transactions mrtt
        ON mrtt.transaction_id = st.transaction_id
    LEFT OUTER JOIN most_recent_true_category cat
        ON cat.name = st.name
        AND cat.category = st.category
        AND cat.subcategory = st.subcategory