import struct
import imghdr
import csv

def generateCards(numberOfSymb,expt_no):
	"""
	Generates a list of cards which are themselves a list of symbols needed on each card to respect the rules of Dobble.
	This algorithm was taken from the french Wikipedia page of "Dobble".
	https://fr.wikipedia.org/wiki/Dobble
	:param numberOfSymb: Number of symbols needed on each card.
	:type numberOfSymb: int
	:returns: List of cards which are list of symbols on it.
	:rtype: List[List[int]]
	"""
	nbSymByCard = numberOfSymb
	nbCards = (nbSymByCard**2) - nbSymByCard + 1
	cards = []
	n = nbSymByCard - 1
	t = []
	t.append([[(i+1)+(j*n) for i in range(n)] for j in range(n)])
	for ti in range(n-1):
		t.append([[t[0][((ti+1)*i) % n][(j+i) % n] for i in range(n)] for j in range(n)])
	t.append([[t[0][i][j] for i in range(n)] for j in range(n)])
	for i in range(n):
		t[0][i].append(nbCards - n)
		t[n][i].append(nbCards - n + 1)
		for ti in range(n-1):
			t[ti+1][i].append(nbCards - n + 1 + ti + 1)
	t.append([[(i+(nbCards-n)) for i in range(nbSymByCard)]])
	for ti in t:
		cards = cards + ti

	# file_name = f'./generated/{expt_no}/card_pack.csv'
	file_name = f'./generated/card_pack.csv'
	# opening the csv file in 'w+' mode
	file = open(file_name, 'w+', newline ='')
	with file:    
		write = csv.writer(file)
		write.writerows(cards)
	return cards

def get_image_size(fname):
	"""
	Determine the image type of fhandle and return its size. From draco
	Code copied from https://stackoverflow.com/a/20380514 and made by https://stackoverflow.com/users/2372270/fred-the-fantastic
	:param fname: Name of the file to open with the path.
	:type fname: string
	:returns: Width and height of the image.
	:rtype: int, int.
	"""
	with open(fname, 'rb') as fhandle:
		head = fhandle.read(24)
		if len(head) != 24:
			return
		if imghdr.what(fname) == 'png':
			check = struct.unpack('>i', head[4:8])[0]
			if check != 0x0d0a1a0a:
				return
			width, height = struct.unpack('>ii', head[16:24])
		elif imghdr.what(fname) == 'gif':
			width, height = struct.unpack('<HH', head[6:10])
		elif imghdr.what(fname) == 'jpeg':
			try:
				fhandle.seek(0) # Read 0xff next
				size = 2
				ftype = 0
				while not 0xc0 <= ftype <= 0xcf:
					fhandle.seek(size, 1)
					byte = fhandle.read(1)
					while ord(byte) == 0xff:
						byte = fhandle.read(1)
					ftype = ord(byte)
					size = struct.unpack('>H', fhandle.read(2))[0] - 2
				# We are at a SOFn block
				fhandle.seek(1, 1)  # Skip `precision' byte.
				height, width = struct.unpack('>HH', fhandle.read(4))
			except Exception: #IGNORE:W0703
				return
		else:
			return
		return width, height

def distanceBetweenTwoPoints(a, b):
	"""
	Gives the distance between two points on a 2D grid.
	:param a: Tuple of the first point with a X and Y coordinate.
	:type a: List
	:param b: Same as a.
	:type b: List
	:returns: Distance between those points.
	:rtype: Float or int depending of the type of the coordinates.
	"""
	return (abs(a[0] - b[0]) + abs(a[1] - b[1]))

def collisionBetweenTwoSurfaces(r1_ul, r1_lr, r2_ul, r2_lr):
	"""
	Check wheter two rectangles are colliding.
	:param r1_ul: Point of the upper left corner of the first rectangle.
	:param r1_lr: Point of the lower right corner of the first rectangle.
	:param r2_ul: Point of the upper left corner of the second rectangle.
	:param r2_lr: Point of the lower right corner of the second rectangle.
	:returns: Boolean telling if the rectangles are colliding.
	:rtype: Boolean
	"""
	return not (r2_ul[0] > r1_lr[0] or r2_lr[0] < r1_ul[0] or r2_ul[1] > r1_lr[1] or r2_lr[1] < r1_ul[1])
