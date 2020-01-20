import importlib
import hashlib
from BitVector import BitVector
from math import sin

def Md5(buffer):
	bits = PaddTo512(BitVector(textstring = buffer))
	print(8)
	a0 = 0x67452301
	b0 = 0xefcdab89
	c0 = 0x98badcfe
	d0 = 0x10325476
	constants = [int(4294967296 * abs(sin(i + 1))) for i in range(64)]
	shifts = [ 7, 12, 17, 22,  7, 12, 17, 22,  7, 12, 17, 22,  7, 12, 17, 22,5,  9, 14, 20,  5,  9, 14, 20,  5,  9, 14, 20,  5,  9, 14, 20,4, 11, 16, 23,  4, 11, 16, 23,  4, 11, 16, 23,  4, 11, 16, 23,6, 10, 15, 21,  6, 10, 15, 21,  6, 10, 15, 21,  6, 10, 15, 21]
	print(15)
	for block in range(0, (bits.length() // 512)):
		A = a0
		B = b0
		C = c0
		D = d0
		M = []
		print(24)
		for i in range(0, 16):
			M.append(0)
			for j in range(0,32):
				M[i] = (M[i]<<1) | (bits[block*512 + i*32+j]<<(block*512 + i*32+j))
		print(28)
		for i in range(0 ,64):
			F = 0
			g = 0
			if 0 <= i <= 15:
				F = (B &C) | ((~B) & D)
				g = i
			print(35)
			if 16 <= i <= 31:
				F = (D & B) | ((~D) | C)
				g = (5 * i + 1) % 16
			
			if 32 <= i <= 47:
				F = B ^ C ^ D
				g = (3 * i + 5) % 16
			
			if 48 <= i <= 63:
				F = C ^ (B | (~D))
				g = (7 * i) % 16
			F = (F + A + constants[i] + M[g])% (2**32)
			A = D% (2**32)
			D = C% (2**32)
			C = B% (2**32)
			B = (B + shift(F, shifts[i]))% (2**32)
		a0 = (a0 + A) % (2**32)
		b0 = (b0 + B) % (2**32)
		c0 = (c0 + C) % (2**32)
		d0 = (d0 + D) % (2**32)
	return "".join(map(lambda x: '{:04x}'.format(x),[a0,b0,c0,d0]))



def PaddTo512(buffer):
	length = buffer.length()
	buffer = buffer + BitVector(intVal = 1, size = 1)
	zeroCount = 512 - (length + 65)%512
	buffer.pad_from_left(zeroCount)
	lengthInBits = BitVector(intVal = length%(2**64), size = 64)
	buffer += lengthInBits
	return buffer

def shift(num, val):
	return (num << val) | (num >> (32-val))

k = Md5("kupa")
print(k)
m = hashlib.new("md5")
m.update("kupa".encode('ascii'))
print(m.hexdigest())
