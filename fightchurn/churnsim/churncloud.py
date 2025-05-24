import boto3
import fnmatch
import glob
import os

from botocore.exceptions import ClientError
from urllib.parse import urlparse

def upload_files_to_cloud_storage(local_directory, s3_uri, file_pattern, s3_prefix=''):
    """
    Copies files from a local directory to an S3 bucket if their names match a given pattern.

    Args:
        local_directory (str): The path to the local directory containing the files.
        bucket_name (str): The name of the S3 bucket to upload to.
        file_pattern (str): The Unix shell-style wildcard pattern (e.g., '*.txt', 'data_*.csv').
        s3_prefix (str, optional): The S3 prefix (folder path) where the files should be uploaded.
                                    Defaults to an empty string (root of the bucket).
    """
    s3_client = boto3.client('s3')

    parsed_uri = urlparse(s3_uri)
    if parsed_uri.scheme != 's3':
        raise ValueError(f"Invalid S3 URI scheme: {parsed_uri.scheme}. Expected 's3://'")
    bucket_name = parsed_uri.netloc
    s3_object_key = parsed_uri.path.lstrip('/')  # Remove leading slash if present
    if not bucket_name:
        raise ValueError("S3 URI must specify a bucket name (e.g., 's3://my-bucket/')")

    uploaded_count = 0

    print(f"Scanning local directory: {local_directory}")
    print(f"Looking for files matching pattern: '{file_pattern}'")

    try:
        for entry_name in os.listdir(local_directory):
            if fnmatch.fnmatch(entry_name, file_pattern):
                local_file_path = os.path.join(local_directory, entry_name)
                s3_object_key = os.path.join(s3_prefix, entry_name).replace(os.sep, '/')
                print(f"Uploading '{local_file_path}' to 's3://{bucket_name}/{s3_object_key}'...")
                s3_client.upload_file(local_file_path, bucket_name, s3_object_key)
                print(f"Successfully uploaded: {entry_name}")
                uploaded_count += 1
    except Exception as e:
        print(f"An error occurred: {e}")

    print(f"\nFinished. Uploaded {uploaded_count} files matching the pattern {file_pattern}")


def download_cloud_file_if_exists(s3_file_path, local_file_path):
    """
    Downloads a file from an S3 bucket to a local path if it exists.

    Args:
        bucket_name (str): The name of the S3 bucket.
        s3_file_key (str): The full path (key) of the file in the S3 bucket.
        local_file_path (str): The local path where the file should be saved.

    Returns:
        str or None: The local_file_path if the file was downloaded successfully,
                     None if the file does not exist in the S3 bucket.
                     Raises other ClientError exceptions for other issues.
    """
    s3_client = boto3.client('s3')

    parsed_uri = urlparse(s3_file_path)

    if parsed_uri.scheme != 's3':
        raise ValueError(f"Invalid S3 URI scheme: Expected 's3', got '{parsed_uri.scheme}'")
    if not parsed_uri.netloc:
        raise ValueError("Invalid S3 URI: Bucket name is missing.")

    bucket_name = parsed_uri.netloc
    # The path will have a leading '/', so we remove it
    object_key = parsed_uri.path.lstrip('/')

    try:
        # First, check if the file exists using head_object
        s3_client.head_object(Bucket=bucket_name, Key=object_key)

        # If head_object doesn't raise a 404, the file exists, so proceed to download
        s3_client.download_file(bucket_name, object_key, local_file_path)
        print(f"Successfully downloaded '{object_key}' to '{local_file_path}'")
        return local_file_path

    except ClientError as e:
        error_code = e.response['Error']['Code']
        if error_code == '404':
            print(f"File '{object_key}' does not exist in bucket '{bucket_name}'.")
            return None  # File not found
        else:
            # Handle other AWS-related errors (e.g., permissions, invalid bucket name)
            print(f"An AWS error occurred while trying to download '{object_key}': {e}")
            raise  # Re-raise the exception for other critical errors
    except Exception as e:
        # Handle other potential errors (e.g., local file system issues)
        print(f"An unexpected error occurred: {e}")
        raise


def convert_csvs_to_parquet(pattern:str, column_names:list[str], force:bool=False):
    """
    Convert all CSV files matching the given regex pattern to Parquet format,
    but only if a corresponding Parquet file doesn't already exist.
    Assumes CSV files have no headers.

    Args:
        pattern (str): Regular expression pattern to match CSV files
    """
    # Find all CSV files matching the pattern
    csv_files = []
    for file in glob.glob(pattern):
        csv_files.append(file)

    if not csv_files:
        print(f"No CSV files found matching pattern: {pattern}")
        return

    # Process each matching CSV file
    for csv_file in csv_files:
        # Define the expected Parquet file name
        parquet_file = os.path.splitext(csv_file)[0] + ".parquet"

        # Skip if Parquet file already exists
        if os.path.exists(parquet_file) and not force:
            continue

        # Convert CSV to Parquet
        try:
            # Read CSV without header
            df = pd.read_csv(csv_file, header=None, names=column_names)

            # Write to Parquet
            df.to_parquet(parquet_file, engine='pyarrow',
                            index=False,
                            compression='snappy' )
            print(f"Successfully converted {csv_file} to {parquet_file}")

        except Exception as e:
            print(f"Error converting {csv_file}: {str(e)}")
