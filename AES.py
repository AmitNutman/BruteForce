# Importing base64 module for encoding/decoding data in base64 format
import base64
from Cryptodome.Cipher import AES
from Cryptodome import Random
import hashlib


class AESCipher(object):

    def __init__(self, key):
        '''
        initialize the cipher with a given key
        :param key: the key used to decrypt and encrypt
        '''
        # block size for AES (16 bytes)
        self.bs = AES.block_size
        # create a 32-byte key using SHA-256 hash
        self.key = hashlib.sha256(str(key).encode()).digest()

    def encrypt(self, raw):
        '''
        encrypt the text
        :param raw: the text string to encrypt
        :return: the encryption (base64-encoded ciphertext)
        '''
        # add spaces (padding) to be in the size of the block
        raw = self._pad(raw)
        # create a random IV (Initialization Vector)
        iv = Random.new().read(AES.block_size)
        #  Create AES cipher with the key and IV in CBC mode
        cipher = AES.new(self.key, AES.MODE_CBC, iv)
        # encrypt the padded text
        return base64.b64encode(iv + cipher.encrypt(raw.encode()))

    def encrypt_bytes(self, data):
        """
        encrypt bytes
        :param data: the bytes to encrypt
        :return: the encrypted bytes
        """
        # add spaces (padding) to be in the size of the block
        padded_data = self._pad_bytes(data)
        # create a random IV (Initialization Vector)
        iv = Random.new().read(AES.block_size)
        #  Create AES cipher with the key and IV in CBC mode
        cipher = AES.new(self.key, AES.MODE_CBC, iv)
        # encrypt the padded data using AES IN CBC mode
        ciphertext = cipher.encrypt(padded_data)
        return iv + ciphertext


    def decrypt(self, enc):
        '''
        decrypt the text
        :param enc: the encrypted string (base64-encoded string containing the IV and ciphertext)
        :return: the original text
        '''
        # decode the base64-encoded input
        enc = base64.b64decode(enc)
        # extract the IV from the beginning of the decoded data
        iv = enc[:AES.block_size]
        # create AES cipher with the same key and IV
        cipher = AES.new(self.key, AES.MODE_CBC, iv)
        # unpad and decode the text (and decrypt the ciphertext)
        return self._unpad(cipher.decrypt(enc[AES.block_size:])).decode('utf-8')


    def decrypt_file(self, enc):
        """
        decrypt the bytes
        :param enc: the encrypted bytes
        :return: the original file's bytes
        """
        # extract the IV from the beginning of the encrypted data
        iv = enc[:AES.block_size]
        # the rest of the data is the ciphertext
        ciphertext = enc[AES.block_size:]
        # creates AES cipher with the same key and iv
        cipher = AES.new(self.key, AES.MODE_CBC, iv)
        # decrypt the ciphertext (still padded)
        plaintext_padded = cipher.decrypt(ciphertext)
        # remove padding and return the original file's bytes
        return self._unpad_bytes(plaintext_padded)


    def encrypt_file(self, file_path):
        """
        encrypt the file
        :param file:
        :return: encrypted string
        """
        with open(file_path, "rb") as f:
            data = f.read()
        # return the encrypted bytes
        return self.encrypt_bytes(data)



    def _pad(self, s):
        '''
         Pads the input string (to ensure its length is a multiple of the block size)
        :param s: The input string to pad
        :return: the padded string
        '''
        # calculate number of padding bytes needed, append padding characters
        return s + (self.bs - len(s) % self.bs) * chr(self.bs - len(s) % self.bs)

    def _pad_bytes(self, s):
        '''
         Pads the input string (to ensure its length is a multiple of the block size)
        :param s: The input string to pad
        :return: the padded string
        '''
        # how much bytes are missing
        n = self.bs - (len(s) % self.bs)
        padding = bytes([n])*n
        # return the original data + padding
        return s + padding



    @staticmethod
    def _unpad(s):
        '''
         removes PKCS#7 padding from the decrypted text.
        :param s: the padded text as bytes
        :return: the unpadded text as bytes
        '''
        # remove padding bytes based on value of the last byte
        return s[:-ord(s[len(s)- 1 :])]


    @staticmethod
    def _unpad_bytes(s):
        '''
         removes PKCS#7 padding from the decrypted text.
        :param s: padded bytes
        :return: unpadded bytes
        '''
        # the last byte indicates the padding length
        padding_len = s[-1]
        return s[:-padding_len]


if __name__ == '__main__':
    myAES = AESCipher(1234)

    file = "dog.jpg"

    dnc_dog = myAES.encrypt_file(file)

    new_dog = myAES.decrypt_file(dnc_dog)

    with open("newDog.jpg", 'wb') as f:
        f.write(new_dog)

