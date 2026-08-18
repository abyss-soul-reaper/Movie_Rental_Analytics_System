# app.py
from data_access.sql_statements import executive_kpi_query, store_performance_query
from data_access.mysql_client import DatabaseHandler

# 1. إنشاء كائن الاتصال
db_client = DatabaseHandler()

# 2. تنفيذ الاستعلام (العائد هنا كائن ResponseHandler بفضل الـ Decorator)
response = executive_kpi_query(db_client)

# 3. التحقق من نجاح العملية وطباعة البيانات
if response.success:
    # بداخل .data توجد القائمة الفعلية القادمة من fetch_all
    for row in response.data:
        print(row)
else:
    print(f"{response.error_msg}")
