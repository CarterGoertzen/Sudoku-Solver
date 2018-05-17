# https://www.lfd.uci.edu/~gohlke/pythonlibs/#curses
import sys,os
import curses
import numpy as np


def solve():
	candInit()
	intersection()
	singleCand()
	return

def candInit():
	for r, row in enumerate(m):
		for c, cell in enumerate(row):
			if cell != 0:
				n[r,c] = 0

def intersection():
	for r, row in enumerate(m):
		for c, cell in enumerate(row):
			if cell != 0:
				n[r,:,cell-1] = 0
				n[:,c,cell-1] = 0
				sg(n,r,c)[:,:,cell-1] = 0

def sg(arr, r, c = None, i = 0):
	if i == 0:
		if -1<r<3: r1, r2 = 0, 3
		elif 2<r<6: r1, r2 = 3, 6
		elif 5<r<9: r1, r2 = 6, 9
		if -1<c<3: c1, c2 = 0, 3
		elif 2<c<6: c1, c2 = 3, 6
		elif 5<c<9: c1, c2 = 6, 9
	else:
		if r == 0:   r1, r2, c1, c2 = 0, 3, 0, 3
		elif r == 1: r1, r2, c1, c2 = 0, 3, 3, 6
		elif r == 2: r1, r2, c1, c2 = 0, 3, 6, 9
		elif r == 3: r1, r2, c1, c2 = 3, 6, 0, 3
		elif r == 4: r1, r2, c1, c2 = 3, 6, 3, 6
		elif r == 5: r1, r2, c1, c2 = 3, 6, 6, 9
		elif r == 6: r1, r2, c1, c2 = 6, 9, 0, 3
		elif r == 7: r1, r2, c1, c2 = 6, 9, 3, 6
		elif r == 8: r1, r2, c1, c2 = 6, 9, 6, 9
	return arr[r1:r2, c1:c2]

def singleCand(): # If cell has only one candidate, set cell to candidate
	for r, row in enumerate(n):
		for c, cell in enumerate(row):
			if np.count_nonzero(n[r,c]) == 1:
				if m[r,c] == 0:
					m[r,c] = n[r,c,n[r,c]!=0][0]

def loneCand(): ##VERY WRONG
	x = 0
	while x<1:
		rowCount = np.bincount(n[x].ravel())
		rowCount[0] = 0
		if np.nonzero(rowCount):
			for num in np.where(rowCount==1)[0]:
				print(num)

			

		x += 1

def errorCheck():
	x = 0
	while x<8:
		row = set(m[x])
		row.discard(0)
		col = set(m[:,x])
		col.discard(0)
		subg = set(sg(m, x, i = 1).ravel())
		subg.discard(0)

		if np.count_nonzero(m[x]) != len(row) \
		or np.count_nonzero(m[:,x]) != len(col) \
		or np.count_nonzero(sg(m, x, i = 1)) != len(subg):
			return 1
		else:
			return 0
		x += 1

m = np.zeros((9,9), dtype=int)
n = np.zeros((9,9,9), dtype=int)
n[:,:]=[1,2,3,4,5,6,7,8,9]

def row(r):
	return '┃ {} ┊ {} ┊ {} ┃ {} ┊ {} ┊ {} ┃ {} ┊ {} ┊ {} ┃'.format(
		m[r][0],m[r][1],m[r][2],m[r][3],m[r][4],
		m[r][5],m[r][6],m[r][7],m[r][8]).replace('0',' ')

topDiv = '┏━━━┯━━━┯━━━┳━━━┯━━━┯━━━┳━━━┯━━━┯━━━┓'
div    = '┠┄┄┄┼┄┄┄┼┄┄┄╂┄┄┄┼┄┄┄┼┄┄┄╂┄┄┄┼┄┄┄┼┄┄┄┨'
midDiv = '┣━━━┿━━━┿━━━╋━━━┿━━━┿━━━╋━━━┿━━━┿━━━┫'
botDiv = '┗━━━┷━━━┷━━━┻━━━┷━━━┷━━━┻━━━┷━━━┷━━━┛'

def draw(scr):

	key = '0'
	curX = 2
	curY = 1

	scr.clear()
	scr.refresh()
	curses.init_pair(1, curses.COLOR_BLACK, curses.COLOR_WHITE)

	while key != 'q':
		scr.clear()

		height, width = scr.getmaxyx()

		if key == 'KEY_DOWN':
			curY = curY + 2
		elif key == 'KEY_UP':
			curY = curY - 2
		elif key == 'KEY_RIGHT':
			curX = curX + 4
		elif key == 'KEY_LEFT':
			curX = curX - 4					

		curX = max(2, min(34, curX))
		curY = max(1, min(17, curY))

		curXg = int((curX-2)/4)
		curYg = int((curY-1)/2)

		if str(key).isdigit() and key != '0':
			m[curYg][curXg] = int(key)
		elif key in (' ','KEY_DC','\b','0'):
			m[curYg][curXg] = 0
		elif key == '\n':
			solve()
		elif key == 'c':

			candString = 'Candidates for R'+str(curYg+1)+'C'+str(curXg+1)+': '
			# candList = list(cands[curYg][curXg])
			candList = list(n[curYg,curXg])
			for cand in candList:
				if cand != 0:
					candString += (str(cand)+', ')
			if not candList:
				candString += 'None'
			candString = candString.rstrip(', ')

			scr.attron(curses.color_pair(1))
			scr.addstr(height-2, 0, candString)
			scr.addstr(height-2, len(candString), " " * (width - len(candString) - 1))
			scr.attroff(curses.color_pair(1))

		keystr = "Last key pressed: {}".format(str(key))
		if key == 0:
			keystr = "No key press detected..."
		scr.addstr(0,0,topDiv)
		scr.addstr(1,0,row(0))
		scr.addstr(2,0,div)
		scr.addstr(3,0,row(1))
		scr.addstr(4,0,div)
		scr.addstr(5,0,row(2))
		scr.addstr(6,0,midDiv)
		scr.addstr(7,0,row(3))
		scr.addstr(8,0,div)
		scr.addstr(9,0,row(4))
		scr.addstr(10,0,div)
		scr.addstr(11,0,row(5))
		scr.addstr(12,0,midDiv)
		scr.addstr(13,0,row(6))
		scr.addstr(14,0,div)
		scr.addstr(15,0,row(7))
		scr.addstr(16,0,div)
		scr.addstr(17,0,row(8))
		scr.addstr(18,0,botDiv)
		# scr.addstr(19,0,keystr)
		# scr.addstr(20,0,str(curXg))
		# scr.addstr(21,0,str(curYg))

		statusbarstr = "Press 'q' to exit | Press ENTER to solve | Press c to display cell candidates"
		scr.attron(curses.color_pair(1))
		scr.addstr(height-1, 0, statusbarstr)
		scr.addstr(height-1, len(statusbarstr), " " * (width - len(statusbarstr) - 1))
		scr.attroff(curses.color_pair(1))

		scr.move(curY, curX)
		scr.refresh()

		key = scr.getkey()


def main():
	curses.wrapper(draw)
	loneCand()
	input()
if __name__ == "__main__":
	main()


# print('┏━━━┯━━━┯━━━┳━━━┯━━━┯━━━┳━━━┯━━━┯━━━┓')
# print('┃ 1 │ 2 │ 3 ┃ 1 │ 2 │ 3 ┃ 1 │ 2 │ 3 ┃')
# print('┠───┼───┼───╂───┼───┼───╂───┼───┼───┨')
# print('┃ 1 │ 2 │ 3 ┃ 1 │ 2 │ 3 ┃ 1 │ 2 │ 3 ┃')
# print('┠───┼───┼───╂───┼───┼───╂───┼───┼───┨')
# print('┃ 1 │ 2 │ 3 ┃ 1 │ 2 │ 3 ┃ 1 │ 2 │ 3 ┃')
# print('┣━━━┿━━━┿━━━╋━━━┿━━━┿━━━╋━━━┿━━━┿━━━┫')
# print('┃ 1 │ 2 │ 3 ┃ 1 │ 2 │ 3 ┃ 1 │ 2 │ 3 ┃')
# print('┠───┼───┼───╂───┼───┼───╂───┼───┼───┨')
# print('┃ 1 │ 2 │ 3 ┃ 1 │ 2 │ 3 ┃ 1 │ 2 │ 3 ┃')
# print('┠───┼───┼───╂───┼───┼───╂───┼───┼───┨')
# print('┃ 1 │ 2 │ 3 ┃ 1 │ 2 │ 3 ┃ 1 │ 2 │ 3 ┃')
# print('┣━━━┿━━━┿━━━╋━━━┿━━━┿━━━╋━━━┿━━━┿━━━┫')
# print('┃ 1 │ 2 │ 3 ┃ 1 │ 2 │ 3 ┃ 1 │ 2 │ 3 ┃')
# print('┠───┼───┼───╂───┼───┼───╂───┼───┼───┨')
# print('┃ 1 │ 2 │ 3 ┃ 1 │ 2 │ 3 ┃ 1 │ 2 │ 3 ┃')
# print('┠───┼───┼───╂───┼───┼───╂───┼───┼───┨')
# print('┃ 1 │ 2 │ 3 ┃ 1 │ 2 │ 3 ┃ 1 │ 2 │ 3 ┃')
# print('┗━━━┷━━━┷━━━┻━━━┷━━━┷━━━┻━━━┷━━━┷━━━┛')

# cands = [0]*9
# for x, z in enumerate(cands):
# 	cands[x] = [0]*9
# 	for y, z in enumerate(cands[x]):
# 		cands[x][y] = {1,2,3,4,5,6,7,8,9}

# def intersection(): #UPDATE
# 	for r, row in enumerate(m):
# 		for c, cell in enumerate(row):
# 			if cell != ' ':
# 				for col in cands[r]:
# 					col.discard(cell)
# 				for row in cands:
# 					row[c].discard(cell)				
# 				for cells in subgridReturn(subgridCheck(r,c)):
# 					if cells != []:
# 						cells.discard(cell)

# def subgridCheck(r,c): #UPDATE
# 	s = None
# 	if -1<c<3:  s = 0
# 	if 2<c<6:  s = 1
# 	if 5<c<9: s = 2
# 	if 2<r<6:  s += 3
# 	if 5<r<9: s += 6
# 	return s

# def subgridReturn(s): #UPDATE
# 	if s == 0: return [cands[0][0],cands[0][1],cands[0][2],cands[1][0],cands[1][1],cands[1][2],cands[2][0],cands[2][1],cands[2][2]]
# 	if s == 1: return [cands[0][3],cands[0][4],cands[0][5],cands[1][3],cands[1][4],cands[1][5],cands[2][3],cands[2][4],cands[2][5]]
# 	if s == 2: return [cands[0][6],cands[0][7],cands[0][8],cands[1][6],cands[1][7],cands[1][8],cands[2][6],cands[2][7],cands[2][8]]
# 	if s == 3: return [cands[3][0],cands[3][1],cands[3][2],cands[4][0],cands[4][1],cands[4][2],cands[5][0],cands[5][1],cands[5][2]]
# 	if s == 4: return [cands[3][3],cands[3][4],cands[3][5],cands[4][3],cands[4][4],cands[4][5],cands[5][3],cands[5][4],cands[5][5]]
# 	if s == 5: return [cands[3][6],cands[3][7],cands[3][8],cands[4][6],cands[4][7],cands[4][8],cands[5][6],cands[5][7],cands[5][8]]
# 	if s == 6: return [cands[6][0],cands[6][1],cands[6][2],cands[7][0],cands[7][1],cands[7][2],cands[8][0],cands[8][1],cands[8][2]]
# 	if s == 7: return [cands[6][3],cands[6][4],cands[6][5],cands[7][3],cands[7][4],cands[7][5],cands[8][3],cands[8][4],cands[8][5]]
# 	if s == 8: return [cands[6][6],cands[6][7],cands[6][8],cands[7][6],cands[7][7],cands[7][8],cands[8][6],cands[8][7],cands[8][8]]
# 	else: return []

# def singleCand(): # If cell has only one candidate, set cell to candidate #UPDATE
# 	for r, row in enumerate(cands):
# 		for c, cell in enumerate(row):
# 			if len(cell) == 1:
# 				if m[r][c] == ' ':
# 					m[r][c] = cell.copy().pop()