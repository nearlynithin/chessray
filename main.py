from pyray import *


init_window(1280,720,"pyShatranj")

set_target_fps(60)

while not window_should_close():
    begin_drawing()
    
    clear_background(BLUE)
    draw_text("Konnichiwa",30,40,30,WHITE)
    
    end_drawing()
    
close_window()
    