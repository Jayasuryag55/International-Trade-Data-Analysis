-- Supplier active vs churned in 2025
WITH supplier_years AS (
    SELECT DISTINCT
        supplier_name,
        year
    FROM shipments
    WHERE supplier_name IS NOT NULL
),
base AS (
    SELECT
        supplier_name,
        MIN(year) AS first_year,
        MAX(year) AS last_year,
        MAX(CASE WHEN year = 2025 THEN 1 ELSE 0 END) AS has_2025
    FROM supplier_years
    GROUP BY supplier_name
)
SELECT
    supplier_name,
    first_year,
    last_year,
    CASE
        WHEN has_2025 = 1 THEN 'Active_2025'
        WHEN has_2025 = 0 AND last_year < 2025 THEN 'Churned'
        ELSE 'Other'
    END AS supplier_status_2025
FROM base
ORDER BY supplier_name;
