
from utils.cloud_storage import GCPStorage

if __name__ == "__main__":
    storage_ob = GCPStorage()
    if not storage_ob.get_credentials():
        print("Exiting as authentication failed.")
    else:
        BUCKET_NAME = 'hello_world_bucket24_saurabh'
        storage_ob.create_bucket(bucket_name=BUCKET_NAME)
        print()
        storage_ob.list_buckets()
