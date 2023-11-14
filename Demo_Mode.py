import pygame
import screeninfo
import cv2

def demo_mode(screen, clock, WIDTH, HEIGHT):
    video = cv2.VideoCapture("./img/demo.mp4")
    success, video_image = video.read()
    fps = video.get(cv2.CAP_PROP_FPS)
    # window = pygame.display.set_mode(video_image.shape[1::-1])

    QUIT = False
    AWAKE = False
    run = success
    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                QUIT = True
            if event.type == pygame.KEYDOWN or event.type == pygame.MOUSEBUTTONDOWN:
                run = False
                AWAKE = True
            if event.type == pygame.WINDOWRESIZED:
                x_scale = screen.get_width() / WIDTH
                y_scale = screen.get_height() / HEIGHT
                WIDTH *= x_scale
                HEIGHT *= y_scale
            
        success, video_image = video.read()
        if success:
            video_surf = pygame.image.frombuffer(video_image.tobytes(), video_image.shape[1::-1], "BGR")
        else:
            run = False
        video_surf = pygame.transform.smoothscale(video_surf, (WIDTH, HEIGHT))

        screen.blit(video_surf, (0,0))
        clock.tick(fps)
        pygame.display.update()

    return AWAKE, QUIT

if __name__ == "__main__":
    for m in screeninfo.get_monitors():
        if m.is_primary:
            monitor = m
    INITIAL_SIZE = (int(monitor.width * 0.8), int(monitor.height * 0.8)) 
    WIDTH = INITIAL_SIZE[0]
    HEIGHT = INITIAL_SIZE[1]
    
    screen = pygame.display.set_mode(INITIAL_SIZE, pygame.RESIZABLE)
    clock = pygame.time.Clock()
    pygame.display.set_caption("Untitled Jet Game")
    demo_mode(screen, clock, WIDTH, HEIGHT)
    pygame.quit()
    exit()