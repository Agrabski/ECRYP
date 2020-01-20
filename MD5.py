import importlib
import hashlib
from BitVector import BitVector
from math import sin

def Md5(buffer):
	bits = PaddTo512(BitVector(textstring = buffer))

	A = 0x67452301
	B = 0xefcdab89
	C = 0x98badcfe
	D = 0x10325476

	rounds = [
		lambda a, b, c: (a & b) | (~a & c),
		lambda a, b, c: (a & c) | (a & ~c),
		lambda a, b, c: a ^ b ^ c,
		lambda a, b, c: b ^ (a & ~c)
	]
	constants = [int(4294967296 * abs(sin(i + 1))) for i in range(64)]
	for block in range(0, (bits.length() // 16) - 1):
		X = 0
		for i in range(0, 15):
			X |= bits[block * 16 + i] << i
		temporary = [A,B,C,D]
		i = 1
		shiftStarts = [7, 5, 4, 6]
		shiftChanges = [
			[0,5, 10, 15],
			[0,4, 9, 15],
			[0,7, 12, 19],
			[0,4, 9, 15],
		]
		indeces = [
			[0, 1, 2, 3],
			[3, 0, 1, 2],
			[2, 3, 0, 1],
			[1, 2, 3, 0]
		]
		kStarts = [0, 1, 5, 0]
		kChanges = [1, 5, 3, 7]
		for round in range(4):
			#print(round)
			for y in range(4):
				for x in range(4):
					#print('[{:1}{:1}{:1}{:1}|{:2},{:2},{:2}]'.format(indeces[x][0], indeces[x][1], indeces[x][2], indeces[x][3],(kStarts[round] + kChanges[round]*(x + 4*y)) % 16,shiftStarts[round] + shiftChanges[round][x],i), end=" ")
					temporary[x] = PerformRound(
						rounds[round],
						temporary[indeces[x][0]],
						temporary[indeces[x][1]],
						temporary[indeces[x][2]],
						temporary[indeces[x][3]],
						(kStarts[round] + kChanges[round]*(x + 4*y)) % 16,
						shiftStarts[round] + shiftChanges[round][x],
						i,X,constants) % (2** 32)
					i += 1
				#print('\n')
		A = (A + temporary[0]) % (2 ** 32)
		B = (B + temporary[1]) % (2 ** 32)
		C = (C + temporary[2]) % (2 ** 32)
		D = (D + temporary[3]) % (2 ** 32)
	t = [A, B, C, D]
	print('{:04x}'.format(A))
	print('{:04x}'.format(B))
	print('{:04x}'.format(C))
	print('{:04x}'.format(D))
	return "".join(map(lambda x: '{:04x}'.format(x),t))
	


def PaddTo512(buffer):
	length = buffer.length()
	buffer = buffer + BitVector(intVal = 1, size = 1)
	zeroCount = 512 - (length + 65)%512
	buffer.pad_from_left(zeroCount)
	lengthInBits = BitVector(intVal = length%(2**64), size = 64)
	buffer += lengthInBits
	return buffer

def PerformRound(f, a, b, c, d, k, s, i,block, constants):
	return b + shift((a + f(b, c, d) + block & shift(1 , k) + constants[i-1]), s)
def shift(num, val):
	result = num
	for i in range(0,val):
		oldest = num & (1<<31)
		result = result <<1
		if oldest != 0:
			result |= 1
	return result & 0b11111111111111111111111111111111

print(Md5("kupa"))
m = hashlib.new("md5")
m.update("kupa".encode('utf-8'))
print(m.hexdigest())
