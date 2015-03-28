from Game.grid import Grid, OutOfBoundsException
import unittest


class Test(unittest.TestCase):
    def setUp(self):
        self.g = Grid(10, 10)
        
    def create_grid(self, list_of_cells):
        self.g.create_grid(list_of_cells)

    def testGridKnowsHowManyCellsItHas(self):
        self.assertEquals((10,10), self.g.dimensions())

    def testInitialGridIsAllDead(self):
        (dim_x, dim_y) = self.g.dimensions()
        for x in xrange(0, dim_x):
            for y in xrange(0,dim_y):
                self.assertFalse(self.g.is_alive(x,y))
                
    def testCanSetInitialState(self):
        self.g.set_alive(1,1)
        self.assertTrue(self.g.is_alive(1,1))
        
    def testCantSetStateOutsideOfDimensions(self):
        self.assertRaises(OutOfBoundsException, self.g.set_alive, 20, 20)
        self.assertRaises(OutOfBoundsException, self.g.set_alive, -1, -1)
        
    def testKnowNeighborsInMiddleOfGrid(self):
        self.assertEquals([(4,4), (5,4), (6,4), (4,5), (6,5), (4, 6), (5, 6), (6,6)], self.g.neighbors(5,5))
        
    def testKnowNeighborsOnTopEdge(self):
        self.assertEquals([(4,0), (6, 0), (4,1), (5,1), (6,1)], self.g.neighbors(5,0))

    def testKnowNeighborsOnBottomEdge(self):
        self.assertEquals([(4,9), (5, 9), (6,9), (4,10), (6,10)], self.g.neighbors(5,10))
        
    def testKnownNeighborsOnLeftEdge(self):
        self.assertEquals([(0,4), (1,4), (1,5), (0,6), (1,6)], self.g.neighbors(0, 5))

    def testKnownNeighborsOnRightEdge(self):
        self.assertEquals([(9,4), (10,4), (9,5), (9,6), (10,6)], self.g.neighbors(10, 5))

    def testKnownNeighborsTopLeftCorner(self):
        self.assertEquals([(1,0), (0,1), (1,1)], self.g.neighbors(0, 0))

    def testKnownNeighborsTopRightCorner(self):
        self.assertEquals([(9,0), (9,1), (10,1)], self.g.neighbors(10, 0))

    def testKnownNeighborsBottomLeftCorner(self):
        self.assertEquals([(0,9), (1,9), (1,10)], self.g.neighbors(0, 10))

    def testKnownNeighborsBottomRightCorner(self):
        self.assertEquals([(9,9), (10,9), (9,10)], self.g.neighbors(10, 10))

    def testRuleCellHasFewerThanTwoLiveNeighbors(self):
        self.g.set_alive(1,1)
        self.assertTrue(self.g.has_fewer_than_two_live_neighbors(1,1))
        
    def testEmptyGridHasFewerThanTwoLiveNeighbors(self):
        self.assertTrue(self.g.has_fewer_than_two_live_neighbors(5, 5))
        
    def testRuleCellHasTwoLiveNeighbors(self):
        self.create_grid([(1,1), (1,2), (0,1)])
        self.assertFalse(self.g.has_fewer_than_two_live_neighbors(1, 1))
        
    def testRuleCellHasTwoOrThreeLiveNeighbors(self):
        self.create_grid([(1,1), (1,2), (0,1)])
        self.assertTrue(self.g.has_two_or_three_live_neighbors(1,1))
        
    def testRuleHasMoreThanThreeNeighbors(self):
        self.create_grid([(5,5), (4,5), (5,6), (4,4), (6,6)])
        self.assertTrue(self.g.has_more_than_three_live_neighbors(5,5))
        
    def testRuleDeadCellHasExactlyThreeLiveNeighbors(self):
        self.create_grid([(4,5), (5,6), (4,4)])
        self.assertTrue(self.g.has_exactly_three_live_neighbors(5,5))
        
    def testInterestingDeadCellListOnEmptyGrid(self):
        self.assertEquals([], self.g.interesting_dead_cell_list())

    def testInterestingDeadCellListOnOneCell(self):
        self.create_grid([(5,5)])
        self.assertItemsEqual([(4,4), (5,4), (6,4), (4,5), (6,5), (4, 6), (5, 6), (6,6)], self.g.interesting_dead_cell_list())

    def testInterestingDeadCellListOnTwoCell(self):
        self.create_grid([(5,5), (4,4)])
        self.assertItemsEqual([(3,3), (4,3), (5,3), (3,4), (3,5), (5,4), (6,4), (4,5), (6,5), (4, 6), (5, 6), (6,6)], self.g.interesting_dead_cell_list())
        
    def testInterestingDeadCellListIsEmptyOnFullGrid(self):
        live_cells = []
        for x in xrange(0,11):
            for y in xrange(0,11):
                live_cells.append((x,y))
        self.create_grid(live_cells)
        self.assertEquals([], self.g.interesting_dead_cell_list())
        
    def testIterateOnGrid(self):
        self.create_grid([(1,1), (1,2), (0,1)])
        (spawning_cells, dying_cells) = self.g.iterate_grid()
        self.assertEquals([(0,2)], spawning_cells)
        self.assertItemsEqual([], dying_cells)
        
    def testIterateOnGrid2(self):
        self.create_grid([(1,1), (1,2), (0,1), (0,2), (2,1)])
        (spawning_cells, dying_cells) = self.g.iterate_grid()
        self.assertEquals([(2,2), (1,0)], spawning_cells)
        self.assertItemsEqual([(1,1), (1,2)], dying_cells)
        
                          


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
