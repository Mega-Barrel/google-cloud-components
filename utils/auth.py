
import os
from google.oauth2 import service_account

class GCPAuth:
    """
    Base class for authenticating with Google Cloud Platform APIs.
    It uses 'credentials.json' file for service account authentication.
    """
    def __init__(self, credentials_path = 'credentials.json'):
        """
        Initializes the credentials and project ID.
        
        Args:
            credentials_path (str): The path to the credentials.json file.
        """
        self.credentials = None
        self.project_id = None

        # Attempt to load credentials from the specified JSON file
        if os.path.exists(credentials_path):
            try:
                self.credentials = service_account.Credentials.from_service_account_file(credentials_path)
                print(f"Successfully authenticated using {credentials_path}")
                # Get the project ID from the credentials
                self.project_id = self.credentials.project_id
            except Exception as e:
                print(f"Failed to load credentials from {credentials_path}: {e}")

    def get_credentials(self):
        """
        Returns the authenticated credentials object.
        """
        return self.credentials

    def get_project_id(self):
        """
        Returns the project ID associated with the credentials.
        """
        return self.project_id

if __name__ == "__main__":
    GCPInstance = GCPAuth()
    print(GCPInstance.get_credentials())
    print(GCPInstance.get_project_id())
