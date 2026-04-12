import sys
import os
import pygame

sys.path.append(os.path.dirname(__file__))
from src.game import Game
from src.start_scene import StartScene
from src.create_character_scene import CreateCharacterScene
from data.config import SCREEN_WIDTH, SCREEN_HEIGHT, FPS


def main():
    # 初始化pygame
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("北科校园物语")
    
    # 字体初始化
    font = None
    font_path = os.path.join(os.path.dirname(__file__), 'fonts', 'msyh.ttf')
    try:
        if os.path.exists(font_path):
            font = pygame.font.Font(font_path, 24)
        else:
            font = pygame.font.SysFont('SimHei', 24)
    except:
        font = pygame.font.Font(None, 24)
    
    large_font = None
    try:
        if os.path.exists(font_path):
            large_font = pygame.font.Font(font_path, 36)
        else:
            large_font = pygame.font.SysFont('SimHei', 36)
    except:
        large_font = pygame.font.Font(None, 36)
    
    # 时钟
    clock = pygame.time.Clock()
    
    current_scene = 'START_SCENE'
    character = None
    
    while True:
        if current_scene == 'START_SCENE':
            start_scene = StartScene(screen)
            running = True
            while running:
                events = pygame.event.get()
                for event in events:
                    if event.type == pygame.QUIT:
                        running = False
                        break
                
                next_scene = start_scene.handle_events(events)
                start_scene.update()
                start_scene.draw()
                
                if next_scene == 'CREATE_CHARACTER_SCENE':
                    running = False
                    current_scene = 'CREATE_CHARACTER_SCENE'
                elif next_scene == 'GAME_SCENE':
                    running = False
                    current_scene = 'GAME_SCENE'
                
                pygame.display.flip()
                clock.tick(FPS)
        
        elif current_scene == 'CREATE_CHARACTER_SCENE':
            create_scene = CreateCharacterScene(screen, font, large_font)
            character = None
            running = True
            while running:
                events = pygame.event.get()
                for event in events:
                    if event.type == pygame.QUIT:
                        running = False
                        current_scene = 'START_SCENE'
                
                character = create_scene.handle_events(events)
                create_scene.update()
                create_scene.draw()
                pygame.display.flip()
                clock.tick(FPS)
                
                if character:
                    running = False
                    current_scene = 'GAME_SCENE'
                elif not running:
                    current_scene = 'START_SCENE'
        
        elif current_scene == 'GAME_SCENE':
            game = Game(character)
            game.run()
            break


if __name__ == "__main__":
    main()
