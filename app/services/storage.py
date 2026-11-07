import aioboto3
from botocore.exceptions import ClientError
from config import settings


class MinIOService:
    def __init__(self):
        self.endpoint = settings.MINIO_ENDPOINT
        self.access_key = settings.MINIO_ACCESS_KEY
        self.secret_key = settings.MINIO_SECRET_KEY
        self.bucket = settings.MINIO_BUCKET
        self._session = aioboto3.Session()

    def _client(self):
        return self._session.client(
            "s3",
            endpoint_url=f'http://{self.endpoint}',
            aws_access_key_id=self.access_key,
            aws_secret_access_key=self.secret_key,
            use_ssl=False,
        )

    async def ensure_bucket(self):
        async with self._client() as s3:
            try:
                await s3.head_bucket(Bucket=self.bucket)
            except ClientError as e:
                error_code = e.response["Error"]["Code"]
                if error_code in ("404", "NoSuchBucket"):
                    await s3.create_bucket(Bucket=self.bucket)
                else:
                    raise

    async def upload_file(self, data:bytes, key:str, content_type:str="application/octet-stream")->str:
        async with self._client() as s3:
            await s3.put_object(Bucket=self.bucket, Key=key, Body=data, ContentType=content_type)
        return key

    async def delete_file(self, key:str)->None:
        async with self._client() as s3:
            await s3.delete_object(Bucket=self.bucket, Key=key)

    async def generate_presigned_url(self, key:str, expiration:int=3600)->str:
        async with self._client() as s3:
            return await s3.generate_presigned_url(
                "get_object",
                Params={"Bucket":self.bucket, "Key":key},
                ExpiresIn=expiration,
            )