from services.metrics_service import *
from data_access.mysql_client import DatabaseHandler as dbh
data = get_executive_dashboard_metrics(dbh())

for k, v in data.data.items():
    print(f"{k}: {v}")