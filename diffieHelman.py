#https://github.com/AmitNutman/BruteForce



import random


class DiffieHelman():

    def __init__(self, g, p):
        """
        builds new object with p, g, secret_key
        :param g: num g
        :param p: num p
        :param secret_key: the secret key(a)
        """
        self.g = g
        self.p = p
        self.secret_key = random.randint(1, self.p-1)

    def calc_key_1(self):
        """
        calcs the public key
        :return: the public key(number1)
        """
        return self.g ** self.secret_key % self.p

    def calc_key_2(self, previous_key):
        """
        calcs the shared key
        :param previous_key: the public key(first_key)
        :return: the shared key
        """
        return previous_key ** self.secret_key % self.p


if __name__ == '__main__':

    alice = DiffieHelman(5, 23)
    alice_key1 = alice.calc_key_1()

    bob = DiffieHelman(5, 23)
    bob_key1 = bob.calc_key_1()


    alice_shared = alice.calc_key_2(bob_key1)
    bob_shared = bob.calc_key_2(alice_key1)

    print(f"Alice Shared: {alice_shared}")
    print(f"Bob Shared: {bob_shared}")
