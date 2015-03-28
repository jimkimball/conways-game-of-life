
class OutOfBoundsException(Exception):
    pass

class Grid:
    def __init__(self, dim_x, dim_y):
        self.__dimensions = (dim_x, dim_y)
        self.__alive_cells = []
    
    def dimensions(self):
        return self.__dimensions
    
    def is_alive(self, x, y):
        return self.__alive_cells.__contains__((x,y))
    
    def is_valid_cell(self, x, y):
        return x >= 0 and y >= 0 and x <= self.__dimensions[0] and y <= self.__dimensions[1]
    
    def set_alive(self, x, y):
        if not self.is_valid_cell(x, y):
            raise OutOfBoundsException("Tried to build %d,%d")
        self.__alive_cells.append((x,y))
        
    def neighbors(self, x, y):
        return self.row_above(x, y) + self.same_row(x, y) + self.row_below(x,y)
        

    def live_neighbor_count(self, x, y):
        live_neighbors = 0
        for cell in self.neighbors(x, y):
            if self.is_alive(cell[0], cell[1]):
                live_neighbors += 1
        
        return live_neighbors

    def has_fewer_than_two_live_neighbors(self, x, y):
        return self.live_neighbor_count(x, y) < 2
    
    def has_two_or_three_live_neighbors(self, x, y):
        count = self.live_neighbor_count(x, y)
        return count == 2 or count == 3
    
    def same_row(self, x, y):
        return self.make_cell(x-1,y) + self.make_cell(x+1, y)
    
    def make_cell(self, x, y):
        if self.is_valid_cell(x, y):
            return [(x,y)]
        return []
    
    def row_above(self, x, y):
        return self.make_cell(x-1,y-1) + self.make_cell(x, y-1) + self.make_cell(x+1, y-1)

    def row_below(self, x, y):
        return self.make_cell(x-1,y+1) + self.make_cell(x, y+1) + self.make_cell(x+1, y+1)

    def has_more_than_three_live_neighbors(self, x, y):
        return self.live_neighbor_count(x, y) > 3
    
    def has_exactly_three_live_neighbors(self, x, y):
        return self.live_neighbor_count(x, y) == 3
    
    def interesting_dead_cell_list(self):
        interesting_dead_cells = set()
        for cell in self.__alive_cells:
            for neighbor_cell in self.neighbors(cell[0], cell[1]):
                if not self.is_alive(neighbor_cell[0], neighbor_cell[1]):
                    interesting_dead_cells.add((neighbor_cell[0], neighbor_cell[1]))
        return list(interesting_dead_cells)
            
    def live_cells(self):
        return self.__alive_cells
    
    def is_empty(self):
        return len(self.__alive_cells) == 0
    
    def iterate_grid(self):
        dying_cells = []
        spawning_cells = []
        for cell in self.__alive_cells:
            if not self.has_two_or_three_live_neighbors(cell[0], cell[1]):
                dying_cells.append(cell)
                
        for cell in self.interesting_dead_cell_list():
            if self.has_exactly_three_live_neighbors(cell[0], cell[1]):
                spawning_cells.append(cell)
                
        for cell in dying_cells:
            self.__alive_cells.remove(cell)
            
        self.__alive_cells.extend(spawning_cells)
                
        return (spawning_cells, dying_cells)
    
    def create_grid(self, list_of_cells):
        for cell in list_of_cells:
            self.set_alive(cell[0], cell[1])
