import random
import string


def random_id_generator():
    return "".join(
        (random.choice(string.ascii_letters + string.digits) for x in range(50))
    )
