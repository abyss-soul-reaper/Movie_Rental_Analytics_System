def customer_segments(data, limit=10):
    from collections import Counter

    # 1. Gather counts from ALL data rows
    segment_counts = Counter(row["segment_label"] for row in data)
    total_customers = len(data)

    # 2. Print the summary section
    print("--- SUMMARY ---")
    for segment, count in segment_counts.items():
        percentage = (count / total_customers) * 100
        print(f"{segment:<8}: {count:<3} customers  ({percentage:.0f}%)")
    print("---------------\n")

    print("--- TOP 10 CUSTOMERS ---")
    for row in data[:limit]:  
        print("-" * 50)
        print(f"Customer ID: {row['customer_id']:<10}")
        print(f"Customer Name: {row['customer']:<30}")
        print(f"Total Rentals: {row['rentals']:<10}")
        print(f"Customer Segment: {row['customer_segment']:<10} ({row['segment_label']})")
        print("-" * 50)

from db import DatabaseHandler as DBHandler

from database.queries import get_customer_segments

customer_segments(get_customer_segments(DBHandler()))


