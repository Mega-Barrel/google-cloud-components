
from google_cloud_components.cloud_storage import GCPStorage

if __name__ == "__main__":
    storage_ob = GCPStorage()
    if not storage_ob.get_credentials():
        print("Exiting as authentication failed.")
    else:
        BUCKET_NAME = "udemy-cource"
        storage_ob.list_blobs(bucket_name=BUCKET_NAME)
        # bucket_metadata = storage_ob.get_bucket_metadata(bucket_name=BUCKET_NAME)
        # print(bucket_metadata)

        blob_metadata = storage_ob.get_blob_metadata(bucket_name=BUCKET_NAME, blob_name='csv/2019-04-27.csv')
        print(blob_metadata)
