def executive_kpi_query(handler, start_date=None, end_date=None):
    where_clause = ""
    params = []

    if start_date and end_date:
        where_clause = "WHERE p.payment_date BETWEEN %s AND %s"
        params = [start_date, end_date]

    query = f"""
        SELECT
            COALESCE(SUM(p.amount), 0.00) AS total_revenue,
            COALESCE(AVG(p.amount), 0.00) AS average_ticket_size,
            COUNT(DISTINCT r.rental_id) AS total_rentals,
            COUNT(CASE WHEN r.return_date IS NOT NULL THEN 1 END) AS returned_rentals,
            COUNT(CASE WHEN r.rental_id IS NOT NULL AND r.return_date IS NULL THEN 1 END) AS active_ongoing_rentals
        FROM payment p
        LEFT JOIN rental r ON p.rental_id = r.rental_id
        {where_clause};
    """
    
    return handler.fetch_all(query, tuple(params))

def store_performance_query(handler, start_date=None, end_date=None, store_id=None):
    conditions = []
    params = []

    if start_date and end_date:
        conditions.append("p.payment_date BETWEEN %s AND %s")
        params.extend([start_date, end_date])

    if store_id:
        conditions.append("i.store_id = %s")
        params.append(store_id)

    where_clause = f"WHERE {' AND '.join(conditions)}" if conditions else ""

    query = f"""
        SELECT
            s.store_id,
            COALESCE(SUM(p.amount), 0.00) AS store_total_revenue,
            COUNT(DISTINCT r.rental_id) AS store_total_rentals
        FROM store s
        LEFT JOIN inventory i ON s.store_id = i.store_id
        LEFT JOIN rental r ON i.inventory_id = r.inventory_id
        LEFT JOIN payment p ON r.rental_id = p.rental_id
        {where_clause}
        GROUP BY s.store_id;
    """
    
    return handler.fetch_all(query, tuple(params))




