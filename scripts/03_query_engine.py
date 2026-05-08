import io
import os
import boto3
import pandas as pd
from moto import mock_aws

def format_table(title, df):
    print(f"\n[QUERY] {title}...")
    # Convert string columns using string formatting for cleaner display
    # This is optional, but Pandas to_string looks good enough
    print(df.to_string(index=False))

@mock_aws
def run_queries():
    s3_client = boto3.client('s3', region_name='us-east-1')
    bucket_name = "pharma-sales-pipeline"
    file_key = "processed/pharma_sales_clean.csv"
    
    try:
        response = s3_client.get_object(Bucket=bucket_name, Key=file_key)
        df = pd.read_csv(io.BytesIO(response['Body'].read()))
    except Exception as e:
        print(f"[ERROR] Could not read file from S3 processed/ folder: {e}")
        return False

    os.makedirs('output', exist_ok=True)
    queries_run = 0

    # Pre-processing
    df['order_date'] = pd.to_datetime(df['order_date'])
    total_rev = df['total_amount'].sum()

    # Query 1: Total revenue by region
    q1 = df.groupby('region')['total_amount'].sum().reset_index()
    q1.rename(columns={'total_amount': 'total_revenue'}, inplace=True)
    q1['revenue_share%'] = (q1['total_revenue'] / total_rev * 100).round(2)
    q1 = q1.sort_values('total_revenue', ascending=False)
    format_table("Total Revenue by Region", q1)
    
    q1_csv = q1.to_csv(index=False)
    s3_client.put_object(Bucket=bucket_name, Key="output/q1_revenue_by_region.csv", Body=q1_csv)
    q1.to_csv("output/q1_revenue_by_region.csv", index=False)
    print(f"[RESULT]  {len(q1)} regions | Saved -> output/")
    queries_run += 1

    # Query 2: Monthly sales trend
    df['year'] = df['order_date'].dt.year
    df['month'] = df['order_date'].dt.month
    q2 = df.groupby(['year', 'month'])['total_amount'].sum().reset_index()
    q2.rename(columns={'total_amount': 'total_revenue'}, inplace=True)
    q2 = q2.sort_values(['year', 'month'])
    q2['mom_growth%'] = q2['total_revenue'].pct_change().fillna(0) * 100
    q2['mom_growth%'] = q2['mom_growth%'].round(2)
    format_table("Monthly Sales Trend", q2.head(10)) # Print head to save space
    
    q2_csv = q2.to_csv(index=False)
    s3_client.put_object(Bucket=bucket_name, Key="output/q2_monthly_trend.csv", Body=q2_csv)
    q2.to_csv("output/q2_monthly_trend.csv", index=False)
    print(f"[RESULT]  {len(q2)} months | Saved -> output/")
    queries_run += 1

    # Query 3: Top 10 products by units sold
    q3 = df.groupby('product_name').agg(
        total_units=('quantity', 'sum'),
        total_revenue=('total_amount', 'sum')
    ).reset_index()
    q3 = q3.sort_values('total_units', ascending=False).head(10)
    format_table("Top 10 Products by Units Sold", q3)
    
    q3_csv = q3.to_csv(index=False)
    s3_client.put_object(Bucket=bucket_name, Key="output/q3_top_products.csv", Body=q3_csv)
    q3.to_csv("output/q3_top_products.csv", index=False)
    print(f"[RESULT]  {len(q3)} products | Saved -> output/")
    queries_run += 1

    # Query 4: Revenue share by product category
    q4 = df.groupby('product_category')['total_amount'].sum().reset_index()
    q4.rename(columns={'total_amount': 'revenue'}, inplace=True)
    q4['percentage'] = (q4['revenue'] / total_rev * 100).round(2)
    q4 = q4.sort_values('revenue', ascending=False)
    format_table("Revenue Share by Product Category", q4)
    
    q4_csv = q4.to_csv(index=False)
    s3_client.put_object(Bucket=bucket_name, Key="output/q4_category_share.csv", Body=q4_csv)
    q4.to_csv("output/q4_category_share.csv", index=False)
    print(f"[RESULT]  {len(q4)} categories | Saved -> output/")
    queries_run += 1

    # Query 5: Data quality summary
    q5 = pd.DataFrame([{
        'total_rows': len(df),
        'date_range': f"{df['order_date'].min().strftime('%Y-%m-%d')} to {df['order_date'].max().strftime('%Y-%m-%d')}",
        'avg_order_value': round(df['total_amount'].mean(), 2),
        'total_revenue': round(total_rev, 2)
    }])
    format_table("Data Quality Summary", q5)
    
    q5_csv = q5.to_csv(index=False)
    s3_client.put_object(Bucket=bucket_name, Key="output/q5_data_summary.csv", Body=q5_csv)
    q5.to_csv("output/q5_data_summary.csv", index=False)
    print(f"[RESULT]  {len(q5)} summary row | Saved -> output/")
    queries_run += 1

    return queries_run

if __name__ == "__main__":
    print("Run via 04_pipeline_runner.py to share the S3 mock state.")
