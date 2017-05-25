#!/usr/bin/env python3 -tt
"""
File: crypto.py
---------------
Assignment 1: Cryptography
Course: CS 41
Name: Mamadou Diallo
SUNet: mamadou

TODO: Replace this with a description of the program.
"""
import utils
import random
# Caesar Cipher

def encrypt_caesar(plaintext):
    """Encrypt plaintext using a Caesar cipher.

    This function encrypts the plaintext passed in as an argument by moving each letter 3 letters forward by turning the letter into its unicode value. Adding 3. Than back to a character.
    """

    def caesar(alpha):
        if (alpha == " "):
            return chr(ord(alpha))
        if (ord(alpha) >= 88):
            return chr(ord(alpha) - 23)
        else:
            return chr(ord(alpha) + 3)

    encrypted = ''.join(caesar(alpha) for alpha in plaintext)
    return encrypted

# encrypt_caesar("PYTHON")


def decrypt_caesar(ciphertext):
    """Decrypt a ciphertext using a Caesar cipher.

    Add more implementation details here.
    """

    def decrypt(alpha):
        if (ord(alpha) <= 67):
            return chr(ord(alpha) + 23)
        else:
            return chr(ord(alpha) - 3)

    decrypted = ''.join(decrypt(alpha) for alpha in ciphertext)
    return decrypted

# decrypt_caesar("SBWKRQ")

# Vigenere Cipher

def extend_keyword(keyword, size):
    index = 0
    extended_keyword = keyword
    while(len(extended_keyword) != len(size)):
        if (index == len(keyword)):
            index = 0;
        extended_keyword = extended_keyword + keyword[index]
        index += 1
    return extended_keyword

def encrypt_vigenere(plaintext, keyword):
    """Encrypt plaintext using a Vigenere cipher with a keyword.

    Add more implementation details here.
    """

    extended_keyword = extend_keyword(keyword, plaintext)

    def vigenere(plain, key):
        combo = (ord(plain) - 65) + (ord(key) - 65)
        if (combo > 26): combo = combo - 26;
        return chr(combo + 65)


    encrypted = ''.join(vigenere(plaintext[i], extended_keyword[i]) for i in range(0, len(plaintext)))
    return encrypted

# encrypt_vigenere("ATTACKATDAWN", "LEMON")

def decrypt_vigenere(ciphertext, keyword):
    """Decrypt ciphertext using a Vigenere cipher with a keyword.

    Add more implementation details here.
    """

    extended_keyword = extend_keyword(keyword, ciphertext)

    def decrypt(letter, key):
        plain = (ord(letter) - 65) - (ord(key) - 65)
        if (plain < 0): plain = plain + 26
        return chr(plain + 65)


    decrypted = ''.join(decrypt(ciphertext[i], extended_keyword[i]) for i in range(0, len(ciphertext)))
    return decrypted

# decrypt_vigenere("LXFOPVEFRNHR", "LEMON")

# Merkle-Hellman Knapsack Cryptosystem

def generate_private_key(n=8):
    """Generate a private key for use in the Merkle-Hellman Knapsack Cryptosystem.

    Following the instructions in the handout, construct the private key components
    of the MH Cryptosystem. This consistutes 3 tasks:

    1. Build a superincreasing sequence `w` of length n
        (Note: you can check if a sequence is superincreasing with `utils.is_superincreasing(seq)`)
    2. Choose some integer `q` greater than the sum of all elements in `w`
    3. Discover an integer `r` between 2 and q that is coprime to `q` (you can use utils.coprime)

    You'll need to use the random module for this function, which has been imported already

    Somehow, you'll have to return all of these values out of this function! Can we do that in Python?!

    @param n bitsize of message to send (default 8)
    @type n int

    @return 3-tuple `(w, q, r)`, with `w` a n-tuple, and q and r ints.
    """

    superincreasing = [random.randint(2, 10)]   # returns random int between 2 and 10
    for i in range(n):  # I'm sure I could of fit this into one line but it just would've been ugly.
        superincreasing.append(random.randint(sum(superincreasing) + 1, 2 * sum(superincreasing)))

    q = random.randint(sum(superincreasing) + 1, 2 * sum(superincreasing))

    # generate r where r is a random int between 2 and q-1 and co-prime with q
    while True:
        r = random.randint(2, q-1)
        if (utils.coprime(r, q)):
            break

    public_key = superincreasing, q, r

    return public_key

# generate_private_key()

def create_public_key(private_key):
    """Create a public key corresponding to the given private key.

    To accomplish this, you only need to build and return `beta` as described in the handout.

        beta = (b_1, b_2, ..., b_n) where b_i = r × w_i mod q

    Hint: this can be written in one line using a list comprehension

    @param private_key The private key
    @type private_key 3-tuple `(w, q, r)`, with `w` a n-tuple, and q and r ints.

    @return n-tuple public key
    """
    beta = tuple([(x * private_key[2]) % private_key[1] for x in private_key[0]])
    return beta

def encrypt_mh(message, public_key):
    """Encrypt an outgoing message using a public key.

    1. Separate the message into chunks the size of the public key (in our case, fixed at 8)
    2. For each byte, determine the 8 bits (the `a_i`s) using `utils.byte_to_bits`
    3. Encrypt the 8 message bits by computing
         c = sum of a_i * b_i for i = 1 to n
    4. Return a list of the encrypted ciphertexts for each chunk in the message

    Hint: think about using `zip` at some point

    @param message The message to be encrypted
    @type message bytes
    @param public_key The public key of the desired recipient
    @type public_key n-tuple of ints

    @return list of ints representing encrypted bytes
    """

    # To encrypt: convert each letter into its bit version
    seperate_message = [message[i:i+8] for i in range(0, len(message), 8)]

    list_to_return = []
    for chunk in seperate_message:
        for letter in chunk:
            alpha = tuple(utils.byte_to_bits(ord(letter)))
            # Multiple each bit by the public_key equavalent of it
            total = 0
            for key, bit in zip(public_key, alpha):
                total += key * bit

            list_to_return.append(total)

    return list_to_return

def decrypt_mh(message, private_key):
    """Decrypt an incoming message using a private key

    1. Extract w, q, and r from the private key
    2. Compute s, the modular inverse of r mod q, using the
        Extended Euclidean algorithm (implemented at `utils.modinv(r, q)`)
    3. For each byte-sized chunk, compute
         c' = cs (mod q)
    4. Solve the superincreasing subset sum using c' and w to recover the original byte
    5. Reconsitite the encrypted bytes to get the original message back

    @param message Encrypted message chunks
    @type message list of ints
    @param private_key The private key of the recipient
    @type private_key 3-tuple of w, q, and r

    @return bytearray or str of decrypted characters
    """
    w = private_key[0]
    q = private_key[1]
    r = private_key[2]
    s = utils.modinv(r, q)
    return None
