
# import os
# from google.oauth2 import service_account

# class GCPAuth:
#     """
#     Base class for authenticating with Google Cloud Platform APIs.
#     It uses 'credentials.json' file for service account authentication.
#     """
#     def __init__(self, credentials_path = 'credentials.json'):
#         """
#         Initializes the credentials and project ID.
        
#         Args:
#             credentials_path (str): The path to the credentials.json file.
#         """
#         self.__credentials = None
#         self.__project_id = None

#         # Attempt to load credentials from the specified JSON file
#         if os.path.exists(credentials_path):
#             try:
#                 self.__credentials = service_account.Credentials.from_service_account_file(credentials_path)
#                 print(f"Successfully authenticated using {credentials_path}")
#                 # Get the project ID from the credentials
#                 self.__project_id = self.__credentials.project_id
#             except Exception as e:
#                 print(f"Failed to load credentials from {credentials_path}: {e}")

#     def get_credentials(self):
#         """
#         Returns the authenticated credentials object.
#         """
#         return self.__credentials

#     def get_project_id(self):
#         """
#         Returns the project ID associated with the credentials.
#         """
#         return self.__project_id

import os

from google.oauth2 import service_account
from google.auth.exceptions import DefaultCredentialsError

class GCPAuth:
    """
    Base class for authenticating with Google Cloud Platform APIs.
    It uses a service account JSON file for authentication.
    """
    def __init__(self, credentials_path='credentials.json'):
        """
        Initializes the credentials and project ID.
        
        This method attempts to load authentication credentials from the specified
        JSON file. It includes proper exception handling to catch common errors
        such as the file not being found or issues with the credential format.

        Args:
            credentials_path (str): The path to the service account credentials JSON file.
        """
        self.__credentials = None
        self.__project_id = None

        # Attempt to load credentials from the specified JSON file
        try:
            if not os.path.exists(credentials_path):
                raise FileNotFoundError(f"Credentials file not found at: {credentials_path}")

            self.__credentials = service_account.Credentials.from_service_account_file(credentials_path)

            # Get the project ID from the credentials
            if self.__credentials.project_id:
                self.__project_id = self.__credentials.project_id
                print(f"Successfully authenticated with project ID: {self.__project_id}")
            else:
                # Handle cases where project_id might be missing from the credentials file
                raise ValueError("Project ID not found in the credentials file.")

        except FileNotFoundError as e:
            print(f"Authentication failed: {e}")
            print("Please ensure 'credentials.json' is in the root directory.")
        except ValueError as e:
            print(f"Authentication failed: {e}")
            print("The credentials file is invalid. Please check the file content.")
        except DefaultCredentialsError as e:
            print(f"Authentication failed: {e}")
            print("Failed to get default credentials. Ensure you have authenticated using 'gcloud auth application-default login' or that the credentials file is valid.")
        except Exception as e:
            print(f"An unexpected error occurred during authentication: {e}")

    def get_credentials(self):
        """
        Returns the loaded Google Cloud credentials.

        Returns:
            google.oauth2.credentials.Credentials: The credentials object or None if authentication failed.
        """
        return self.__credentials

    def get_project_id(self):
        """
        Returns the project ID from the loaded credentials.

        Returns:
            str: The project ID or None if not available.
        """
        return self.__project_id

if __name__ == "__main__":
    GCPInstance = GCPAuth()
    print(GCPInstance.get_credentials())
    print(GCPInstance.get_project_id())
