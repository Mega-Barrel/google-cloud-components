
from google.cloud import storage
from utils.auth import GCPAuth

class GCPStorage(GCPAuth):
    """
    Base class for Google CLoud Storage operations.
    It inherits GCPAuth to get authentication credentials
    """
    def __init__(self):
        """
        Initializes the storage class
        """
        # Call the parent class's constructor to handle authentication
        super().__init__()

        if self.get_credentials():
            self.storage_client = storage.Client(
                credentials = self.get_credentials(),
                project = self.get_project_id()
            )
            print("Storage client created successfully.")
        else:
            self.storage_client = None

    def create_bucket(self, bucket_name: str):
        """
        Create a new bucket in the Mumbai [Asia] region
        Documentation: https://cloud.google.com/storage/docs/creating-buckets

        Args:
            bucket_name (str): The name of bucket.
        """
        if not self.storage_client:
            return
        print(f"\nCreating bucket '{bucket_name}'...")
        try:
            bucket = self.storage_client.bucket(bucket_name)
            bucket.storage_class = "STANDARD"
            bucket.location = "ASIA-SOUTH1"
            bucket.create()
            print(
                f"Created bucket {bucket.name} in {bucket.location} with storage class {bucket.storage_class}"
            )
        except Exception as e:
            print(f"Failed to create bucket '{bucket_name}': {e}")

    def list_buckets(self):
        """
        Lists all buckets in the authenticated project.
        Documentation: https://cloud.google.com/storage/docs/listing-buckets
        """
        if not self.storage_client:
            print("Cannot list buckets. Authentication failed.")
            return

        print("\nListing buckets in the project:")
        try:
            buckets = self.storage_client.list_buckets()
            for bucket in buckets:
                print(f"- {bucket.name}")
        except Exception as e:
            print(f"An error occurred while listing buckets: {e}")

    def list_objects(self, bucket_name: str):
        """
        Lists all objects present inside bucket
        """
        if not self.storage_client:
            print("Cannot list buckets. Authentication failed.")
            return
        try:
            blobs = self.storage_client.list_blobs(bucket_name)
            print(blobs.num_results)
            print(blobs.__sizeof__())
            print(blobs.max_results)

            #     for blob in blobs:
            #         print(f"    - {blob.name}")
        except Exception as e:
            print(f"An error occurred while listing buckets: {e}")

    def read_blob(self):
        """
        Read the specified object
        """
        pass

    def get_bucket(self, bucket_name=None):
        """
        Return the specified bucket
        Documentation: https://cloud.google.com/storage/docs/bucket-metadata
        """
        if not self.storage_client:
            print("Cannot list buckets. Authentication failed.")
            return
        if not bucket_name:
            print("Bucket Name cannnot be empty")
        else:
            bucket = self.storage_client.get_bucket(bucket_name)
            return f"Fetched bucket: {bucket.name}, location: {bucket.location}, time created: {bucket.time_created}"
