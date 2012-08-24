import pygame
import random

# Define some colors
black    = (   0,   0,   0)
white    = ( 255, 255, 255)
green    = (   0, 255,   0)
red      = ( 255,   0,   0)
yellow   = ( 255,   255, 0)
purple   = ( 255,   0, 255)

FACE_WIDTH = 40
SEGMENT_WIDTH = 35
STEP = 2
MIN_X = 0
MAX_X = 1000
FOOD_WIDTH = 15
EAT_WIDTH = 5

class caterpillar:
    def __init__(self):
        x = random.randrange(0,1000)
        self.face_xcoord = x
        self.face_ycoord = 250
        self.body = segment_queue()
        self.food = food_list()
        self.wellbeing = 0
        self.need_shrink = False
        t = random.randrange(0,2)
        if t == 0:
            self.travel_direction = 'left'
        else:
            self.travel_direction = 'right'
        
    def draw_caterpillar(self, screen):
        self.draw_face(screen)
        self.draw_body(screen)
        self.draw_food(screen)

    def draw_face(self, screen):
        x = self.face_xcoord 
        y = self.face_ycoord
        pygame.draw.ellipse(screen,red,[x, y, 40, 45])
        pygame.draw.ellipse(screen,black,[x+6, y+10, 10, 15])
        pygame.draw.ellipse(screen,black,[x+24, y+10, 10, 15])
        pygame.draw.line(screen,black, (x+11, y), (x+9, y-10), 3)
        pygame.draw.line(screen,black, (x+24, y), (x+26, y-10), 3)
        
    def draw_body(self, screen):
        #traverse the segment queue
        if self.need_shrink:
            self.shrink_back()
        current_node = self.body.head
        count = 0
        while current_node is not None:
            count += 1
            if self.wellbeing > 1:
                current_node.draw_segment(screen, yellow) 
            elif self.wellbeing < -1:
                current_node.draw_segment(screen, [purple, black][count % 2])
            else:
                current_node.draw_segment(screen) 
            current_node = current_node.next 
           
    def draw_food(self, screen):
        #traverse the segment queue
        current_node = self.food.head
        while current_node is not None:
            current_node.draw_fooditem(screen) 
            current_node = current_node.next 
           
    def grow(self):
        segment_x = 0
        segment_y = self.face_ycoord
        if self.travel_direction == "left":
            if self.body.length == 0:
                segment_x = self.face_xcoord + FACE_WIDTH
            else:
                segment_x = self.body.last.xcoord + SEGMENT_WIDTH
        else:
            if self.body.length == 0:
                segment_x = self.face_xcoord - SEGMENT_WIDTH
            else:
                segment_x = self.body.last.xcoord - SEGMENT_WIDTH
        self.body.addSegment(segment_x, segment_y)
        

    def reverse(self):
        self.body.reverse()
        if self.travel_direction == "left":
            self.travel_direction = "right"
            self.face_xcoord = self.body.head.xcoord + SEGMENT_WIDTH
        else:
            self.travel_direction = "left"
            self.face_xcoord = self.body.head.xcoord - FACE_WIDTH

    def eat_food(self):
        if self.food.length == 0:
            return
        if self.food.length == 1:
            curfood = self.food.head
            if abs(self.face_xcoord - curfood.xcoord) <= FOOD_WIDTH - 5:
                if curfood.is_nice_food():
                    self.wellbeing += 1
                else:
                    self.wellbeing -= 1
                    if self.wellbeing == -2:
                        self.need_shrink = True
                self.food.empty_list()
                return

        curfood = self.food.head
        prev = curfood
        while curfood:
            if abs(self.face_xcoord - curfood.xcoord) <= FOOD_WIDTH - 5:
                if curfood.is_nice_food():
                    self.wellbeing += 1
                else:
                    self.wellbeing -= 1
                    if self.wellbeing == -2:
                        self.need_shrink = True
                if self.food.head == curfood:
                    self.food.head = curfood.next
                    curfood = curfood.next
                    prev = curfood
                    self.food.length -= 1
                else:
                    prev.next = curfood.next
                    curfood = curfood.next
                    self.food.length -= 1
            else:
                prev = curfood
                curfood = curfood.next
                    

    
    def move_forward(self):
        if self.body.isEmpty():
            return

        if self.travel_direction == "left":
            if self.face_xcoord <= MIN_X:
                self.reverse()
                return

            self.face_xcoord -= STEP
            self.body.change_coord(x=-STEP)
        else:
            if self.face_xcoord >= MAX_X - FACE_WIDTH:
                self.reverse()
                return
            self.face_xcoord += STEP
            self.body.change_coord(x=STEP)
        self.eat_food()
                
    def drop_food(self):
        food_x = random.randrange(0, 980)
        food_y = random.randrange(self.face_ycoord - FOOD_WIDTH, self.face_ycoord + FACE_WIDTH)
        food_type = "nice" if random.randrange(0,2) == 0 else "nasty"
        self.food.add_item(food_x, food_y, food_type)

        
    def shrink_back(self):
        self.need_shrink = False
        self.body.remove_first_segement()
        if self.body.length > 0 :
            if self.travel_direction == "left":
                self.face_xcoord += SEGMENT_WIDTH
            else:
                self.face_xcoord -= SEGMENT_WIDTH
    
class segment_queue:
    def __init__(self):
        self.length = 0
        self.head = None
        self.last = None
      
    def isEmpty(self):
        return self.length == 0

    def remove_first_segement(self):
        if self.length == 0:
            return
        self.head = self.head.next
        self.length -= 1
      
    def addSegment(self, x, y): 
        segment = body_segment(x, y)
        if not self.head:
            self.head = segment
            self.last = segment
            self.length = 1
        else:
            lastnode = self.last
            self.last = segment
            lastnode.next = self.last
            self.length += 1

    def change_coord(self, x=0, y=0):
        cur = self.head
        while cur:
            cur.xcoord += x
            cur.ycoord += y
            cur = cur.next


    def reverse(self):
        if self.length == 0:
            return

        self.last = self.head
        cur = self.head
        left = cur
        cur = cur.next
        while cur:
            temp = cur.next
            cur.next = left
            left = cur
            cur = temp

        self.head = left
        self.last.next = None

        
class body_segment:
    def __init__(self, x, y):
        self.xcoord = x
        self.ycoord = y
        self.next = None
        
    def draw_segment(self, screen, fill=green):
        x = self.xcoord
        y = self.ycoord
        pygame.draw.ellipse(screen,fill,[x, y, 35, 40])
        pygame.draw.line(screen,black, (x+8, y+35), (x+8, y+45), 3)
        pygame.draw.line(screen,black, (x+24, y+35), (x+24, y+45), 3)
        
class food_list:
    def __init__(self):
        self.length = 0
        self.head = None

    def empty_list(self):
        self.length = 0
        self.head = None

    def add_item(self, x, y, ftype):
        item = food_item(x, y, ftype)
        if not self.head:
            self.head = item
            self.length = 1
        else:
            cur = self.head
            left = cur
            while cur:
                left = cur
                cur = cur.next
            left.next = item
            self.length += 1
        
class food_item:
    def __init__(self, x, y, kind):
        self.xcoord = x
        self.ycoord = y
        self.foodtype = kind
        self.next = None   

    def is_nice_food(self):
        return self.foodtype == "nice"
        
    def draw_fooditem(self, screen):
        x = self.xcoord
        y = self.ycoord
        if self.foodtype == 'nice':
            pygame.draw.ellipse(screen,yellow,[x, y, 15, 15])
        else:
            pygame.draw.ellipse(screen,purple,[x, y, 15, 15])
