from pkg_exceptions.output_handler import ResponseHandler
from data_access.sql_statements import EXECUTIVE_KPI_BASE_QUERY, STORE_PERFORMANCE_BASE_QUERY

def get_executive_dashboard_metrics(handler, start_date=None, end_date=None, store_id=None):
    kpi_conditions = []
    kpi_params = []

    store_conditions = []
    store_params = []

    if start_date:
        kpi_conditions.append("p.payment_date >= %s")
        kpi_params.append(start_date)

        store_conditions.append("p.payment_date >= %s")
        store_params.append(start_date)

    if end_date:
        kpi_conditions.append("p.payment_date <= %s")
        kpi_params.append(end_date)

        store_conditions.append("p.payment_date <= %s")
        store_params.append(end_date)

    if store_id:
        store_conditions.append("s.store_id = %s")
        store_params.append(store_id)

    kpi_where = f"WHERE {' AND '.join(kpi_conditions)}" if kpi_conditions else ""
    store_where = f"WHERE {' AND '.join(store_conditions)}" if store_conditions else ""

    final_kpi_query = f"{EXECUTIVE_KPI_BASE_QUERY} {kpi_where};"
    final_store_query = f"{STORE_PERFORMANCE_BASE_QUERY} {store_where} GROUP BY s.store_id ORDER BY s.store_id;"

    company_response = handler.fetch_one(final_kpi_query, tuple(kpi_params))
    stores_response = handler.fetch_all(final_store_query, tuple(store_params))

    if company_response.success and stores_response.success:
        company_kpis = company_response.data
        stores_raw_data = stores_response.data


        total_revenue = float(company_kpis.get("total_revenue", 0.00))
        total_rentals = int(company_kpis.get("total_rentals", 0))

        avg_rental_value = round(total_revenue / total_rentals, 2) if total_rentals > 0 else 0.00

        stores_performance_list = []
        top_store_id = None
        top_store_revenue = -1.0

        for store in stores_raw_data:
            s_id = store.get("store_id")
            s_rev = float(store.get("store_total_revenue", 0.00))
            s_ren = int(store.get("store_total_rentals", 0))

            s_contribution = round((s_rev / total_revenue) * 100, 2) if total_revenue > 0 else 0.00

            stores_performance_list.append({
                "store_id": s_id,
                "store_total_revenue": s_rev,
                "store_total_rentals": s_ren,
                "store_contribution": s_contribution
            })

            if s_rev > top_store_revenue:
                top_store_revenue = s_rev
                top_store_id = s_id

        dashborad_data = {
        "company_overview": {
            "revenue": total_revenue,
            "rentals": total_rentals,
            "avg_rental_value": avg_rental_value,
            "active_rentals": int(company_kpis.get("active_ongoing_rentals", 0)),
            "returned_rentals": int(company_kpis.get("returned_rentals", 0))
        },

        "stores_performance": stores_performance_list,
        
        "top_store": {
            "store_id": top_store_id,
            "revenue": top_store_revenue
        }
    }

        return ResponseHandler.ok(dashborad_data)
    
    else:
        error_info = {
            "msg": "Failed to retrieve dashboard metrics.",
            "technical_msg": f"Company Response: {company_response.error_msg}, Stores Response: {stores_response.error_msg}",
            "code": 500
        }
        return ResponseHandler.exception(**error_info)
    

