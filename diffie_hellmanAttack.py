from random import (
    randint,
    seed
)
from computeDL import (
    gelfond_shanks,
    pollig_hellman,
    pollard_rho
)

# Compound numbers that hard to identify correctly by probabilistic algorythms 
CARMICHAEL_NUMBERS = list([561, 1105, 1729, 2465, 2821, 6601, 8911, 10585,
                          15841, 29341, 41041, 46657, 52633, 62745,
                          63973, 75361])
LOW_PRIME = list([2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 39, 41, 43, 47])

def gcd(a_value, b_value):
    """
    Function finds an gcd of a pair of given numbers.\n

    :param int a_value: first value\n
    :param int n_value: second value\n

    """

    if a_value < b_value:
        a_value, b_value = b_value, a_value
    while b_value:
        a_value, b_value = b_value, a_value % b_value
    return a_value


def ferma_test(simple_value, rounds):

    """
    Function determines whether given value is a simple or not
    with Ferma algorythm.\n
    Possible values: True, False, ValueError, "Error message"\n

    :param int simple_value: number that will be checked on simplicity\n
    :param int rounds: check iteration number\n

    """

    if simple_value == 2 or simple_value == 3:
        return True

    if simple_value in CARMICHAEL_NUMBERS:
        return False

    # Seeding randint function for clear number randomizing
    seed(randint(1, 2048))

    if simple_value == 1:
        return ValueError, "1 is neither an a simple or compound number"

    # Checking if given simple value is odd
    if simple_value % 2 is 0:
        return ValueError, "Given number is even"

    # Perform multiple rounds of division
    for _ in range(rounds):
        random_simple = int(0)
        while gcd(random_simple, simple_value) != 1:
            random_simple = randint(2, simple_value)
        # Numpy array approach for performing big-integer operations
        if int(pow(random_simple, simple_value - 1, simple_value)) != 1:
            return False
        else:
            continue

    return True


def diffie_hellman(bit_size):
    seed(randint(1, 2048))
    print("{:-^50}".format("Генерация начальных параметров протокола Диффи-Хеллмана"))
    p = randint(1, int('1' * bit_size, 2))
    g = int()
    while ferma_test(p, 7) is False or \
        ferma_test((p - 1) // 2, 7) is False:
        p = randint(1, int('1' * bit_size, 2))
    g = LOW_PRIME[randint(1, len(LOW_PRIME) - 1)]    
    print("Были сформированы следующие параметры: ", p, g)
    print("{:-^50}".format("Генерация закрытых ключей"))
    a_secret = randint(1, int('1' * bit_size, 2))
    b_secret = randint(1, int('1' * bit_size, 2))
    print("Следующие закрытые ключи были сгенерированы: ", a_secret, b_secret)
    print("{:-^50}".format("Генерация открытых ключей"))
    a_open = pow(g, a_secret, p)
    b_open = pow(g, b_secret, p)
    print("Следующие открытые ключи были сгенерированы: ", a_open, b_open)
    print("{:-^50}".format("Передача открытого ключа стороне А"))
    print("{:-^50}".format("Перехват открытого ключа злоумышленником"))
    print("{:-^50}".format("Вычисление дискретного логарифма и поиск закрытого ключа злоумышленником"))
    gs = gelfond_shanks(g, b_open, p)
    ph =  pollig_hellman(g, b_open, p)
    otc = pollard_rho(g, b_open, p)
    print("Дискретный логарифм был вычислен: ", b_secret)
    print("Вычисление секретного ключа злоумышленником: ", pow(a_open, b_secret, p))
    print("{:-^50}".format("Вычисление общего секретного ключа"))
    b_common = pow(a_open, b_secret, p)
    a_common = pow(b_open, a_secret, p)
    print("Общий секретный ключ: ", a_common)
    if a_common == b_common:
        print("Секретный ключ злоумышленника совпадает с общим секретным ключом!\nВыход из алгоритма, передача сообщений больше не считается защищенной...")


if __name__ == "__main__":
    diffie_hellman(16)