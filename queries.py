def rental_count(handler):
    data = handler.fetch_all("""
        SELECT COUNT(rental_id) AS `rental_count`
        FROM rental
    """)
    return data

def rented_movies(handler, limit=None):
    query = f"""
        SELECT f.title AS `movie`, COUNT(r.rental_id) AS `rentals per movie`
        FROM rental r
        JOIN inventory i ON r.inventory_id = i.inventory_id
        JOIN film f ON i.film_id = f.film_id
        GROUP BY f.film_id, f.title
        ORDER BY `rentals per movie` DESC
        {"LIMIT %s" if limit is not None else ""}
    """
    params = (limit,) if limit is not None else ()

    return handler.fetch_all(query, params)

def get_customer_segments(handler):
    query = f"""
        WITH customer_rentals AS (
            SELECT
                c.customer_id,
                CONCAT_WS(' ', c.first_name, c.last_name) AS customer,
                COUNT(r.rental_id) AS `rentals`
                FROM customer c
                LEFT JOIN rental r ON c.customer_id = r.customer_id
                GROUP BY c.customer_id, c.first_name, c.last_name
        ),

        customer_segments AS (
            SELECT
                cr.customer_id,
                cr.customer,
                cr.rentals,
                NTILE(3) OVER(ORDER BY cr.rentals, cr.customer_id) AS `customer_segment`
            FROM customer_rentals cr
        )

        SELECT
            cs.customer_id,
            cs.customer,
            cs.rentals,
            cs.customer_segment,

            CASE cs.customer_segment
                WHEN 1 THEN 'Casual'
                WHEN 2 THEN 'Regular'
                ELSE 'Heavy'
            END AS `segment_label`

        FROM customer_segments cs
        ORDER BY cs.rentals DESC, cs.customer_id;
    """

    return handler.fetch_all(query)

def revenue_per_store(handler, limit=None):
    query = f"""
        SELECT st.store_id, SUM(p.amount) AS `revenue per store`
        FROM payment p
        JOIN staff sf ON p.staff_id = sf.staff_id
        JOIN store st ON sf.store_id = st.store_id
        GROUP BY st.store_id
        ORDER BY `revenue per store` DESC
        {"LIMIT %s" if limit is not None else ""}
    """
    params = (limit,) if limit is not None else ()

    return handler.fetch_all(query, params)

def rentals_per_month(handler):
    query = """
        SELECT COUNT(rental_id) AS `rentals per month`, DATE_FORMAT(rental_date, '%Y-%m') AS `month`
        FROM rental
        GROUP BY DATE_FORMAT(rental_date, '%Y-%m')
        ORDER BY `rentals per month`
    """

    return handler.fetch_all(query)




