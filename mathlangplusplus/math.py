# math functions - use binary
# to convert a number into binary: "{:b}".format(number)

def to_binary(num: int):
    return "{:b}".format(num)

# returns a binary number as a string
def add(num1: str, num2: str):
    x = int(num1, 2)
    y = int(num2, 2)

    # bitwise addition: repeat until there is no carry
    while y != 0:
        carry = x & y  # carry
        x = x ^ y  # sum without carry
        y = carry << 1  # shift carry left

    return str(bin(x)[2:])

#def multiply(num1: str, num2: str):



print(int(add(to_binary(1), to_binary(2)), 2))

MAX_ITERATIONS = 10
INITIAL_GUESS = 1

def square_root(x):
    xn = INITIAL_GUESS
    for i in range(MAX_ITERATIONS):
        xn1 = 0.5 * (xn + x / xn)
        xn = xn1

    return xn

print(square_root(10))