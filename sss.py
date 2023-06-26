#!/bin/python
import argparse
import sys
from getpass import getpass
import itertools

from encoding import SHARE_ALPHABET, PASSWORD_ALPHABET, encode, decode
from algorithm import make_random_shares, recover_secret, PRIME

def split(s, n, k):
    shares = make_random_shares(s, minimum=k, shares=n)

    print('Shares:')
    if shares:
        # Verify that all permutations can recover the secret
        for permutation in itertools.permutations(shares, k):
            assert(s==recover_secret(permutation))

        for share in shares:
            encoding = encode(share[1], SHARE_ALPHABET)
            easy_read = '-'.join(encoding[i:i+5] for i in range(0, len(encoding), 5))
            print(f'  {share[0]},{easy_read}')

def input_int(prompt, desc):
    val = input(prompt)
    try:
        val = int(val)
        return val
    except ValueError:
        print(f'ERROR: The {desc} should be an integer.')
        exit(8)

def input_and_split():
    # Get and verify password
    password = getpass('Enter the password to share: ')
    repassword = getpass('Re-enter the password: ')
    if password != repassword:
        print('ERROR: The passwords that you entered did not match.', file=sys.stderr)
        exit(4)

    if len([c for c in password if c not in PASSWORD_ALPHABET]) > 0:
        print(f'ERROR: Legal password characters are {PASSWORD_ALPHABET}', file=sys.stderr)
        exit(1)

    secret = decode(password, PASSWORD_ALPHABET)
    if secret >= PRIME:
        print('ERROR: The password is too long.', file=sys.stderr)
        exit(2)

    # Get and verify shares and threshold numbers
    shares_num = input_int('Enter the amount of shares: ', 'amount of shares')
    threshold = input_int('Enter the threshold for recovering the password: ', 'threshold for recovering the password')

    if threshold > shares_num:
        print("ERROR: The threshold must not be larger than the amount of shares.", file=sys.stderr)
        exit(3)

    split(secret, shares_num, threshold)

def input_and_recover():
    shares = list()
    
    # Input shares until given ENTER
    while True:
        share = input('Enter a share (ENTER to finish): ')
        if share == '':
            break

        x, f_x = share.split(',')
        x = int(x)
        f_x = f_x.replace('-', '').upper()
        if len([c for c in f_x if c not in SHARE_ALPHABET]) > 0:
            print(f'ERROR: Legal share characters are {SHARE_ALPHABET}', file=sys.stderr)
            exit(6)

        shares.append((int(x), decode(f_x, SHARE_ALPHABET)))

    if len(shares) == 0:
        print("ERROR: No shares entered.", file=sys.stderr)
        exit(5)

    print(f'The recovered password should be: {encode(recover_secret(shares), PASSWORD_ALPHABET)}')

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('command', type=str, choices=['split', 'recover'], help='`split`: create N pieces from key, `recover`: recover key from K pieces')
    args = parser.parse_args()

    if args.command == 'split':
        input_and_split()

    elif args.command == 'recover':
        input_and_recover()
