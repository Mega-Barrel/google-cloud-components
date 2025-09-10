
from utils.cloud_storage import GCPStorage

if __name__ == "__main__":
    storage_ob = GCPStorage()
    if not storage_ob.get_credentials():
        print("Exiting as authentication failed.")
    else:
        # BUCKET_NAME = f"{storage_ob.get_project_id()}-test-bucket-example"
        BUCKET_NAME = "udemy-cource"
        storage_ob.list_blobs(bucket_name=BUCKET_NAME)
        # storage_ob.create_blob(bucket_name=BUCKET_NAME, source_file_name='packsges.txt', destination_blob_name="packsges.txt")

        # print(storage_ob.get_bucket(bucket_name=BUCKET_NAME))
        # storage_ob.create_bucket(bucket_name=BUCKET_NAME)
        # storage_ob.list_buckets()
        # print(storage_ob.get_bucket(bucket_name=BUCKET_NAME))