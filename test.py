import random
a = [random.choice('qwertyuiopasdfghjklzxcvbnm') for _ in range(4)]
a = "".join(a)
print(a)