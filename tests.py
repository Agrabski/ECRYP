import MD5
import random
import string


def randomString(length):
	letters = string.ascii_lowercase
	return ''.join(random.choice(letters) for i in range(length))
size = 10_000
hashes = dict()
print("generating hashes")
for i in range(0, size):
	if i % (size//1000) == 0:
		print('{0:.2f}%'.format(((i/size)*100)))
	str = randomString(random.randint(1, size))
	hash = MD5.Md5(str)
	if hash in hashes.items():
		hashes[hash] += 1
	else:
		hashes[hash] = 1
print("hash generation complete")
values = list(hashes.values())
values.sort(reverse = True)
print("expected hash propability:{0:.4f}%".format(1/size*100))
print("top 10 highest propabilities:")
for i in range(1, 10):
	print("propability:{0:.4f}%".format(values[i] / size * 100))
printed = []
print('distribution of propability:')
for val in values:
	if val not in printed:
		printed.append(val)
		print('{0:.4f}% '.format(val / size * 100) + 'occured in {0:.4f}% of cases'.format(values.count(val)/len(values)*100))