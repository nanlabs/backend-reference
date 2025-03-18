import base64
import json
from typing import Optional, Union

import boto3
from botocore.exceptions import ClientError


class SecretContext:
    def __init__(self, secret_name: str, region_name: str):
        self.secret_name = secret_name
        self.region_name = region_name


class SecretsResolver:
    secret_cache: dict[str, Union[str, bytes]] = {}

    def get_secret_key(
        self,
        key: str,
        context: SecretContext,
        default: Optional[str] = None,
        json_decode: bool = True,
    ) -> Optional[Union[str, bytes]]:
        secret = self.get_secret(secret_name=context.secret_name, region_name=context.region_name)
        if not secret:
            return default
        if json_decode:
            secret = json.loads(secret)
        if isinstance(secret, dict):
            return secret.get(key, default)
        return default

    def get_secret(self, secret_name: str, region_name: str) -> Union[str, bytes]:
        if secret_name in self.secret_cache:
            return self.secret_cache[secret_name]

        session = boto3.session.Session()
        client = session.client(service_name="secretsmanager", region_name=region_name)

        try:
            response = client.get_secret_value(SecretId=secret_name)
        except ClientError as e:
            raise e
        secret = response.get("SecretString", None)
        if secret:
            self.secret_cache[secret_name] = secret
            return secret
        decoded_binary_secret = base64.b64decode(response["SecretBinary"])
        self.secret_cache[secret_name] = decoded_binary_secret
        return decoded_binary_secret
