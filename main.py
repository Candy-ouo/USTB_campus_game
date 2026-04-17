import sys
import os

# 禁用 libpng 的 iCCP 警告
class DevNull:
    def write(self, *args): pass
    def flush(self): pass

# 重定向stderr以忽略libpng警告
old_stderr = sys.stderr
sys.stderr = DevNull()

# 然后导入 pygame
import pygame

sys.path.append(os.path.dirname(__file__))
from src.game import Game
from src.start_scene import StartScene
from src.create_character_scene import CreateCharacterScene
from src.save_system import SaveSystem
from data.config import SCREEN_WIDTH, SCREEN_HEIGHT, FPS


def main():
    # 初始化pygame
    pygame.init()
    # 创建不可调整大小的窗口（默认就是不可调整的）
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
                    character = None

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
                    # 删除旧存档（如果有的话）
                    save_system = SaveSystem()
                    if save_system.has_save_file():
                        save_system.delete_save()
                    # 直接进入游戏场景
                    print(f"传递给Game的character参数: {character}")
                    game = Game(character, screen)
                    game.run()
                    break
                elif not running:
                    if current_scene != 'GAME_SCENE':
                        current_scene = 'START_SCENE'

        elif current_scene == 'GAME_SCENE':
            save_system = SaveSystem()
            if save_system.has_save_file():
                print(f"读档进入游戏")
                character = save_system.load_character_from_save()
                game = Game(character, screen)
                success, msg = save_system.load_game(game)
                if success:
                    print(msg)
                game.run()
            else:
                print("没有存档，自动进入新游戏")
                current_scene = 'CREATE_CHARACTER_SCENE'
                continue
            break


if __name__ == "__main__":
    main()
