import picodisplay as display

width = display.get_width()
height = display.get_height()

display_buffer = bytearray(width * height * 2)  # 2-bytes per pixel (RGB565)
display.init(display_buffer)
display.set_backlight(1.0)

sprite_width = 66
sprite_height = 42


def load_image_to_buffer (filename, framebuffer):
    with open (filename, "rb") as file:
        position = 0
        position_x = 0
        position_y = 0
        
        while position_y < (sprite_height):
            while position_x < (sprite_width):
                current_byte_h = file.read(1)
                current_byte_l = file.read(1)

                # if eof
                if len(current_byte_h) == 0:
                    break

                # copy to buffer
                framebuffer[position] = ord(current_byte_h)
                framebuffer[position+1] = ord(current_byte_l)  
                
                position += 2
                position_x += 1
            
            position_x = 0
            position_y += 1
            
    file.close()


# This is based on a binary image file (RGB565)
# The image is with a dimensions of: sprite_width x sprite_height 
# updates the global display_buffer directly
def blit_image_file(buffer, x, y):
    global display_buffer

    position = x + y * width * 2
    position_x = 0
    position_y = 0
    idx = 0
    
    while position_y < (sprite_height):
        while position_x < (sprite_width):
            current_byte_h = buffer[idx]
            current_byte_l = buffer[idx+1]

            # copy to buffer
            if (current_byte_h == ord(b'\x07') and current_byte_l == ord(b'\xe0')):
                pass
            else:
                #print(current_byte_h, current_byte_l)
                display_buffer[position] = current_byte_h
                display_buffer[position+1] = current_byte_l  
            
            idx += 2
            position += 2
            position_x += 1
        
        position_x = 0
        position_y += 1
        position = x + (y + position_y) * width * 2
            

rainbow = [(255,0,0),(255,152,0),(255,255,0),(0,255,0),(0,152,255),(101,50,255)]

def draw_rainbow(count):
    for j in range(6):
        for i in range(6):
            display.set_pen(rainbow[i][0], rainbow[i][1], rainbow[i][2])
            display.rectangle(100 - 20 * j, ((j+count)%2)*3 + 6*i + 40, 20, 6)


stream = ["frame1.raw", "frame2.raw", "frame3.raw", "frame4.raw", "frame5.raw", "frame6.raw"]

sprite_size = sprite_width * sprite_height * 2
buffer = []


# load all images into buffer (to improve performance)
for i in range(len(stream)):
    buffer.append(bytearray(sprite_size))
    load_image_to_buffer(stream[i], buffer[i])
    

# Do nothing - but continue to display the image
while True:
    
    count = 0
    
    for i in range(len(stream)):
        display.set_pen(9, 20, 230);
        display.clear()           # Fill the screen with the colour
        
        draw_rainbow(count)       # rainbow as background
        blit_image_file(buffer[i], 180, 40)
        count += 1
        
        # (optional) control on-board RGB led
        #c = count % 6
        #display.set_led(rainbow[c][0], rainbow[c][1], rainbow[c][2])
        
        # update screen
        display.update()
        
