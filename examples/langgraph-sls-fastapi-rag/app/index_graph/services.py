from io import StringIO
from typing import Any, Dict, List

import boto3
import pandas as pd


class S3CSVReader:
    """Service to read and parse CSV files from an S3 directory."""
    
    def __init__(self, bucket_name: str, prefix: str):
        """
        Initialize the S3 CSV reader.
        
        Args:
            bucket_name (str): Name of the S3 bucket
            prefix (str): Directory prefix in the S3 bucket
        """
        self.s3_client = boto3.client('s3')
        self.bucket_name = bucket_name
        self.prefix = prefix

    def list_csv_files(self) -> List[str]:
        """
        List all CSV files in the specified S3 directory.
        
        Returns:
            List[str]: List of CSV file keys
        """
        response = self.s3_client.list_objects_v2(
            Bucket=self.bucket_name,
            # Prefix=self.prefix
        )
        
        csv_files = []
        if 'Contents' in response:
            for obj in response['Contents']:
                if obj['Key'].endswith('.csv'):
                    csv_files.append(obj['Key'])
        
        return csv_files

    def read_csv_file(self, file_key: str) -> List[Dict[str, Any]]:
        """
        Read and parse a single CSV file from S3.
        
        Args:
            file_key (str): S3 key of the CSV file
            
        Returns:
            List[Dict[str, Any]]: List of dictionaries containing the CSV data
        """
        try:
            response = self.s3_client.get_object(
                Bucket=self.bucket_name,
                Key=file_key
            )
            
            csv_content = response['Body'].read().decode('utf-8')
            df = pd.read_csv(StringIO(csv_content))
            return df.to_dict('records')
            
        except Exception as e:
            print(f"Error reading file {file_key}: {str(e)}")

    def read_all_csv_files(self) -> List[Dict[str, Any]]:
        """
        Read and parse all CSV files in the specified S3 directory.
        
        Returns:
            List[Dict[str, Any]]: Combined list of dictionaries containing all CSV data
        """
        all_records = []
        csv_files = self.list_csv_files()
        
        for file_key in csv_files:
            records = self.read_csv_file(file_key)
            all_records.extend(records)
            
        return all_records
