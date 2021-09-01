import pygame
import files.csvfile as csvfile
import files.shuffle as shuffle
import glob
import os
import sys

def abs_path(rel_path):
    return os.path.join(os.getcwd(), rel_path)

def scale_same_aspect(image, width = None, height = None, noblank = False):
    if (width == None) and (height == None):
        raise ValueError
    size = [100,100]
    if width == None:
        resize_aspect = height / image.get_height()
    elif height == None:
        resize_aspect = width / image.get_width()
    else:
        resize_aspect_1 = width / image.get_width()
        resize_aspect_2 = height / image.get_height()
        print([resize_aspect_1, resize_aspect_2])
        if noblank:
            resize_aspect = resize_aspect_1 if resize_aspect_2 < resize_aspect_1 else resize_aspect_2
        else:
            resize_aspect = resize_aspect_1 if resize_aspect_1 < resize_aspect_2 else resize_aspect_2
    size[0] = int(image.get_width() * resize_aspect)
    size[1] = int(image.get_height() * resize_aspect)
    return pygame.transform.scale(image, size)

def draw_background(main_color = (100,100,100), sub_color = (50, 50, 150)):
    global screen
    global HEIGHT
    global WIDTH
    screen.fill(main_color)
    screen_height = HEIGHT
    for i in range(int(WIDTH / 5 + HEIGHT / 5)):
        point_list = [[(i * 5),0], [(i * 5) + 1, 0], [(i * 5) - screen_height + 1, screen_height], [(i * 5) - screen_height, screen_height]]
        pygame.draw.polygon(screen, sub_color, point_list)

def rearrange_list_index(index, org_list):
    if abs(index) >= len(org_list):
        index = index / abs(index) * (abs(index) % len(org_list))
    rearranged_index = index
    if index < 0:
        rearranged_index = len(org_list) + index
    return int(rearranged_index)

pygame.init()

username = os.environ['USERNAME']

try:
    if os.path.isdir(sys.argv[1]):
        PHOTOS_DIR = sys.argv[1]
        print("Opening ", end = "")
    elif os.path.isfile(sys.argv[1]):
        PHOTOS_DIR = os.path.split(sys.argv[1])[0]
        opened_filepath = sys.argv[1]
        print("Opening ", end = "")
    else:
        print("Invalid argument received. opening default folder ", end = "")
        PHOTOS_DIR = "C:\\Users\\" + username + "\\Pictures\\"
except:
    print("No argument received. opening default folder ", end = "")
    PHOTOS_DIR = "C:\\Users\\" + username + "\\Pictures\\"

photos_path_list = []
print(PHOTOS_DIR + "......", end = "")

for photo in glob.glob(PHOTOS_DIR + "*.jpg"):
    photos_path_list.append(photo)

for photo in glob.glob(PHOTOS_DIR + "*.png"):
    photos_path_list.append(photo)
print(str(len(photos_path_list)) + "photos loaded")

if len(photos_path_list)==0:
    print("no  photos loaded, exiting software...")
    quit()

print("initializing screen......", end = "")
WIDTH = 768
HEIGHT = 512

screen = pygame.display.set_mode((WIDTH, HEIGHT),pygame.RESIZABLE)

myclock = pygame.time.Clock()
myfont = pygame.font.Font(None, 32)

state = "normal"
time_from_last_change = 1
try:
    photo_index = photos_path_list.index(opened_filepath)
except:
    photo_index = 0
wallpaper_now_org = pygame.image.load(photos_path_list[photo_index])
wallpaper_now = scale_same_aspect(wallpaper_now_org, width = WIDTH, height = HEIGHT)

last_photo_index = photo_index
length_photos = len(photos_path_list)

print("done")
print("load complete")

photo_scale = 1
photo_position = [0,0]

clicking = False

while state != "end":
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            state = "end"
        if event.type == pygame.VIDEORESIZE:
            WIDTH = event.w
            HEIGHT = event.h
            wallpaper_now = scale_same_aspect(wallpaper_now_org, width = WIDTH, height = HEIGHT)
            screen = pygame.display.set_mode((event.w, event.h),pygame.RESIZABLE)
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT:
                photo_index -= 1
            if event.key == pygame.K_RIGHT:
                photo_index += 1
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                clicking = True
                dragging = False
        if event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:
                if dragging == False:
                    photo_index += 1
                else:
                    dragging = False
                clicking = False
            if event.button == 3:
                photo_index -= 1
            if event.button == 4:
                photo_scale *= 1.1
                wallpaper_now = scale_same_aspect(wallpaper_now_org, width = WIDTH * photo_scale, height = HEIGHT * photo_scale)
            if event.button == 5:
                photo_scale /= 1.1
                wallpaper_now = scale_same_aspect(wallpaper_now_org, width = WIDTH * photo_scale, height = HEIGHT * photo_scale)
        if event.type == pygame.MOUSEMOTION:
            if clicking == True:
                dragging = True
                photo_position[0] += event.rel[0]
                photo_position[1] += event.rel[1]
    
    photo_index = rearrange_list_index(photo_index, photos_path_list)
    if photo_index != last_photo_index:
        wallpaper_now_org = pygame.image.load(photos_path_list[photo_index])
        wallpaper_now = scale_same_aspect(wallpaper_now_org, width = WIDTH, height = HEIGHT)
        photo_scale = 1
        photo_position = [0,0]
    
    screen.fill((100,100,100))
    screen.blit(wallpaper_now, (WIDTH / 2 - wallpaper_now.get_width() / 2 + photo_position[0], HEIGHT / 2 - wallpaper_now.get_height() / 2 + photo_position[1]))
    picture_index_text = myfont.render(str(photo_index + 1) + "/" + str(length_photos), False, (255,255,255), (0,0,0))
    screen.blit(picture_index_text, (0,0))
    pygame.display.flip()
    myclock.tick(60)
    last_photo_index = photo_index

pygame.quit()
