#  include encryption functionality for:
#  1. generate password hash
#  2. verify password hash 

from passlib.hash import pbkdf2_sha256 as sha256


class Encryption():

    def __init__(self):
        pass

    # create password hash
    def generate_hash(self, password):
        return sha256.hash(password)

    # verify pasword to stored hash
    def verify_hash(self, password, hash):
        return sha256.verify(password, hash)
