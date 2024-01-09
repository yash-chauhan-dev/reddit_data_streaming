from utils.constants import AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY_ID
import s3fs
import time


def connect_to_s3():
    try:
        s3 = s3fs.S3FileSystem(
            anon=False,
            key=AWS_ACCESS_KEY_ID,
            secret=AWS_SECRET_ACCESS_KEY_ID,
            client_kwargs={"region_name": "ap-south-1"},
        )
        return s3
    except Exception as e:
        print(e)


def create_bucket_if_not_exist(s3: s3fs.S3FileSystem, bucket: str, max_retries=5):
    for attempt in range(max_retries):
        try:
            if not s3.exists(bucket):
                s3.mkdir(bucket)
                print("Bucket created")
                break  # Exit the loop if successful
            else:
                print("Bucket already exists")
                break
        except Exception as e:
            print(f"Error creating bucket (attempt {attempt+1}/{max_retries}): {e}")
            if attempt < max_retries - 1:
                time.sleep(60)  # Wait for 60 seconds before retrying
    else:
        raise RuntimeError("Failed to create bucket after multiple attempts")


def upload_to_s3(s3: s3fs.S3FileSystem, file_path: str, bucket: str, s3_file_name: str):
    try:
        s3.put(file_path, bucket + "/raw/" + s3_file_name)
        print("File uploaded to s3")
    except FileNotFoundError:
        print("The file was not found")
