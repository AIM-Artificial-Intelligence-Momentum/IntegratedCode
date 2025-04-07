from azure.storage.blob import BlobServiceClient
import os
from dotenv import load_dotenv

class AzureBlobStorage:
    def __init__(self):
        # .env에서 불러오기
        load_dotenv()

        self.blob_connection_str = os.getenv("BLOB_CONNECTION_STRING")
        self.blob_service_client = BlobServiceClient.from_connection_string(self.blob_connection_str)

    def upload_file(self, container_name: str, file_path: str):
        """Azure Blob Storage에 파일 업로드"""
        container_client = self.blob_service_client.get_container_client(container_name)
        blob_name = os.path.basename(file_path)
        with open(file_path, "rb") as data:
            container_client.upload_blob(blob_name, data)
        return f"File {blob_name} uploaded to {container_name}"

    def download_file(self, container_name: str, blob_name: str, download_path: str):
        """Azure Blob Storage에서 파일 다운로드"""
        container_client = self.blob_service_client.get_container_client(container_name)
        blob_client = container_client.get_blob_client(blob_name)
        with open(download_path, "wb") as download_file:
            download_file.write(blob_client.download_blob().readall())
        return f"File {blob_name} downloaded to {download_path}"
