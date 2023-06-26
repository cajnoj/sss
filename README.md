# A CLI implementation of Shamir's Secret Sharing algorithm 

## Splitting a password

Input that you'll be required to enter:

- Password - legal characters are `"0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ!"#$%&'()*+,-./:;<=>?@[\]^_{|}~"`
- Amount of shares `N`
- Restoration threshold `K` (must not be larger than `N`)

Invocation:

    sss[.py] split

Output:

A list of `N` shares.

The share format is: `"x,y"` where `x` is an integer between `1` and `N` and `y` is an alphanumeric string optionally split by dashes `-`.
For example: `"3,2L5L3-ECH5R-XUK1W-YKWV0-S8WGS"`

## Recovering a pasword

Input that you'll be required to enter:

- A list of `K` separate shares - case insensitive.
- Terminate the list by pressing ENTER

Usage:

    sss[.py] recover