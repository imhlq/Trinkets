# A Small Library Related to Prime Number
# Copyright (c) 2024 xHou

import numpy as np
import os, secrets
import random
import time


# Generate secure random number
def rand_bytes():
    iv = os.urandom(16)
    serial = int.from_bytes(iv, byteorder='big')
    return serial

# Popular algorithm to check prime
def is_prime(num: int):
    if num <= 1 or num % 2 == 0 or num % 3 == 0:
        return False
    i = 5
    while i * i <= num:
        if num % i == 0 or num % (i + 2) == 0:
            return False
        i += 6
    return True


def get_primes(limit: int):
    # Simple Sieve of Eratosthenes
    sieve = [True] * (limit + 1)
    p = 2
    while (p * p <= limit):
        if (sieve[p] == True):
            for i in range(p * p, limit + 1, p):
                sieve[i] = False
        p += 1
    primes = [p for p in range(2, limit) if sieve[p]]
    return primes


# ================
# Prime Factors of Integer
# ================

def prime_factors(num: int):
    factors = []
    # Check for number of 2s that divide num
    while num % 2 == 0:
        factors.append(2)
        num = num // 2
    
    # num must be odd at this point, thus skip even numbers
    for i in range(3, int(num**0.5) + 1, 2):
        while num % i == 0:
            factors.append(i)
            num = num // i
    
    # This condition is to check if num is a prime number greater than 2
    if num > 2:
        factors.append(num)
    
    return factors

# Calcuate prime list at first
def efficient_prime_factors(num: int):
    factors = []
    primes = get_primes(int(num**0.5) + 1)  # Generate primes up to the square root of num
    
    for prime in primes:
        while num % prime == 0:
            factors.append(prime)
            num = num // prime
    
    # If num is a prime number greater than the largest prime in the list
    if num > 1:
        factors.append(num)
    
    return factors

# Shor' algorithm [Simulated Quantum]
def gcd(a, b):
    """Compute the greatest common divisor of a and b."""
    while b != 0:
        a, b = b, a % b
    return a

def modular_exponentiation(base, exponent, mod):
    """Perform modular exponentiation efficiently."""
    result = 1
    base = base % mod
    while exponent > 0:
        if (exponent % 2) == 1:  # If exponent is odd, multiply base with result
            result = (result * base) % mod
        exponent = exponent >> 1  # Divide exponent by 2
        base = (base * base) % mod  # Square the base
    return result

def find_period(a, N):
    """Simulate the quantum period finding subroutine."""
    for r in range(1, N):
        if modular_exponentiation(a, r, N) == 1:
            return r
    return None

def shor_algorithm(N: int):
    """Shor's Algorithm simulated on a classical computer."""
    if is_prime(N):
        return f"{N} is prime."
    elif N % 2 == 0:
        return "2 is a factor."

    while True:
        # find a, st. gcd(a, N) = 1
        a = random.randint(2, N - 1)
        gcd_result = gcd(a, N)
        if gcd_result > 1:
            return f"{gcd_result} is a factor (found by GCD)."
        # find min even r, st. a**r = 1 mod N
        r = find_period(a, N)
        if r is None:
            continue
        if r % 2 != 0:
            continue  # Period must be even

        plus_factor = modular_exponentiation(a, r // 2, N) + 1
        minus_factor = modular_exponentiation(a, r // 2, N) - 1
        factor1 = gcd(plus_factor, N)
        factor2 = gcd(minus_factor, N)

        if factor1 == N or factor2 == N:
            continue  # Trivial factor, retry
        return f"Factors found: {factor1} and {factor2}"



def test():
    t_case = [32, 44, 3945, 99939, 12093909432, 3945809348590383]

    start_time = time.time()
    for t_ in t_case:
        print(t_, prime_factors(t_))
    end_time = time.time()
    print(f"Function Time: {end_time - start_time:.5f} seconds")


    start_time = time.time()
    for t_ in t_case:
        print(t_, shor_algorithm(t_))
    end_time = time.time()
    print(f"Function Time: {end_time - start_time:.5f} seconds")


if __name__ == '__main__':
    test()
