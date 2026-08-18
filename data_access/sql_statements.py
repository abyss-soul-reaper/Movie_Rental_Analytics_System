EXECUTIVE_KPI_BASE_QUERY = """
    SELECT
        COALESCE(SUM(p.amount), 0.00) AS total_revenue,
        COALESCE(AVG(p.amount), 0.00) AS average_ticket_size,
        COUNT(DISTINCT r.rental_id) AS total_rentals,
        COUNT(CASE WHEN r.return_date IS NOT NULL THEN 1 END) AS returned_rentals,
        COUNT(CASE WHEN r.rental_id IS NOT NULL AND r.return_date IS NULL THEN 1 END) AS active_ongoing_rentals
    FROM payment p
    LEFT JOIN rental r ON p.rental_id = r.rental_id
"""

STORE_PERFORMANCE_BASE_QUERY = """
    SELECT
        s.store_id,
        COALESCE(SUM(p.amount), 0.00) AS store_total_revenue,
        COUNT(DISTINCT r.rental_id) AS store_total_rentals
    FROM payment p
    INNER JOIN rental r ON p.rental_id = r.rental_id
    INNER JOIN inventory i ON r.inventory_id = i.inventory_id
    RIGHT JOIN store s ON i.store_id = s.store_id
"""



