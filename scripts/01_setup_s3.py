import os
import boto3
import pandas as pd
from moto import mock_aws

@mock_aws
def setup_s3():
    print("============================================================")
    print("  PHARMA PIPELINE - S3 SETUP")
    print("============================================================")
    
    bucket_name = "pharma-sales-pipeline"
    print(f"[CREATE]  Creating S3 bucket: {bucket_name}")
    
    # Initialize S3 client (region must be specified for moto to work properly)
    s3_client = boto3.client('s3', region_name='us-east-1')
    
    # Create the bucket
    s3_client.create_bucket(Bucket=bucket_name)
    print("[SUCCESS] Bucket created")
    
    # Create folder structure
    # In S3, folders are just prefixes, but we can create empty objects ending in '/'
    # to simulate folders if needed. Often just uploading the file with the prefix is enough,
    # but to strictly "create folder structure" we can put empty objects.
    folders = ['raw/', 'processed/', 'output/', 'logs/']
    for folder in folders:
        s3_client.put_object(Bucket=bucket_name, Key=folder)
        
    file_path = "data/pharma_sales_clean.csv"
    print(f"[UPLOAD]  Uploading pharma_sales_clean.csv -> raw/")
    
    try:
        if os.path.exists(file_path):
            df = pd.read_csv(file_path)
            record_count = len(df)
            
            s3_client.upload_file(file_path, bucket_name, "raw/pharma_sales_clean.csv")
            print(f"[SUCCESS] File uploaded ({record_count:,} records)")
        else:
            print(f"[ERROR]   File not found: {file_path}")
            
    except Exception as e:
        print(f"[ERROR]   Upload failed: {e}")

    print("[INFO]    Folder structure:")
    print("            raw/       <- raw uploads")
    print("            processed/ <- validated files")
    print("            output/    <- query results")
    print("            logs/      <- error reports")
    print("============================================================")

if __name__ == "__main__":
    setup_s3()
