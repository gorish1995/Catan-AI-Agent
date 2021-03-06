"""
This is the node class which deals with the intersections
of any tile in the board. It will be the primary point
for functionality in the game.
"""


class Node:
    def __init__(self, row, col):
        self.row = row
        self.col = col
        self.touchingTiles = []
        self.neighbours = []
        self.isOccupied = False
        self.occupyingPiece = None
        self.port = None

    def __str__(self):
        printStr = "Node: (" + str(self.row) + ", " + str(self.col) + ")"
        return printStr

    def get_occupying_piece(self):
        return self.occupyingPiece

    def is_occupied(self):
        return self.isOccupied

    def get_tiles(self):
        return self.touchingTiles

    def set_occupying_piece(self, piece):
        self.isOccupied = True
        self.occupyingPiece = piece

    def set_neighbours(self, board):
        neighbours = board.getNeighborNodes(self.row, self.col)
        toSet = []
        for coord in neighbours:
            toSet.append(board.nodes[coord[0]][coord[1]])
        self.neighbours = toSet

class Board:
  
    def __init__(self):
        self.nodes = {0: [Node(0, i) for i in range(7)],
                      1: [Node(1, i) for i in range(9)],
                      2: [Node(2, i) for i in range(11)],
                      3: [Node(3, i) for i in range(11)],
                      4: [Node(4, i) for i in range(9)],
                      5: [Node(5, i) for i in range(7)]}
        self.tiles = []

        # Loop over all the nodes and define neighbors
        for rowNum, row in self.nodes.items():
            for node in row:
                node.set_neighbours(self)

        #Setup ports
        self.init_ports()
        

    def init_ports(self):
        self.nodes[0][0].port = "Any"
        self.nodes[0][1].port = "Any"

        self.nodes[0][3].port = "Wool"
        self.nodes[0][4].port = "Wool"

        self.nodes[1][7].port = "Any"
        self.nodes[1][8].port = "Any"

        self.nodes[1][0].port = "Ore"
        self.nodes[2][0].port = "Ore"
        
        self.nodes[2][1].port = "Any"
        self.nodes[3][1].port = "Any"

        self.nodes[3][0].port = "Grain"
        self.nodes[4][0].port = "Grain"

        self.nodes[4][7].port = "Brick"
        self.nodes[4][8].port = "Brick"
        
        self.nodes[5][0].port = "Any"
        self.nodes[5][1].port = "Any"

        self.nodes[5][3].port = "Wood"
        self.nodes[5][4].port = "Wood"
        
        
    # Check whether a node is in bounds
    def inBounds(self, node):
        return node[0] >= 0 and node[0] < len(self.nodes.keys()) and node[1] >= 0 and node[1] < len(self.nodes[node[0]])

    # Get the given node
    def getNode(self, node):
        r, c = node
        return self.nodes[r][c]

    # Set a nodes touching tiles
    def setTouchingTiles(self, tile):
        # Takes a tile object
        tr, tc = tile.id
        if tr < 2:
            br, bc = (tr + 1, tc + 1)
        elif tr == 2:
            br, bc = (tr + 1, tc)
        else:
            br, bc = (tr + 1, tc - 1)

        for i in range(-1, 2):
            node = self.nodes[tr][tc + i]
            node.touchingTiles.append(tile)

        for i in range(-1, 2):
            node = self.nodes[br][bc + i]
            node.touchingTiles.append(tile)

    # Get a nodes neighbours
    def getNeighborNodes(self, r, c):
        if r < 2:
            if c % 2 == 0:
                neighbors = [(r, c - 1), (r, c + 1), (r + 1, c + 1)]
            else:
                neighbors = [(r - 1, c - 1), (r, c - 1), (r, c + 1)] 
        elif r == 2:
            if c % 2 == 0:
                neighbors = [(r, c - 1), (r, c + 1), (r + 1, c)]
            else:
                neighbors = [(r, c - 1), (r, c + 1), (r - 1, c - 1)] 
        elif r == 3:
            if c % 2 == 0:
                neighbors = [(r, c - 1), (r, c + 1), (r - 1, c)]
            else:
                neighbors = [(r, c + 1), (r, c - 1), (r + 1, c - 1)] 
        else:
            if c % 2 == 0:
                neighbors = [(r, c - 1), (r, c + 1), (r - 1, c + 1)]
            else:
                neighbors = [(r + 1, c - 1), (r, c - 1), (r, c + 1)]
        inBoundsNeighbors = []
        for n in neighbors:
            if self.inBounds(n):
                inBoundsNeighbors.append(n)
        return inBoundsNeighbors

    # Get neighbouring edges
    def getNeighborEdges(self, edge):
        one = edge[0]
        two = edge[1]
        nOne = self.getNeighborNodes(one)
        nTwo = self.getNeighborNodes(two)
        nEdgesOne = [(one, n) for n in nOne]
        nEdgesTwo = [(two, n) for n in nTwo]
        return nEdgesOne + nEdgesTwo 

    # Get a given tiles nodes
    def getNodesForTile(self, tile):
        # Let each tile have an identifier = the node coord at its peak
        # Return the 6 nodes at that tile's corners
        r, c = tile.id
        return [(r, c - 1), (r, c), (r, c + 1), \
                (r + 1, c - 1), (r + 1, c), (r + 1, c + 1)]

    # Get a node from co-ordinates
    def getNodeFromCoords(self, r, c):
        node = (r, c)
        if self.inBounds(node):
            return self.nodes[r][c]
        else:
            return None

    # Get a tile for the node
    def getTileForNode(self, r, c):
        for tile in self.tiles:
            if tile.id == (r, c):
                return tile
        return None

# Defines the tile class
class Tile:
    def __init__(self, resource, value, has_robber, id):
        self.resource = resource
        self.value = value
        self.hasRobber = has_robber
        self.id = id