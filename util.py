BLACK = (0, 0, 0)
GRAY = (178, 178, 178)
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
LBLUE = (144, 215, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
YELLOW = (255, 255, 0)
BROWN =  (153, 76, 0)
WBROWN =  (123, 76, 0)
DBROWN = ( 91, 66, 61)
CBROWN = (79, 57, 47)

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

def renderText(screen,font,text,text_x,text_y,color):
    message = font.render(text, True, color)
    message_rect = message.get_rect()
    x = screen.get_width() / 2 - message_rect.width / 2
    y = screen.get_height() / 2 - message_rect.height / 2
    screen.blit(message, [x + text_x, y + text_y])