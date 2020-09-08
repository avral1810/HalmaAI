import copy
import time
import math


class Node:
	def __init__(self,state,parent,cost):
		self.parent = parent
		self.cost = cost
		self.state = state


class DataHolder:

	def __init__(self,fileName):
		self.board = []
		with open(fileName) as inputFile:
			lines = inputFile.readlines()
			self.gameMode = lines[0][0:-1]
			self.playerColor = lines[1][0:-1]
			self.givenTime = float(lines[2][0:-1])
			for i in range(3,19):
				if i != 18:
					self.board.append(lines[i][0:-1])
				else:
					self.board.append(lines[i])


class Game: #white 1 Black 2
	

	def __init__(self, inputData):
		self.timeOut = 1
		self.start_time = time.time()
		self.bestMove = None

		self.bottomRightCorner = (
			(15,15),(15,14),(15,13),(15,12),(15,11),
			(14,15),(14,14),(14,13),(14,12),(14,11),
			(13,15),(13,14),(13,13),(13,12),
			(12,15),(12,14),(12,13),
			(11,15),(11,14))
		self.topLeftCorner = (
			(0,0),(0,1),(0,2),(0,3),(0,4),
			(1,0),(1,1),(1,2),(1,3),(1,4),
			(2,0),(2,1),(2,2),(2,3),
			(3,0),(3,1),(3,2),
			(4,0),(4,1))

		self.inputData = inputData

		self.blackPawns = []
		self.whitePawns = []

		for i in range(16):
			for j in range(16):
				if self.inputData.board[i][j] == "B":
					temp = (i,j)
					self.blackPawns.append(temp)
				if self.inputData.board[i][j] == "W":
					temp = (i,j)
					self.whitePawns.append(temp)


	def isWhiteWinner(self, currentBoard):
		
		winner = 0
		i = 0
		while i < 5:
			if i == 0:
				j = 0
				while j < 5:
					
					if currentBoard[i][j] == 0:
						winner = 0
						return 0
					elif currentBoard[i][j] == 1:
						winner = 1
					j += 1
			else:
				j = 0
				while j < 6 - i:
					if currentBoard[i][j] == 0:
						winner = 0
						return 0
					elif currentBoard[i][j] == 1:
						winner = 1
					j += 1
			i += 1

		return winner

	def isBlackWinner(self, currentBoard):
		
		winner = 0
		i = 11
		while i < 16:
			if i == 15:
				j = 11
				while j < 16:
					if currentBoard[i][j] == 0:
						winner = 0
						return 0
					elif currentBoard[i][j] == 2:
						winner = 2
					j += 1
			else:
				j = 25 - i
				while j < 16:
					if currentBoard[i][j] == 0:
						winner = 0
						return 0
					elif currentBoard[i][j] == 2:
						winner = 2
					j += 1
			i += 1

		return winner


	def createBoard(self, currBlack, currWhite):
		board = [[0] * 16 for i in range(16)]
		for pawn in currBlack:
			board[pawn[0]][pawn[1]] = 2
		for pawn in currWhite:
			board[pawn[0]][pawn[1]] = 1
		return board


	def print(self,currWhite, currBlack):
		print("Black Pawns")
		for i in currBlack:
			print(i,end = " ")
		print("")
		print("White Pawns")
		for i in currWhite:
			print(i,end = " ")
		print("")


	def findMoves(self, pawn, currBlack, currWhite):

		moves = []
		for i in range(-1, 2):
			for j in range(-1, 2):
				if( i == 0 and j == 0):
					continue
				posx = pawn[0] + i
				posy = pawn[1] + j
				if not ( posx < 0 or posx >= 16 or posy < 0 or posy >= 16 ):
					if ((posx, posy) not in currBlack):
						if((posx, posy) not in currWhite):
							moves.append((posx,posy))

		for jump in self.findJumps(pawn, [pawn], currBlack, currWhite):
			move = jump
			moves.append(jump)
		return moves


	def findJumps(self, pawn, path, currBlack, currWhite):
		moves = []
		for i in range(-1, 2):
			for j in range(-1, 2):
				if( i == 0 and j == 0):
					continue
				posx = pawn[0] + 2*i
				posy = pawn[1] + 2*j
				if not ( posx < 0 or posx >= 16 or posy < 0 or posy >= 16 ):
					if ((posx, posy) not in currBlack):
						if((posx, posy) not in currWhite):
							jumpx = pawn[0] + i
							jumpy = pawn[1] + j
							if not ( jumpx < 0 or jumpx >= 16 or jumpy < 0 or jumpy >= 16 ):
								if((jumpx,jumpy) != pawn):
									if ((jumpx,jumpy) in currBlack) or ((jumpx,jumpy) in currWhite):
										if (posx, posy) not in path:
											path.append((pawn[0], pawn[1]))
											jumps = self.findJumps((posx, posy), path, currBlack, currWhite)
											for jump in jumps:
												moves.append(jump)
											moves.append((posx,posy))
		return moves



	def findAllMoves(self, playerPawns, currBlack, currWhite, maximizer ,moves_as_coords=False):
		moves = {}
		count = 0
		
		if maximizer:
			move_count_for_inside_pawn = 0
			for pawn in playerPawns:
				if pawn in self.topLeftCorner:
					count += 1
			for pawn in playerPawns:
				onePawn = []
				if count < 19 and count > 0:
					if pawn in self.topLeftCorner:
						for move in self.findMoves(pawn, currBlack, currWhite):
							if (move[0] - pawn[0]) + (move[1] - pawn[1]) > 0: 
								move_count_for_inside_pawn += 1
								onePawn.append(move)
				else:
					for move in self.findMoves(pawn, currBlack, currWhite):
						onePawn.append(move)
				moves[pawn] = onePawn

			for pawn in playerPawns:
				onePawn = []
				if move_count_for_inside_pawn == 0:
					if pawn not in self.topLeftCorner:
						for move in self.findMoves(pawn, currBlack, currWhite):
							onePawn.append(move)
				temp = moves[pawn]
				onePawn += temp
				moves[pawn] = onePawn
		else:
			move_count_for_inside_pawn = 0
			for pawn in playerPawns:
				if pawn in self.bottomRightCorner:
					count += 1
			for pawn in playerPawns:
				onePawn = []
				if count < 19 and count > 0:
					if pawn in self.bottomRightCorner:
						for move in self.findMoves(pawn, currBlack, currWhite):
							if (move[0] - pawn[0]) + (move[1] - pawn[1]) < 0:
								move_count_for_inside_pawn += 1
								onePawn.append(move)
				else:
					for move in self.findMoves(pawn, currBlack, currWhite):
						onePawn.append(move)
				moves[pawn] = onePawn
			for pawn in playerPawns:
				onePawn = []
				if move_count_for_inside_pawn == 0:
					if pawn not in self.topLeftCorner:
						for move in self.findMoves(pawn, currBlack, currWhite):
							onePawn.append(move)
				temp = moves[pawn]
				onePawn += temp
				moves[pawn] = onePawn
		return moves


	def isEnd(self, currBlack, currWhite):
		currentBoard = self.createBoard(currBlack, currWhite)
		white = self.isWhiteWinner(currentBoard)
		if white != 0:
			return white
		return self.isBlackWinner(currentBoard)

	def evaluation(self, currBlack, currWhite, maximizer):
		value = 0		
		for e in currBlack:
			value += (e[0] - 15) + (e[1] - 15)

		for e in currWhite:
			value += (e[0] + e[1])

		if maximizer:
			return ((value),((-1,-1),(-1,-1)))
		else:
			return ((value),((-1,-1),(-1,-1)))

	def isMoveValid(self,pawn,move, currBlack, currWhite, maximizer):


		moveLoc = "neutral"
		pawnLoc = "neutral"
		if maximizer:
			if pawn in currBlack:
				pawnLoc = "home"
			elif pawn in currWhite:
				pawnLoc = "goal"
			if move in currBlack:
				moveLoc = "home"
			elif move in currWhite:
				moveLoc = "goal"
		else:
			if pawn in currWhite:
				pawnLoc = "home"
			elif pawn in currBlack:
				pawnLoc = "goal"
			if move in currWhite:
				moveLoc = "home"
			elif move in currBlack:
				moveLoc = "goal"

		if pawnLoc == "goal" and moveLoc != "goal":
			return False
		
		if (pawnLoc == "neutral" or pawnLoc == "goal") and moveLoc == "home":
			return False

		return True


	def alphaBetaPlayer(self, depth, currBlack, currWhite, maximizer, alpha, beta, maxDepth):
		if depth == maxDepth or self.isEnd(currBlack,currWhite):
			return self.evaluation(currBlack, currWhite, maximizer)
		if maximizer:
			best = -1000000
			all_valid_moves = self.findAllMoves(currBlack,currBlack,currWhite,maximizer)
			for init_pawn,all_moves_for_that_pawn in all_valid_moves.items():
				for one_move in all_moves_for_that_pawn:
					newCurrBlack = copy.deepcopy(currBlack)
					newCurrBlack.remove(init_pawn)
					newCurrBlack.append(one_move)

					value,temp = self.alphaBetaPlayer(depth + 1, newCurrBlack, currWhite, False, alpha, beta, maxDepth)
					if value > best: 
						best = value
						bestMove = (init_pawn,one_move)
					if best > alpha:
						alpha = best
					if beta <= alpha:
						break
			return best,bestMove
		else:
			best = 1000000
			all_valid_moves = self.findAllMoves(currWhite,currBlack,currWhite,maximizer)
			for init_pawn,all_moves_for_that_pawn in all_valid_moves.items():
				for one_move in all_moves_for_that_pawn:
					newCurrWhite = copy.deepcopy(currWhite)
					newCurrWhite.remove(init_pawn)
					newCurrWhite.append(one_move)

					value,temp = self.alphaBetaPlayer(depth + 1, currBlack, newCurrWhite, True, alpha, beta, maxDepth)
					if value < best:
						best = value
						bestMove = (init_pawn,one_move)
					if best < beta:
						beta = best

					if beta <= alpha:
						break
			return (best,bestMove)
					



	def getRouteNeighbors(self,parent,final_pawn,currBlack,currWhite):
		neighbors = []
		
		for i in range(-1,2):
			for j in range(-1,2):
				if i == 0 and j == 0:
					continue
				posx = parent.state[0] + 2*i
				posy = parent.state[1] + 2*j
				if not ( posx < 0 or posx >= 16 or posy < 0 or posy >= 16 ):
					if ((posx, posy) not in currBlack):
						if((posx, posy) not in currWhite):
							jumpx = parent.state[0] + i
							jumpy = parent.state[1] + j
							if not ( jumpx < 0 or jumpx >= 16 or jumpy < 0 or jumpy >= 16 ):
								if ((jumpx,jumpy) in currBlack) or ((jumpx,jumpy) in currWhite):
									temp = Node((posx,posy),parent,parent.cost + 1)
									neighbors.append(temp)
		return neighbors


	def getJumpRoute(self,init_pawn,final_pawn,currBlack,currWhite):
		pathQueue = []
		visited = []
		aNode = Node(init_pawn, None, 0)
		pathQueue.append(aNode)
		while pathQueue:
			poppedNode = pathQueue.pop(0)
			if poppedNode.state[0] == final_pawn[0] and poppedNode.state[1] == final_pawn[1]:
				return poppedNode
			else:
				neighbors = self.getRouteNeighbors(poppedNode,final_pawn,currBlack,currWhite)
				for each_neighbor in neighbors:
					if each_neighbor not in visited:
						pathQueue.append(each_neighbor)
						visited.append(each_neighbor)
		return None




	def play(self):
		
		if self.inputData.gameMode == "SINGLE":
			move_type = "J"
			depth = 3
			if self.inputData.givenTime < 10:
				depth = 2
			elif self.inputData.givenTime < 2:
				depth = 1
			if self.inputData.playerColor == "BLACK":
				value, move = self.alphaBetaPlayer(0,self.blackPawns,self.whitePawns,True,-1000000,1000000,depth)
			else:
				value, move = self.alphaBetaPlayer(0,self.blackPawns,self.whitePawns,False,-1000000,1000000,depth)
			init_pawn, final_pawn = move
			for i in range(-1,2):
				for j in range(-1,2):
					if (i == 0 and j == 0):
						continue
					posx = init_pawn[0] + i
					posy = init_pawn[1] + j
					if (posx,posy) == final_pawn:
						move_type = "E"
						break
			
			if move_type == "J":
				route = self.getJumpRoute(init_pawn,final_pawn,self.blackPawns,self.whitePawns)
				locations = []
				while route.parent is not None:
					locations.append(route.state)
					route = route.parent
				locations.append(init_pawn)
				locations.reverse()
				output_string = ""
				for i in range(0,len(locations) - 1):	
					output_string += "J " + str(locations[i][1]) + "," + str(locations[i][0]) + " " + str(locations[i+1][1]) + "," + str(locations[i+1][0]) + "\n"
				output_string = output_string[0:-1]
			else:
				output_string = "E " + str(init_pawn[1]) + "," + str(init_pawn[0]) + " " + str(final_pawn[1]) + "," +str(final_pawn[0])
			with open('output.txt','w') as opfile:
				opfile.write(output_string)
		else:
			move_type = "J"
			depth = 3
			if self.inputData.givenTime < 40:
				depth = 2
			elif self.inputData.givenTime < 10:
				depth = 1
			if self.inputData.playerColor == "BLACK":
				reward = 0
				for each in self.blackPawns:
					if each in self.bottomRightCorner:
						reward += 2
					else:
						if each[0] > 7 and each[1] > 7:
							reward += 1
				if depth == 3 and reward < 25:
					depth = 2
				value, move = self.alphaBetaPlayer(0,self.blackPawns,self.whitePawns,True,-1000000,1000000,depth)
			else:
				reward = 0
				for each in self.whitePawns:
					if each in self.topLeftCorner:
						reward += 2
					else:
						if each[0] < 7 and each[1] < 7:
							reward += 1
				if depth == 3 and reward < 25:
					depth = 2
				value, move = self.alphaBetaPlayer(0,self.blackPawns,self.whitePawns,True,-1000000,1000000,depth)
			init_pawn, final_pawn = move
			for i in range(-1,2):
				for j in range(-1,2):
					if (i == 0 and j == 0):
						continue
					posx = init_pawn[0] + i
					posy = init_pawn[1] + j
					if (posx,posy) == final_pawn:
						move_type = "E"
						break
			
			if move_type == "J":
				route = self.getJumpRoute(init_pawn,final_pawn,self.blackPawns,self.whitePawns)
				locations = []
				while route.parent is not None:
					locations.append(route.state)
					route = route.parent
				locations.append(init_pawn)
				locations.reverse()
				output_string = ""
				for i in range(0,len(locations) - 1):	
					output_string += "J " + str(locations[i][1]) + "," + str(locations[i][0]) + " " + str(locations[i+1][1]) + "," + str(locations[i+1][0]) + "\n"
				output_string = output_string[0:-1]
			else:
				output_string = "E " + str(init_pawn[1]) + "," + str(init_pawn[0]) + " " + str(final_pawn[1]) + "," +str(final_pawn[0])
			with open('output.txt','w') as opfile:
				opfile.write(output_string)




inputData = DataHolder("input.txt")
game = Game(inputData)
game.play()