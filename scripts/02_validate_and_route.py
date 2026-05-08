import io
import boto3
import pandas as pd
from moto import mock_aws

@mock_aws
def validate_and_route():
    print("[VALIDATE] Running data quality checks...")
    
    s3_client = boto3.client('s3', region_name='us-east-1')
    bucket_name = "pharma-sales-pipeline"
    file_key = "raw/pharma_sales_clean.csv"
    
    try:
        response = s3_client.get_object(Bucket=bucket_name, Key=file_key)
        df = pd.read_csv(io.BytesIO(response['Body'].read()))
    except Exception as e:
        print(f"[ERROR] Could not read file from S3: {e}")
        return False
        
    checks_passed = 0
    errors = []
    
    # Check 1: All required columns exist
    required_cols = [
        'order_id', 'order_date', 'product_name', 'product_category',
        'quantity', 'unit_price', 'total_amount', 'region', 'city',
        'customer_name', 'customer_segment'
    ]
    if all(col in df.columns for col in required_cols):
        print("    [PASS] Column structure check")
        checks_passed += 1
    else:
        print("    [FAIL] Column structure check")
        errors.append("Missing required columns")

    # Check 2: No nulls in critical columns
    critical_cols = ['order_id', 'order_date', 'total_amount', 'region']
    if df[critical_cols].isnull().sum().sum() == 0:
        print("    [PASS] Null check on critical columns")
        checks_passed += 1
    else:
        print("    [FAIL] Null check on critical columns")
        errors.append("Nulls found in critical columns")

    # Check 3: Row count > 40,000
    row_count = len(df)
    if row_count > 40000:
        print(f"    [PASS] Row count check ({row_count:,} > 40,000)")
        checks_passed += 1
    else:
        print(f"    [FAIL] Row count check ({row_count:,} <= 40,000)")
        errors.append(f"Insufficient row count: {row_count}")

    # Check 4: Positive values check
    if (df['total_amount'] > 0).all() and (df['quantity'] > 0).all():
        print("    [PASS] Positive values check")
        checks_passed += 1
    else:
        print("    [FAIL] Positive values check")
        errors.append("Negative or zero values found in amount/quantity")

    # Check 5: Date range check (2021-2024)
    try:
        # Avoid overriding the dataframe column just in case
        dates = pd.to_datetime(df['order_date'])
        years = dates.dt.year
        if years.between(2021, 2024).all():
            print("    [PASS] Date range check")
            checks_passed += 1
        else:
            print("    [FAIL] Date range check")
            errors.append("Dates outside 2021-2024 range")
    except Exception as e:
        print("    [FAIL] Date range check (Parsing error)")
        errors.append("Invalid date formats")

    print(f"  Quality Score: {checks_passed}/5 checks passed")
    
    if checks_passed == 5:
        # Move to processed
        copy_source = {'Bucket': bucket_name, 'Key': file_key}
        s3_client.copy_object(CopySource=copy_source, Bucket=bucket_name, Key="processed/pharma_sales_clean.csv")
        s3_client.delete_object(Bucket=bucket_name, Key=file_key)
        print("[ROUTE]    All checks passed. File moved to processed/ folder.")
        return True
    else:
        # Move to logs
        copy_source = {'Bucket': bucket_name, 'Key': file_key}
        s3_client.copy_object(CopySource=copy_source, Bucket=bucket_name, Key="logs/pharma_sales_clean.csv")
        s3_client.delete_object(Bucket=bucket_name, Key=file_key)
        
        error_report = "\n".join(errors)
        s3_client.put_object(Bucket=bucket_name, Key="logs/error_report.txt", Body=error_report.encode('utf-8'))
        print(f"[ROUTE]    Checks failed. File moved to logs/ folder. Reasons: {', '.join(errors)}")
        return False

if __name__ == "__main__":
    import importlib
    import sys
    import os
    
    # Add parent directory to path to allow import
    sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    
    # In a standalone run, Moto's @mock_aws on validate_and_route starts a new empty mock environment!
    # So the bucket and file won't exist because setup_s3 ran in its own mock context and exited.
    # To run this standalone, we'd need them to share the mock context.
    # Therefore, standalone testing is better done via the pipeline_runner script.
    print("Run via 04_pipeline_runner.py to share the S3 mock state.")
