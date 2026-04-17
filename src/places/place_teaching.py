import pygame
import os
import sys
from data.config import SCREEN_WIDTH, SCREEN_HEIGHT

class Teaching:
    def __init__(self, game):
        self.game = game
        self.screen = game.screen
        self.font = game.font
        self.large_font = game.large_font
        self.classroom_background = None
        self._load_images()

    def _load_images(self):
        """加载教学区背景图片"""
        classroom_path = os.path.join(os.path.dirname(__file__), '..', '..', 'image', 'classroom_background.png')
        try:
            if os.path.exists(classroom_path):
                self.classroom_background = pygame.image.load(classroom_path)
        except:
            pass

    def draw(self):
        """绘制教学区场景"""
        if self.classroom_background:
            scaled_bg = pygame.transform.scale(self.classroom_background, (SCREEN_WIDTH, SCREEN_HEIGHT))
            self.screen.blit(scaled_bg, (0, 0))
        else:
            self.screen.fill((50, 50, 50))

        option1_rect = pygame.Rect(400, 200, 500, 50)
        option2_rect = pygame.Rect(400, 280, 500, 50)

        if not self.game.has_studied:
            pygame.draw.rect(self.screen, (220, 180, 140), option1_rect)
            pygame.draw.rect(self.screen, (150, 100, 50), option1_rect, 2)
            self.game.draw_text("上课：行动点-2 学识+30 心情-30 健康值-5", option1_rect.x + 10, option1_rect.y + 10, (254, 247, 201))

            pygame.draw.rect(self.screen, (220, 180, 140), option2_rect)
            pygame.draw.rect(self.screen, (150, 100, 50), option2_rect, 2)
            self.game.draw_text("自习：行动点-1 学识+15 心情-20 健康值-5", option2_rect.x + 10, option2_rect.y + 10, (254, 247, 201))
        else:
            self.game.draw_text("已学习", SCREEN_WIDTH // 2 - 50, 200, (254, 247, 201), self.large_font)

        if self.game.message_timer > 0:
            self.game.draw_text(self.game.message, SCREEN_WIDTH // 2 - 300, SCREEN_HEIGHT - 60, (254, 247, 201), self.large_font)
            self.game.message_timer -= 1

        time_display = self.game.time_system.get_time_display()
        self.game.ui_hud.draw_all(time_display, self.game.player)

    def handle_events(self, events):
        """处理教学区场景事件"""
        option1_rect = pygame.Rect(400, 200, 500, 50)
        option2_rect = pygame.Rect(400, 280, 500, 50)

        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.game.current_state = "MAIN_GAME"
                    self.game.map_system.toggle_map()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                if option1_rect.collidepoint(pos):
                    if self.game.player.action_points >= 2:
                        self.game.player.action_points -= 2
                        current_year = self.game.time_system.get_year()
                        self.game.player.add_knowledge(30, current_year)
                        self.game.player.add_mood(-30)
                        self.game.player.add_health(-5)
                        self.game.message = "你选择了上课，行动点-2，学识+30，心情-30，健康值-5"
                        self.game.message_timer = 90
                    else:
                        self.game.message = "行动点不足！"
                        self.game.message_timer = 60
                elif option2_rect.collidepoint(pos):
                    if self.game.player.action_points >= 1:
                        self.game.player.action_points -= 1
                        current_year = self.game.time_system.get_year()
                        self.game.player.add_knowledge(15, current_year)
                        self.game.player.add_mood(-20)
                        self.game.player.add_health(-5)
                        self.game.message = "你选择了自习，行动点-1，学识+15，心情-20，健康值-5"
                        self.game.message_timer = 90
                    else:
                        self.game.message = "行动点不足！"
                        self.game.message_timer = 60
