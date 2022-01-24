import pygame
import cv2
from terminate import terminate


def run_eegg():
    pygame.init()
    video = cv2.VideoCapture('./data/video/spider.mp4')
    success, video_image = video.read()
    fps = video.get(cv2.CAP_PROP_FPS)

    pygame.mixer.music.load('data/video/spider.ogg')
    pygame.mixer.music.play()
    window = pygame.display.set_mode(video_image.shape[1::-1])
    clock = pygame.time.Clock()

    run = success
    lol = True
    while run:
        clock.tick(fps)
        for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
                    terminate()
                '''if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        pygame.mixer.music.pause()
                        lol = False
                        # pygame.mixer.music.stop()
                    elif event.key == pygame.K_RETURN:
                        pygame.mixer.music.unpause()
                        lol = True
                        # pygame.mixer.music.play()'''

        if lol:
            success, video_image = video.read()
            if success:
                video_surf = pygame.image.frombuffer(
                    video_image.tobytes(), video_image.shape[1::-1], "BGR")
            else:
                run = False
        window.blit(video_surf, (0, 0))
        pygame.display.flip()