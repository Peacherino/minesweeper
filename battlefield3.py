from fltk import *

WIDTH = 10
HEIGHT = 10
CELL_SIZE = 100
NUM_BOMBS = 10
NUM_CELLS = WIDTH * HEIGHT
# sizings and amount of items in the game

class Field(Fl_Window):

    # constructor
    def __init__(self, x, y, w, h, title):
        super().__init__(x, y, w, h, title)
        self.begin()
        # group for resizable gird of buttons
        grid_group = Fl_Group(0, 0, WIDTH * CELL_SIZE, HEIGHT * CELL_SIZE)
        grid_group.begin()
        self.buttons = [] # store all buttons
        self.button_grid = {} # dictionary for all x, y positions of each button
        self.revealed_count = 0
        self.timer_value = 0
        self.timer_running = False
        self.bomb_image = Fl_JPEG_Image("bomb.jpg").copy(CELL_SIZE, CELL_SIZE)
        # create button grid for all x, y positions
        for x in range(WIDTH):
            for y in range(HEIGHT):
                minibutton = Fieldbutton(self, x, y, x*CELL_SIZE, y*CELL_SIZE, CELL_SIZE, CELL_SIZE)
                self.buttons.append(minibutton)
                self.button_grid[(x, y)] = minibutton
        # buttons now all in grid_group and resizable along with the window
        grid_group.end()
        self.resizable(grid_group)
        # box with amount of flags placed
        self.flag_count = NUM_BOMBS
        self.flag_label = Fl_Box(WIDTH * CELL_SIZE // 2 - 50, 1010, 100, 30, str(self.flag_count))
        self.flag_label.labelcolor(FL_RED)
        self.flag_label.labelsize(20)
        self.flag_label.box(FL_FLAT_BOX)
        # button that reveals all buttons (for debugging, current position hidden)
        self.show_all = ShowAllButton(self, 1010, 700, 100, 20, "show all")
        # box for a timer to count time
        self.timer_label = Fl_Box(70, HEIGHT * CELL_SIZE + 10, 100, 30, "0")
        self.timer_label.box(FL_UP_BOX)
        self.start_timer()
        self.place_bombs()
        self.end()
        self.show()

    # restarts game at original sizing
    def restart_game(self):
        self.hide()
        new_game = Field(0, 0, WIDTH * CELL_SIZE, HEIGHT * CELL_SIZE + 50, "Minesweeper")
        Fl.run()

    # timer for time of game
    def start_timer(self):
        self.timer_running = True
        self.update_timer()

    def update_timer(self):
        if not self.timer_running:
            return
        self.timer_value += 1
        self.timer_label.label(str(self.timer_value))
        Fl.add_timeout(1.0, self.update_timer)

    # all my bombs places randomly
    def place_bombs(self):
        import random
        positions = [(i, j) for i in range(WIDTH) for j in range(HEIGHT)]
        random.shuffle(positions)
        bomb_positions = positions[:NUM_BOMBS]
        for pos in bomb_positions:
            self.button_grid[pos].is_bomb = True

    # losing the game
    def game_over(self):
        print("game over")
        self.timer_running = False
        # gets time count
        elapsed_time = self.timer_value
        # all images now revealed/stay the same
        for button in self.buttons:
            button.update_images()
        # gives time count
        fl_message(f"You lose!\nTimetaken: {elapsed_time} seconds")
        self.redraw()
        self.restart_game()

    # same mechanics as game over
    def game_win(self):
        print("game win")
        self.timer_running = False
        elapsed_time = self.timer_value
        for button in self.buttons:
            button.showing = True
            button.update_images()
        fl_message(f"You win!\nTimetaken: {elapsed_time} seconds")
        self.redraw()
        self.restart_game()

# shows all my buttons if need be
# no longer necessary
class ShowAllButton(Fl_Button):
    def __init__(self, app, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.app = app
        self.callback(self.on_click)

    def on_click(self, widget):
        for button in self.app.buttons:
            button.reveal()

# representative for each cell in grid
class Fieldbutton(Fl_Button):

    # constructor
    def __init__(self, field, grid_x, grid_y, x, y, w, h):
        super().__init__(x, y, w, h)
        self.grid_x = grid_x # x-coord in grid
        self.grid_y = grid_y # y-coord in grid
        self.field = field
        self.is_bomb = False
        self.is_flagged = False
        self.showing = False
        self.button_id = f"({self.grid_x}, {self.grid_y})"
        self.flag_image = Fl_PNG_Image("flag.png")
        self.flag_image = self.flag_image.copy(CELL_SIZE, CELL_SIZE)

    # handles all the mouse events
    def handle(self, event):
        if event == FL_PUSH:
            if Fl.event_button() == FL_RIGHT_MOUSE:
                self.toggle_flag()
                return 1
            elif Fl.event_button() == FL_LEFT_MOUSE:
                if self.is_bomb:
                    self.field.game_over()
                else:
                    self.reveal()
                return 1
        return super().handle(event)

    # handles resizing of window and updates images accordingly
    def resize(self, x, y, w, h):
        super().resize(x, y, w, h)
        # print('i resized', x, y, w, h)
        self.update_images()

    # takes care of every image update for a button based on the cell's individual states
    def update_images(self):
        if self.is_flagged:
            # flag incorrect after gameover
            if not self.field.timer_running and not self.is_bomb:
                self.image(None)
                self.label("X")
                self.labelcolor(FL_RED)
            else:
                # correct flag during/after game
                resized_flag = self.flag_image.copy(self.w(), self.h())
                self.image(resized_flag)
                self.label(None)
        elif self.showing:
            # cell is revealed and bomb and not flagged
            if self.is_bomb:
                resized_bomb = self.field.bomb_image.copy(self.w(), self.h())
                self.image(resized_bomb)
                self.label(None)
            # cell has no interesting attributes
            elif self.numbombs == 0:
                self.image(None)
                #self.label("empty")
            else:
                # not a bomb then show neighbour bombs
                self.image(None)
                self.label(str(self.numbombs()) if self.numbombs() > 0 else " ")
                # bombs after gameover
        elif not self.field.timer_running:
            if self.is_bomb:
                resized_bomb = self.field.bomb_image.copy(self.w(), self.h())
                self.image(resized_bomb)
                self.label(None)
            # leftover button that has nothing
            else:
                self.image(None)
                self.label("empty")
        else:
            # default state for unrevealed cells
            self.image(None)
            self.label(None)
        self.redraw()

    # flagging of cell on and off
    # also adjusts flag_count number as flag toggles
    def toggle_flag(self):
        if self.showing:
            return
        self.is_flagged = not self.is_flagged
        self.update_images()
        if self.is_flagged:
            self.field.flag_count -= 1
        else:
            self.field.flag_count += 1

        self.field.flag_label.label(str(self.field.flag_count))
        self.field.flag_label.redraw()
        self.redraw()
        # self.update_images()


    # reveals cell(s)
    def reveal(self):
        if self.showing:
            return
        if not self.is_flagged:
            self.showing = True
            self.field.revealed_count += 1
            # this is an epic win
            if self.field.revealed_count == NUM_CELLS - NUM_BOMBS:
                self.field.game_win()
            # if it's a bomb
            if self.is_bomb:
                resized_bomb = self.field.bomb_image.copy(self.w(), self.h())
                self.image(resized_bomb)
                self.redraw()
            else:
                # recurse for empty neighbours until they kiss neighbours that have bomb neighbours and then we stop there
                if self.numbombs() == 0:
                    self.label("empty")
                    for neighbour in self.getneighbours():
                        neighbour.reveal()
                else:
                    self.label(f'{self.numbombs()}')
            self.redraw()

    # counts bomb neighbours
    def numbombs(self):
        count = 0
        for neighbour in self.getneighbours():
            if neighbour.is_bomb:
                count += 1
        return count

    # will tell you what the neighbours of the button are
    # it's not necessary but it's here
    def getneighbours(self):
        print(f"Clicked on {self.button_id}")
        neighbours = []
        for dx in [-1, 0, 1]:
            for dy in [-1, 0, 1]:
                if dx == 0 and dy == 0:
                    continue
                nx = self.grid_x + dx
                ny = self.grid_y + dy
                if 0 <= nx < WIDTH and 0 <= ny < HEIGHT:
                    neighbour_button = self.field.button_grid.get((nx, ny))
                    if neighbour_button:
                        neighbours.append(neighbour_button)
        print(f"Neighbours of {self.button_id}: {[n.button_id for n in neighbours]}")
        return neighbours

# initializes and allows game to run hooray
app = Field(0, 0, WIDTH * CELL_SIZE, HEIGHT * CELL_SIZE + 100, "minesweeper")
Fl.run()


