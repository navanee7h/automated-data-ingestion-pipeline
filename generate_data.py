import pandas as pd
import numpy as np
from datetime import datetime, timedelta

def generate_data():
    num_records = 50000
    np.random.seed(42)
    
    order_ids = [f"ORD{i:06d}" for i in range(1, num_records + 1)]
    start_date = datetime(2021, 1, 1)
    order_dates = [(start_date + timedelta(days=np.random.randint(0, 365*4))).strftime('%Y-%m-%d') for _ in range(num_records)]
    
    products = ['Aspirin', 'Ibuprofen', 'Amoxicillin', 'Lisinopril', 'Metformin']
    categories = ['Pain Relief', 'Antibiotics', 'Blood Pressure', 'Diabetes']
    product_names = np.random.choice(products, num_records)
    product_categories = np.random.choice(categories, num_records)
    
    quantities = np.random.randint(1, 100, num_records)
    unit_prices = np.random.uniform(5.0, 150.0, num_records).round(2)
    total_amounts = (quantities * unit_prices).round(2)
    
    regions = ['North', 'South', 'East', 'West']
    cities = ['New York', 'Los Angeles', 'Chicago', 'Houston', 'Phoenix']
    row_regions = np.random.choice(regions, num_records)
    row_cities = np.random.choice(cities, num_records)
    
    customer_names = [f"Hospital_{i}" for i in np.random.randint(1, 100, num_records)]
    customer_segments = ['Hospital', 'Pharmacy', 'Clinic']
    row_segments = np.random.choice(customer_segments, num_records)
    
    df = pd.DataFrame({
        'order_id': order_ids,
        'order_date': order_dates,
        'product_name': product_names,
        'product_category': product_categories,
        'quantity': quantities,
        'unit_price': unit_prices,
        'total_amount': total_amounts,
        'region': row_regions,
        'city': row_cities,
        'customer_name': customer_names,
        'customer_segment': row_segments
    })
    
    import os
    os.makedirs('data', exist_ok=True)
    df.to_csv('data/pharma_sales_clean.csv', index=False)
    print("Data generated!")

if __name__ == '__main__':
    generate_data()
