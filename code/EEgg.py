import pygame
import cv2
from code.functions.terminate import terminate

# Функция проигрывание видео
def run_eegg():
    pygame.init()
    video = cv2.VideoCapture('../data/video/spider.mp4')
    success, video_image = video.read()
    fps = video.get(cv2.CAP_PROP_FPS)
    # Получает количество кадров видео

    # Подключение звука из видео
    pygame.mixer.music.load('../data/video/spider.ogg')
    pygame.mixer.music.play()
    window = pygame.display.set_mode(video_image.shape[1::-1])
    clock = pygame.time.Clock()

    run = success
    lol = True
    while run:
        clock.tick(fps)
        # Обновляем экран с частотой кардов из видео
        for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
                    terminate()
                # В пасхалке нет позможности поставить видео на паузу
                # чтобы выйти из пасхалки ты должен посмотреть видео полностью
                # но это функция паузы сделана код закоменчен ниже
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
            # Отображение текущего кадра
            success, video_image = video.read()
            if success:
                video_surf = pygame.image.frombuffer(
                    video_image.tobytes(), video_image.shape[1::-1], "BGR")
            else:
                run = False
        window.blit(video_surf, (0, 0))
        pygame.display.flip()