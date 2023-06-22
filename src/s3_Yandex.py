import boto3

from config import YANDEX_ID, YANDEX_KEY, YANDEX_REGION

file_bucket = 'file-bucket-for-backend-practice'
os = boto3.client(
    's3',
    aws_access_key_id=YANDEX_ID,
    aws_secret_access_key=YANDEX_KEY,
    region_name=YANDEX_REGION,
    endpoint_url='https://storage.yandexcloud.net'
)


def upload(file, object_name):
    os.upload_fileobj(file, file_bucket, object_name)


def download(file_name, object_name):
    os.download_file(file_bucket, file_name, object_name)


def get_object(path):
    get_object_response = os.get_object(Bucket=file_bucket, Key=path)
    return get_object_response['Body'].read()


def delete(bucket_name, object_name):
    os.delete_object(Bucket=bucket_name, Key=object_name)


print(get_object('download/{}'.format('Направления.pdf')))