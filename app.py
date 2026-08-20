from services.metrics_service import *
from data_access.mysql_client import DatabaseHandler as dbh
data = get_executive_dashboard_metrics(dbh())

if data.success:
    print("Dashboard Metrics Retrieved Successfully:")
    for key, value in data.data.items():
        print(f"{key}: {value}")
else:
    print(f"Error: {data.error_msg} (Code: {data.error_code})")