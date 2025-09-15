""" Entry point for google_cloud_components package"""
import json
from google_cloud_components.cloud_storage import GCPStorage

if __name__ == "__main__":
    storage_ob = GCPStorage()
    if not storage_ob.get_credentials():
        print("Exiting as authentication failed.")
    else:
        BUCKET_NAME = "udemy-cource"
        BLOB_NAME = "json/2019-04-28.json"

        # storage_ob.list_blobs(bucket_name=BUCKET_NAME)
        # json_data = storage_ob.read_blob_content(bucket_name=BUCKET_NAME, blob_name=BLOB_NAME)

        # parsed_data = []
        # for line in json_data.strip().splitlines():
        #     if line:
        #         try:
        #             parsed_data.append(json.loads(line))
        #         except json.JSONDecodeError as e:
        #             # Continue to the next line to process the rest of the file
        #             pass
        # # Return the list of parsed JSON objects.
        # print(type(json_data))
        # print(parsed_data)
