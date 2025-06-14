from enum import Enum
import base64
import binascii
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad

from doraSpider.types.format import Format


class AESCipher:
    @staticmethod
    def _encode(data: bytes, fmt: Format) -> str:
        if fmt == Format.BASE64:
            return base64.b64encode(data).decode("utf-8")
        elif fmt == Format.HEX:
            return binascii.hexlify(data).decode("utf-8")
        else:
            raise ValueError("Invalid output format.")

    @staticmethod
    def _decode(data: str, fmt: Format) -> bytes:
        if fmt == Format.BASE64:
            return base64.b64decode(data)
        elif fmt == Format.HEX:
            return binascii.unhexlify(data)
        else:
            raise ValueError("Invalid input format.")

    @staticmethod
    def aes_ecb_encrypt(key: str, plain_text: str, output_format: Format = Format.BASE64) -> str:
        """
        aes-ecb 加密
        :param key:
        :param plain_text:
        :param output_format:
        :return:
        """
        key_bytes = key.encode("utf-8")
        data = plain_text.encode("utf-8")

        if len(key_bytes) not in [16, 24, 32]:
            raise ValueError("Key must be 16, 24, or 32 bytes.")

        cipher = AES.new(key_bytes, AES.MODE_ECB)
        encrypted = cipher.encrypt(pad(data, AES.block_size))
        return AESCipher._encode(encrypted, output_format)

    @staticmethod
    def aes_ecb_decrypt(key: str, cipher_text: str, input_format: Format = Format.BASE64) -> str:
        """
        aes-ecb 解密
        :param key:
        :param cipher_text:
        :param input_format:
        :return:
        """
        key_bytes = key.encode("utf-8")
        encrypted = AESCipher._decode(cipher_text, input_format)

        if len(key_bytes) not in [16, 24, 32]:
            raise ValueError("Key must be 16, 24, or 32 bytes.")

        cipher = AES.new(key_bytes, AES.MODE_ECB)
        decrypted = unpad(cipher.decrypt(encrypted), AES.block_size)
        return decrypted.decode("utf-8")

    @staticmethod
    def aes_cbc_encrypt(key: str, iv: str, plain_text: str, output_format: Format = Format.BASE64) -> str:
        """
        aes-cbc 加密
        :param key:
        :param iv:
        :param plain_text:
        :param output_format:
        :return:
        """
        key_bytes = key.encode("utf-8")
        iv_bytes = iv.encode("utf-8")
        data = plain_text.encode("utf-8")

        if len(key_bytes) not in [16, 24, 32]:
            raise ValueError("Key must be 16, 24, or 32 bytes.")
        if len(iv_bytes) != 16:
            raise ValueError("IV must be 16 bytes.")

        cipher = AES.new(key_bytes, AES.MODE_CBC, iv_bytes)
        encrypted = cipher.encrypt(pad(data, AES.block_size))
        return AESCipher._encode(encrypted, output_format)

    @staticmethod
    def aes_cbc_decrypt(key: str, iv: str, cipher_text: str, input_format: Format = Format.BASE64) -> str:
        """
        aes-cbc 解密
        :param key:
        :param iv:
        :param cipher_text:
        :param input_format:
        :return:
        """
        key_bytes = key.encode("utf-8")
        iv_bytes = iv.encode("utf-8")
        encrypted = AESCipher._decode(cipher_text, input_format)

        if len(key_bytes) not in [16, 24, 32]:
            raise ValueError("Key must be 16, 24, or 32 bytes.")
        if len(iv_bytes) != 16:
            raise ValueError("IV must be 16 bytes.")

        cipher = AES.new(key_bytes, AES.MODE_CBC, iv_bytes)
        decrypted = unpad(cipher.decrypt(encrypted), AES.block_size)
        return decrypted.decode("utf-8")
