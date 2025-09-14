
from google.cloud.exceptions import NotFound
from google.cloud import storage
from google_cloud_components.auth import GCPAuth

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

    def get_bucket_metadata(self, bucket_name=None):
        """
        Return a formatted string with all specified bucket properties.
        Documentation: https://cloud.google.com/storage/docs/bucket-metadata
        """
        if not self.storage_client:
            return "Authentication failed."
        if not bucket_name:
            return "Bucket Name cannnot be empty"
        try:
            bucket = self.storage_client.get_bucket(bucket_name)
            return self._format_bucket_details(bucket)
        except NotFound:
            return f"Bucket '{bucket_name}' not found."
        except Exception as e:
            return f"An error occurred while getting the bucket: {e}"

    def _format_bucket_details(self, bucket):
        """Helper method to format bucket details into a single string."""
        public_access_prevention = "N/A"
        if bucket.iam_configuration:
            public_access_prevention = bucket.iam_configuration.public_access_prevention

        return {
            "id": bucket.id,
            "name": bucket.name,
            "storage_class": bucket.storage_class,
            "location": bucket.location,
            "location_type": bucket.location_type,
            "cors": bucket.cors,
            "default_event_based_hold": bucket.default_event_based_hold,
            "default_kms_key_name": bucket.default_kms_key_name,
            "metageneration": bucket.metageneration,
            "public_access_prevention": public_access_prevention,
            "retention_effective_time": str(bucket.retention_policy_effective_time),
            "retention_period": bucket.retention_period,
            "retention_policy_locked": bucket.retention_policy_locked,
            "object_retention_mode": bucket.object_retention_mode,
            "requester_pays": bucket.requester_pays,
            "self_link": bucket.self_link,
            "time_created": str(bucket.time_created),
            "versioning_enabled": bucket.versioning_enabled,
            "labels": bucket.labels
        }

    def create_bucket(
        self,
        bucket_name: str,
        location: str = "ASIA-SOUTH1",
        storage_class: str = "STANDARD"
    ):
        """
        Create a new bucket with optional location and storage class.

        Args:
            bucket_name (str): The name of the bucket.
            location (str, optional): The location for the bucket. Defaults to "ASIA-SOUTH1".
            storage_class (str, optional): The storage class for the bucket. Defaults to "STANDARD".
        """
        if not self.storage_client:
            print("Storage client is not initialized.")
            return

        print(f"\nCreating bucket '{bucket_name}'...")
        try:
            bucket = self.storage_client.bucket(bucket_name)

            # Set location and storage-class
            bucket.location = location
            bucket.storage_class = storage_class

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
            print("Authentication failed.")
            return

        print("\nListing buckets in the project:")
        try:
            buckets = self.storage_client.list_buckets()
            for bucket in buckets:
                print(f"- {bucket.name}")
        except Exception as e:
            print(f"An error occurred while listing buckets: {e}")

    def delete_bucket(self, bucket_name):
        """Deletes an empty bucket."""
        if not self.storage_client:
            print("Authentication failed.")
            return

        print(f"\nDeleting bucket '{bucket_name}'...")
        try:
            bucket = self.storage_client.bucket(bucket_name)
            bucket.delete()
            print(f"Bucket '{bucket_name}' deleted successfully.")
        except NotFound:
            print(f"Bucket '{bucket_name}' not found.")
        except Exception as e:
            print(f"Failed to delete bucket '{bucket_name}': {e}")
            print("Note: Bucket must be empty to be deleted.")

    def create_blob(self, bucket_name, source_file_name, destination_blob_name):
        """Uploads a file to the specified bucket."""
        if not self.storage_client:
            print("Authentication failed.")
            return

        print(f"\nUploading '{source_file_name}' to '{destination_blob_name}' in bucket '{bucket_name}'...")
        try:
            bucket = self.storage_client.bucket(bucket_name)
            blob = bucket.blob(destination_blob_name)
            blob.upload_from_filename(source_file_name)
            print(f"File '{source_file_name}' uploaded successfully.")
        except NotFound:
            print(f"Bucket '{bucket_name}' not found.")
        except Exception as e:
            print(f"An error occurred while uploading: {e}")

    def list_blobs(self, bucket_name: str):
        """
        Lists all objects present inside a bucket.

        This method first checks if the bucket contains any objects. If it's
        not empty, it groups the blobs by their top-level directory (based on
        the '/' delimiter in their names) and prints them in a structured format.

        Documentation: https://cloud.google.com/storage/docs/listing-objects
        
        Args:
            bucket_name (str): The name of the bucket to list blobs from.
        """
        if not self.storage_client:
            print("Authentication failed.")
            return

        print(f"\nListing objects in bucket '{bucket_name}':")
        try:
            blobs_iterator = self.storage_client.list_blobs(bucket_name)
            blobs_list = list(blobs_iterator)

            if not blobs_list:
                print(f"Bucket '{bucket_name}' is empty.")
                return

            # Group blobs by their top-level directory
            structured_list = {}
            for blob in blobs_list:
                parts = blob.name.split('/', 1)
                prefix = parts[0]
                if len(parts) == 1:
                    # This is a file at the root of the bucket
                    if '/' not in structured_list:
                        structured_list['/'] = []
                    structured_list['/'].append(prefix)
                else:
                    # This is a file within a 'directory'
                    if prefix not in structured_list:
                        structured_list[prefix] = []
                    structured_list[prefix].append(parts[1])

            # Print the structured output
            for prefix, files in structured_list.items():
                if prefix == '/':
                    for file_name in files:
                        print(f"- {file_name}")
                else:
                    print(f"{prefix} Folder:")
                    for file_name in files:
                        print(f"    - {file_name}")

        except NotFound:
            print(f"Bucket '{bucket_name}' not found.")
        except Exception as e:
            print(f"An error occurred while listing blobs: {e}")

    def delete_blob(self, bucket_name, blob_name):
        """Deletes a blob from the bucket."""
        if not self.storage_client:
            print("Authentication failed.")
            return

        print(f"\nDeleting blob '{blob_name}' from bucket '{bucket_name}'...")
        try:
            bucket = self.storage_client.bucket(bucket_name)
            blob = bucket.blob(blob_name)
            blob.delete()
            print(f"Blob '{blob_name}' deleted successfully.")
        except NotFound:
            print(f"Blob '{blob_name}' not found in bucket '{bucket_name}'.")
        except Exception as e:
            print(f"An error occurred while deleting: {e}")

    def get_blob_metadata(self, bucket_name: str = None, blob_name: str = None):
        """
        Return a formatted dictionary with all Blob properties.
        Documentation: https://cloud.google.com/storage/docs/metadata

        Args:
            bucket_name (str): The name of the bucket.
            blob_name (str): The name of the blob.
        """
        if not self.storage_client:
            return "Authentication failed."
        if not bucket_name:
            return "Bucket Name cannot be empty."
        if not blob_name:
            return "Blob Name cannot be empty."
        try:
            bucket = self.storage_client.get_bucket(bucket_name)
            blob = bucket.get_blob(blob_name)
            if blob is None:
                return f"The blob '{blob_name}' does not exist in bucket '{bucket_name}'."
            return self._format_blob_details(blob)

        except NotFound as e:
            return f"Either the bucket '{bucket_name}' or blob '{blob_name}' does not exist: {e}"
        except Exception as e:
            return f"An unexpected error occurred while getting the blob: {e}"

    def _format_blob_details(self, blob):
        """Helper method to get blob metadata"""
        return {
            "id": blob.id,
            "name": blob.name,
            "bucket": blob.bucket.name,
            "storage_class": blob.storage_class,
            "size": f"{blob.size} bytes",
            "updated": blob.updated,
            "generation": blob.generation,
            "metageneration": blob.metageneration,
            "etag": blob.etag,
            "owner": blob.owner,
            "component_count": blob.component_count,
            "crc32c": blob.crc32c,
            "md5_hash": blob.md5_hash,
            "cache_control": blob.cache_control,
            "content_type": blob.content_type,
            "content_disposition": blob.content_disposition,
            "content_encoding": blob.content_encoding,
            "content_language": blob.content_language,
            "metadata": blob.metadata,
            "media_link": blob.media_link,
            "custom_time": str(blob.custom_time) if blob.custom_time else None,
            "temporary_hold": "enabled" if blob.temporary_hold else "disabled",
            "event_based_hold": "enabled" if blob.event_based_hold else "disabled",
            "retention_mode": blob.retention.mode if blob.retention else None,
            "retention_retain_until_time": blob.retention.retain_until_time if blob.retention else None,
        }
