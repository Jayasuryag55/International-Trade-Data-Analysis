-- Top 25 HSN codes by value + Others
WITH hsn_totals AS (
    SELECT
        hsn_code,
        SUM(total_value_inr) AS total_value_inr
    FROM shipments
    GROUP BY hsn_code
),
sorted_hsn AS (
    SELECT
        hsn_code,
        total_value_inr,
        total_value_inr * 1.0 / SUM(total_value_inr) OVER () AS share_of_total,
        SUM(total_value_inr) OVER (ORDER BY total_value_inr DESC)
          * 1.0 / SUM(total_value_inr) OVER () AS cumulative_share,
        ROW_NUMBER() OVER (ORDER BY total_value_inr DESC) AS rn
    FROM hsn_totals
)
SELECT
    CASE
        WHEN rn <= 25 THEN hsn_code
        ELSE 'Others'
    END AS hsn_bucket,
    SUM(total_value_inr) AS total_value_inr,
    SUM(share_of_total)  AS share_of_total
FROM sorted_hsn
GROUP BY
    CASE
        WHEN rn <= 25 THEN hsn_code
        ELSE 'Others'
    END
ORDER BY
    CASE
        WHEN hsn_bucket = 'Others' THEN 99999
        ELSE 1
    END,
    total_value_inr DESC;
