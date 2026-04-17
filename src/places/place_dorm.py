import pygame
import os
import sys
from data.config import SCREEN_WIDTH, SCREEN_HEIGHT

class Dorm:
    def __init__(self, game):
        self.game = game
        self.screen = game.screen
        self.font = game.font
        self.large_font = game.large_font
        self.dorm_background = None
        self._load_images()

    def _load_images(self):
        """加载宿舍背景图片"""
        dorm_path = os.path.join(os.path.dirname(__file__), '..', '..', 'image', 'dorm_background.png')
        try:
            if os.path.exists(dorm_path):
                self.dorm_background = pygame.image.load(dorm_path)
        except:
            pass

    def draw(self):
        """绘制宿舍场景"""
        if self.dorm_background:
            scaled_bg = pygame.transform.scale(self.dorm_background, (SCREEN_WIDTH, SCREEN_HEIGHT))
            self.screen.blit(scaled_bg, (0, 0))
        else:
            self.screen.fill((50, 50, 50))

        option1_rect = pygame.Rect(400, 200, 500, 50)
        option2_rect = pygame.Rect(400, 280, 500, 50)
        option3_rect = pygame.Rect(400, 360, 500, 50)

        pygame.draw.rect(self.screen, (220, 180, 140), option1_rect)
        pygame.draw.rect(self.screen, (150, 100, 50), option1_rect, 2)
        self.game.draw_text("玩游戏：心情+40 行动点-1", option1_rect.x + 10, option1_rect.y + 10, (254, 247, 201))

        pygame.draw.rect(self.screen, (220, 180, 140), option2_rect)
        pygame.draw.rect(self.screen, (150, 100, 50), option2_rect, 2)
        self.game.draw_text("看书：学识+10 心情-10 行动点-1", option2_rect.x + 10, option2_rect.y + 10, (254, 247, 201))

        pygame.draw.rect(self.screen, (220, 180, 140), option3_rect)
        pygame.draw.rect(self.screen, (150, 100, 50), option3_rect, 2)
        self.game.draw_text("床：行动点+2 健康值+5", option3_rect.x + 10, option3_rect.y + 10, (254, 247, 201))

        if self.game.message_timer > 0:
            self.game.draw_text(self.game.message, SCREEN_WIDTH // 2 - 300, SCREEN_HEIGHT - 60, (254, 247, 201), self.large_font)
            self.game.message_timer -= 1

        time_display = self.game.time_system.get_time_display()
        self.game.ui_hud.draw_all(time_display, self.game.player)

    def handle_events(self, events):
        """处理宿舍场景事件"""
        option1_rect = pygame.Rect(400, 200, 500, 50)
        option2_rect = pygame.Rect(400, 280, 500, 50)
        option3_rect = pygame.Rect(400, 360, 500, 50)

        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.game.current_state = "MAIN_GAME"
                    self.game.map_system.toggle_map()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                if option1_rect.collidepoint(pos):
                    if self.game.player.action_points >= 1:
                        self.game.player.action_points -= 1
                        self.game.player.add_mood(40)
                        self.game.message = "你选择了玩游戏，心情+40，行动点-1"
                        self.game.message_timer = 90
                    else:
                        self.game.message = "行动点不足！"
                        self.game.message_timer = 60
                elif option2_rect.collidepoint(pos):
                    if self.game.player.action_points >= 1:
                        self.game.player.action_points -= 1
                        self.game.player.add_knowledge(10)
                        self.game.player.add_mood(-10)
                        self.game.message = "你选择了看书，学识+10，心情-10，行动点-1"
                        self.game.message_timer = 90
                    else:
                        self.game.message = "行动点不足！"
                        self.game.message_timer = 60
                elif option3_rect.collidepoint(pos):
                    if not self.game.has_rested:
                        self.game.player.action_points += 2
                        self.game.player.add_health(5)
                        self.game.has_rested = True
                        self.game.message = "你选择了休息，行动点+2，健康值+5"
                        self.game.message_timer = 90
                    else:
                        self.game.message = "你已经休息过了，每回合只能休息一次"
                        self.game.message_timer = 60
