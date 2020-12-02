sudoku = """002900010
100003000
000000207
000000903
400001000
005800040
051790080
040060000
073140000"""

def print1(board):
	text = ""
	for y in range(9):
		line = ""
		for x in range(9):
			item = sudoku[y][x]
			if type(item) is list:
				line += " "
			else:
				line += item
		text += line + "\n"
	print(text)

def print2(board):
    print("-"*37)
    for i, row in enumerate(board):
        print(("|" + " {}   {}   {} |"*3).format(*[x if x != 0 else " " for x in row]))
        if i == 8:
            print("-"*37)
        elif i % 3 == 2:
            print("|" + "---+"*8 + "---|")
        else:
            print("|" + "   +"*8 + "   |")

def print3(board):
	sudoku = [[" " for x in range(35)] for y in range(35)]
	for y in range(3):
		for x in range(3):
			for y1 in range(3):
				for x1 in range(3):
					item = board[y*3 + y1][x*3 + x1]
					if type(item) is list:
						for y2 in range(3):
							for x2 in range(3):
								nx = x*11 + x + x1*3 + x1 + x2
								ny = y*11 + y + y1*3 + y1 + y2
								n = y2*3 + x2 + 1
								if n in item:
									sudoku[ny][nx] = str(n)
					else:
						nx = x*11 + x + x1*3 + x1 + 1
						ny = y*11 + y + y1*3 + y1 + 1
						sudoku[ny][nx-1] = "("
						sudoku[ny][nx] = str(item)
						sudoku[ny][nx+1] = ")"

	#add line
	for x in range(35):
		if x == 11 or x == 23:
			sudoku[11][x] = "+"
			sudoku[23][x] = "+"
		else:
			sudoku[11][x] = "-"
			sudoku[23][x] = "-"
			sudoku[x][11] = "|"
			sudoku[x][23] = "|"
	out = ""
	for line in sudoku:
		out += ("").join(line) + "\n"
	print(out)

class Sudoku:
	def __init__(self, sudoku):
		self.convert(sudoku)
		self.get_rows()
		self.get_columns()
		self.get_squares()
		self.single()

	def solve(self):
		i = 0 #fail sage
		found_single = True
		found_hidden = False
		found_pair = False
		while (found_single or found_hidden or found_pair) and i < 100 and len(self.remaining) > 0:
			i += 1
			found_single = self.single()
			found_hidden = False
			found_pair = False
			if not found_single:
				found_hidden = self.hidden_single()
				if not found_hidden:
					found_pair = self.naked_pair()

		if (len(self.remaining) > 0):
			print("failed!")
		else:
			print("solved!")

	def convert(self, sudoku):
		sudoku = sudoku.split()
		self.board = []
		self.remaining = []
		for y in range(9):
			line = list(sudoku[y])
			row = []
			for x in range(9):
				item = int(sudoku[y][x])
				if item == 0:
					self.remaining.append((x, y))
					row.append([1, 2, 3, 4, 5, 6, 7, 8, 9])
				else:
					row.append(item)
			self.board.append(row)

	def set(self, x, y, n):
		print(chr(y + 65) + str(x+1) + ": " + str(n), self.board[y][x])
		#print(x, y, n, self.rows[y], self.columns[x], self.squares[int(y/3)][int(x/3)])
		self.board[y][x] = n

		#fail safe
		if n in self.rows[y]: print("rows")
		if n in self.columns[x]: print("colums")
		if n in self.squares[int(y/3)][int(x/3)]: print("squares")

		#remove from remaning and update rows, columns, squares
		self.remaining.remove((x, y))
		self.rows[y].append(n)
		self.columns[x].append(n)
		self.squares[int(y/3)][int(x/3)].append(n)

	def get_rows(self):
		self.rows = []
		for y in range(9):
			row = []
			for x in range(9):
				item = self.board[y][x]
				if type(item) is int:
					row.append(item)
			self.rows.append(row)

	def get_columns(self):
		self.columns = []
		for x in range(9):
			column = []
			for y in range(9):
				item = self.board[y][x]
				if type(item) is int:
					column.append(item)
			self.columns.append(column)

	def get_squares(self):
		self.squares = []
		for y in range(3):
			line = []
			for x in range(3):
				square = []
				for y1 in range(3):
					for x1 in range(3):
						nx = x1 + x*3
						ny = y1 + y*3
						item = self.board[ny][nx]
						if type(item) is int:
							square.append(item)
				line.append(square)
			self.squares.append(line)

	def single(self):
		#if a number is the only option in a row, column and square
		found = False

		for (x, y) in self.remaining:
			item = self.board[y][x]

			#remove element if in row
			for element in self.rows[y]:
				if element in item:
					item.remove(element)

			#remove element if in column
			for element in self.columns[x]:
				if element in item:
					item.remove(element)

			#remove element if in square
			for element in self.squares[int(y/3)][int(x/3)]:
				if element in item:
					item.remove(element)

			#add to board
			if len(item) == 1:
				#print("single")
				found = True
				self.set(x, y, item[0])
				
		return found

	def hidden_single(self):
		#if a hidden number is the only hidden option in a row, column or square
		for (x, y) in self.remaining:

			#remove element if in row
			item = self.board[y][x][:]
			for y1 in range(9):
				if (y != y1 and type(self.board[y1][x]) is list):
					elements = self.board[y1][x]
					for element in elements:
						if element in item:
							item.remove(element)
			if len(item) == 1:
				#print("hidden single row")
				self.set(x, y, item[0])
				return True

			#remove element if in column
			item = self.board[y][x][:]
			for x1 in range(9):
				if (x != x1 and type(self.board[y][x1]) is list):
					elements = self.board[y][x1]
					for element in elements:
						if element in item:
							item.remove(element)
			if len(item) == 1:
				#print("hidden single column")
				self.set(x, y, item[0])
				return True

			#remove element if in square
			item = self.board[y][x][:]
			for y1 in range(3):
				for x1 in range(3):
					nx = 3*int(x/3) + x1
					ny = 3*int(y/3) + y1
					if not(nx == x and ny == y):
						elements = self.board[ny][nx]
						if type(elements) is list:
							for element in elements:
								if element in item:
									item.remove(element)
			if len(item) == 1:
				#print("hidden single square")
				self.set(x, y, item[0])
				return True

		return False

	def naked_pair_column(self, x, y):
		#generate a list from 0 to 9 and look for a pair of a candidate number in the column, which is in a square
		found = False
		count = [[] for i in range(9)]

		for y1 in range(9):
			if (x, y1) in self.remaining:
				for n in self.board[y1][x]:
					count[(n-1)].append(y1)

		for n in range(9):
			#check for a pair
			if len(count[n]) == 2:
				#check if it is in the same square
				x1 = 3*int(x/3)
				y1 = 3*int(count[n][0]/3)
				y2 = 3*int(count[n][1]/3)
				if (y1 == y2):
					#loop trough the square and remove candidate
					for ny in range(y1, y1+3):
						for nx in range(x1, x1+3):
							if nx != x and (nx, ny) in self.remaining:
								if (n+1) in self.board[ny][nx]:
									self.board[ny][nx].remove((n+1))
									found = True
					#if found:
						#print("Pair col " + chr(count[n][0] + 65) + str(x+1) + ", " + chr(count[n][1] + 65) + str(x+1) + " removes " + str(n+1))
			elif len(count[n]) == 3:
				#check if it is in the same square
				x1 = 3*int(x/3)
				y1 = 3*int(count[n][0]/3)
				y2 = 3*int(count[n][1]/3)
				y3 = 3*int(count[n][2]/3)
				if (y1 == y2 and y2 == y3):
					#loop trough the square and remove candidate
					for ny in range(y1, y1+3):
						for nx in range(x1, x1+3):
							if nx != x and (nx, ny) in self.remaining:
								if (n+1) in self.board[ny][nx]:
									self.board[ny][nx].remove((n+1))
									found = True
					#if found:
						#print("Triple col " + chr(count[n][0] + 65) + str(x+1) + ", " + chr(count[n][1] + 65) + str(x+1) + ", " + chr(count[n][2] + 65) + str(x+1) + " removes " + str(n+1))
		
		return found

	def naked_pair_row(self, x, y):
		#generate a list from 0 to 9 and look for a pair of a candidate number in the row, which is in a square
		found = False
		count = [[] for i in range(9)]

		for x1 in range(9):
			if (x1, y) in self.remaining:
				for n in self.board[y][x1]:
					count[(n-1)].append(x1)

		for n in range(9):
			#check for a pair
			if len(count[n]) == 2:
				#check if it is in the same square
				x1 = 3*int(count[n][0]/3)
				x2 = 3*int(count[n][1]/3)
				y1 = 3*int(y/3)
				if (x1 == x2):
					#loop trough the square and remove candidate
					for ny in range(y1, y1+3):
						for nx in range(x1, x1+3):
							if ny != y and (nx, ny) in self.remaining:
								if (n+1) in self.board[ny][nx]:
									self.board[ny][nx].remove((n+1))
									found = True
					#if found:
						#print("Pair row " + chr(y + 65) + str(count[n][0]+1) + ", " + chr(y + 65) + str(count[n][1]+1) + " removes " + str(n+1))
			elif len(count[n]) == 3:
				#check if it is in the same square
				x1 = 3*int(count[n][0]/3)
				x2 = 3*int(count[n][1]/3)
				x3 = 3*int(count[n][2]/3)
				y1 = 3*int(y/3)
				if (x1 == x2 and x2 == x3):
					#loop trough the square and remove candidate
					for ny in range(y1, y1+3):
						for nx in range(x1, x1+3):
							if ny != y and (nx, ny) in self.remaining:
								if (n+1) in self.board[ny][nx]:
									self.board[ny][nx].remove((n+1))
									found = True
					#if found:
						#print("Triple row " + chr(y + 65) + str(count[n][0]+1) + ", " + chr(y + 65) + str(count[n][1]+1) + ", " + chr(y + 65) + str(count[n][2]+1) + " removes " + str(n+1))
		
		return found

	def naked_pair(self):
		found = False
		for (x, y) in self.remaining:
			if self.naked_pair_column(x, y):
				found = True
			elif self.naked_pair_row(x, y):
				found = True

		return found

s = Sudoku(sudoku)
s.solve()
s.hidden_single()
print3(s.board)
