import sys, pygame as pg
from pygame.draw import line
"""
This file defines the table that is displayed for the Visualization
"""
pg.init()
screen_size = 850, 850
screen = pg.display.set_mode(screen_size)
font = pg.font.SysFont('FreeSans', 19, bold=True)
pg.display.set_caption('Table')
letters = ['Z','A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R','S','T','U','V','W','X','Y']
# letter_grid = [letters.append(letters.pop(0)) for i in range(26)]
letter_grid = []
for i in range (26):
    letters.append(letters.pop(0))
    new_letters = letters.copy()
    letter_grid.append(new_letters)
# print(letter_grid)


# table class draws a vigenere table and implements functionality for highlighting specific
# rows, columns, and cells in the table
class Table:
    def __init__(self):
        # self.screen is the surface that holds the table with all current highlights
        self.screen = pg.Surface(screen_size)

        # self.save is a surface that holds the blank table before any highlighting. This is
        # used in the animation to delete previous highlights in order to make new highlights
        self.save = pg.Surface(screen_size)

        # list of every single rectangular cell in the table
        self.cells = []

        # list of each of the letters in the table and their positions
        self.letters = []

        # list of letters on the edge row and their positions
        self.edgeRowLetters = []

        # list of letters on the edge column and their positions
        self.edgeColLetters = []

        # upon initialization, draws the table onto self.screen
        self.draw_background() # draw the background for the table
        self.draw_letters() # draw the letters on the table
        self.draw_edge_row() # draw the edge row letters
        self.draw_edge_col() # draw the edge column letters
        self.save.blit(self.screen, (0, 0)) # save blank table to self.save
        return None

    # refresh clears self.screen of any highlights
    def refresh(self):
        self.screen.blit(self.save, (0, 0))

    # draw_background draws the table grid
    def draw_background(self):
        self.screen.fill(pg.Color("white"))
        pg.draw.rect(self.screen, pg.Color("black"), pg.Rect(40,40,780,780),3)
        i = 1
        while (i * 30) < 810:
            line_width = 3 
            pg.draw.line(self.screen, pg.Color("black"), pg.Vector2((i * 30)+40, 40), pg.Vector2((i*30) +40, 820), line_width)
            pg.draw.line(self.screen, pg.Color("black"), pg.Vector2(40, (i * 30)+40), pg.Vector2(820, (i*30) +40), line_width)
            i += 1
        return None

    # draw_letters draws all of the letters in the table grid
    def draw_letters(self):
        row = 0
        offset = 50
        while row < 26:
            col = 0
            while col < 26:
                output = letter_grid[row][col]
                # print(str(output))
                tempRect = pg.Rect((col*30 + 42), (row * 30 + 42), 27, 27)
                pg.draw.rect(self.screen, (255, 255, 255), tempRect)
                self.cells.append(tempRect)
                n_text = font.render(str(output), True, pg.Color('black'))
                curpos = pg.Vector2((col*30 + offset - 2), (row * 30 + offset))
                self.screen.blit(n_text, curpos)
                self.letters.append((n_text, curpos))
                col += 1
            row += 1
        return None

    # draw letters along the top row above the grid 
    def draw_edge_row(self):
        edge_row = ['A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R','S','T','U','V','W','X','Y','Z']
        row = 0
        offset = 50
        while row < 26:
            output = edge_row[row]
            n_text = font.render(str(output), True, pg.Color('black'))
            pp = pg.Vector2(20, (row * 30 + offset))
            self.screen.blit(n_text, pp)
            self.edgeRowLetters.append((n_text, pp))
            row += 1
        return None

    # draw letters along the column to the left of the grid
    def draw_edge_col(self):
        edge_col = ['A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R','S','T','U','V','W','X','Y','Z']
        col = 0
        offset = 50
        while col < 26:
            output = edge_col[col]
            n_text = font.render(str(output), True, pg.Color('black'))
            pp = pg.Vector2((col * 30 + offset), 20)
            self.screen.blit(n_text, pg.Vector2((col * 30 + offset), 20))
            self.edgeColLetters.append((n_text, pp))
            col += 1
        return None

    # highlight a specific row in the table
    def highlightRow(self, row):
        offset = row * 26
        tempRect = pg.Rect(self.cells[0].left - 30, self.cells[row*26].top, 27, 27)
        pg.draw.rect(self.screen, (0, 180, 255), tempRect)
        self.screen.blit(self.edgeRowLetters[row][0], self.edgeRowLetters[row][1])
        for i in range(26):
            pg.draw.rect(self.screen, (0, 180, 255), self.cells[offset + i])
            self.screen.blit(self.letters[offset+i][0], self.letters[offset+i][1])
        return None

    # highlight a specific column
    def highlightCol(self, col):
        tempRect = pg.Rect(self.cells[col].left, self.cells[0].top - 30, 27, 27)
        pg.draw.rect(self.screen, (255, 255, 0), tempRect)
        self.screen.blit(self.edgeColLetters[col][0], self.edgeColLetters[col][1])
        for i in range(26):
            pos = i*26 + col
            pg.draw.rect(self.screen, (255, 255, 0), self.cells[pos])
            self.screen.blit(self.letters[pos][0], self.letters[pos][1])
        return None

    # Fill a specific cell in the table with a specific color
    def fill_cell(self, row, col, color):
        index = row*26 + col
        pg.draw.rect(self.screen, color, self.cells[index])
        self.screen.blit(self.letters[index][0], self.letters[index][1])
        return None

    # fill a specific letter on the edge row/column
    def fill_edge_cell(self, row, col):
        tempRect = pg.Rect(self.cells[col].left, self.cells[0].top - 30, 27, 27)
        pg.draw.rect(self.screen, (0, 255, 0), tempRect)
        self.screen.blit(self.edgeColLetters[col][0], self.edgeColLetters[col][1])
        return None

    # this function is used to make all of the necessary highlights for a single step in the
    # encryption process. It highlights the specified row, specified column, and the cell that is
    # at the intersection between the highlighted row and column
    def displayEncrypt(self, row, column):
        self.screen.blit(self.save, (0, 0))
        self.highlightRow(row)
        self.highlightCol(column)
        self.fill_cell(row, column, (0, 255, 0))
        return None

    # this function is used to make all of the necessary highlights for a single step in the
    # decryption process. It highlights the specified row, specified column, and the cell that is
    # at the intersection between the highlighted row and column, and the cell that represents the
    # location of the decrypted letter
    def displayDecrypt(self, row, column):
        self.screen.blit(self.save, (0, 0))
        self.highlightRow(row)
        self.highlightCol(column)
        self.fill_cell(row, column, (255, 80, 80))
        self.fill_edge_cell(row, column)
        return None

def main():
    table = Table()
    table.displayDecrypt(7, 12)
    while True:
        screen.blit(table.screen, (0, 0))
        events = pg.event.get()
        pressed_keys = pg.key.get_pressed()
        for event in events:
            if event.type == pg.QUIT:
                pg.quit()
        pg.display.update()


