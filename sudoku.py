# https://www.lfd.uci.edu/~gohlke/pythonlibs/#curses
import sys,os
import curses
import numpy as np
import time

def solve():
	candInit()
	intersection()
	nakedSingle()
	hiddenSingle()
	return 0

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
		if  -1 < r < 3: r1, r2 = 0, 3
		elif 2 < r < 6: r1, r2 = 3, 6
		elif 5 < r < 9: r1, r2 = 6, 9
		if  -1 < c < 3: c1, c2 = 0, 3
		elif 2 < c < 6: c1, c2 = 3, 6
		elif 5 < c < 9: c1, c2 = 6, 9
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

def sg_ind(ind):
	if   ind == 0: return 0, 0
	elif ind == 1: return 0, 1
	elif ind == 2: return 0, 2
	elif ind == 3: return 1, 0
	elif ind == 4: return 1, 1
	elif ind == 5: return 1, 2
	elif ind == 6: return 2, 0
	elif ind == 7: return 2, 1
	elif ind == 8: return 2, 2

def nakedSingle(): # If cell has only one candidate, set cell to candidate
	for r, row in enumerate(n):
		for c, cell in enumerate(row):
			if np.count_nonzero(n[r,c]) == 1:
				if m[r,c] == 0:
					m[r,c] = n[r,c,n[r,c]!=0][0]
					print('NAKED')

def hiddenSingle(): # If cell cand is exclusive in region, set to cand
	x = 0
	while x<9:
		rowCount = np.bincount(n[x].ravel())
		rowCount[0] = 0
		if np.nonzero(rowCount):
			for num in np.where(rowCount==1)[0]:	## Find lone number 'num'
				for cell, cands in enumerate(n[x]): ## Loop thru cands for each cell in row
					if cands[num-1]:				## If num in cands:
						m[x,cell] = num
						print('ROW')
						return
			
		colCount = np.bincount(n[:,x].ravel())
		colCount[0] = 0
		if np.nonzero(colCount):
			for num in np.where(colCount==1)[0]:
				for cell, cands in enumerate(n[:,x]):
					if cands[num-1]:
						m[cell,x] = num
						print('COLUMN')
						return

		subgCount = np.bincount(sg(n, x, i = 1).ravel())
		subgCount[0] = 0
		if np.nonzero(subgCount):
			for num in np.where(subgCount==1)[0]:
				for cell, cands in enumerate(sg(n, x, i = 1).reshape(9,9)):
					if cands[num-1]:		
						sg(m, x, i = 1)[sg_ind(cell)] = num
						print('SUBG')
						return
		x += 1

def errorCheck():
	x = 0
	while x<9:
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
		x += 1
	return 0


m = np.zeros((9,9), dtype=int)
n = np.zeros((9,9,9), dtype=int)
n[:,:]=[1,2,3,4,5,6,7,8,9]

topDiv = '┏━━━┯━━━┯━━━┳━━━┯━━━┯━━━┳━━━┯━━━┯━━━┓'
div    = '┠┄┄┄┼┄┄┄┼┄┄┄╂┄┄┄┼┄┄┄┼┄┄┄╂┄┄┄┼┄┄┄┼┄┄┄┨'
midDiv = '┣━━━┿━━━┿━━━╋━━━┿━━━┿━━━╋━━━┿━━━┿━━━┫'
botDiv = '┗━━━┷━━━┷━━━┻━━━┷━━━┷━━━┻━━━┷━━━┷━━━┛'

def row(r):
	return '┃ {} ┊ {} ┊ {} ┃ {} ┊ {} ┊ {} ┃ {} ┊ {} ┊ {} ┃'.format(
		m[r,0],m[r,1],m[r,2],m[r,3],m[r,4],
		m[r,5],m[r,6],m[r,7],m[r,8]).replace('0',' ')

def draw(scr):
	scr.nodelay(1)
	key = -1
	curX = 2
	curY = 1

	scr.clear()
	scr.refresh()
	curses.init_pair(1, curses.COLOR_BLACK, curses.COLOR_WHITE)
	curses.init_pair(2, curses.COLOR_WHITE, curses.COLOR_RED)
	keystr = ''
	error = 0
	while key != 113:
		
		scr.clear()

		height, width = scr.getmaxyx()

		if key == curses.KEY_DOWN:
			curY = curY + 2
		elif key == curses.KEY_UP:
			curY = curY - 2
		elif key == curses.KEY_RIGHT:
			curX = curX + 4
		elif key == curses.KEY_LEFT:
			curX = curX - 4					

		curX = max(2, min(34, curX))
		curY = max(1, min(17, curY))

		curXg = int((curX-2)/4)
		curYg = int((curY-1)/2)

		# if str(key).isdigit() and key != '0':
		if 48 < key < 58:
			m[curYg, curXg] = int(key-48)
		elif key in (48,32,8,330):
			m[curYg, curXg] = 0
		elif key in (10,459):
			solve()

		if 99 == 99:

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

		if errorCheck():
			errorString = 'ERROR: Invalid Configuration'
			scr.attron(curses.color_pair(2))
			scr.addstr(height-3, 0, errorString)
			scr.addstr(height-3, len(errorString), " " * (width - len(errorString) - 1))
			scr.attroff(curses.color_pair(2))

		if key != -1:
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
		scr.addstr(19,0,keystr)

		statusbarstr = "Press 'q' to exit | Press ENTER to solve"
		scr.attron(curses.color_pair(1))
		scr.addstr(height-1, 0, statusbarstr)
		scr.addstr(height-1, len(statusbarstr), " " * (width - len(statusbarstr) - 1))
		scr.attroff(curses.color_pair(1))

		scr.move(curY, curX)
		scr.refresh()

		key = scr.getch()

def main():
	curses.wrapper(draw)
	input()

if __name__ == "__main__":
	main()