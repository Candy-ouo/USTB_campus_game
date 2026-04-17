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

        # 只有未玩游戏时显示玩游戏选项
        if not self.game.has_played_games:
            pygame.draw.rect(self.screen, (220, 180, 140), option1_rect)
            pygame.draw.rect(self.screen, (150, 100, 50), option1_rect, 2)
            self.game.draw_text("玩游戏：心情+40 行动点-1", option1_rect.x + 10, option1_rect.y + 10, (254, 247, 201))

        # 只有未看书时显示看书选项
        if not self.game.has_read_book:
            pygame.draw.rect(self.screen, (220, 180, 140), option2_rect)
            pygame.draw.rect(self.screen, (150, 100, 50), option2_rect, 2)
            self.game.draw_text("看书：学识+10 心情-10 行动点-1", option2_rect.x + 10, option2_rect.y + 10, (254, 247, 201))

        # 只有未休息时显示休息选项
        if not self.game.has_rested:
            pygame.draw.rect(self.screen, (220, 180, 140), option3_rect)
            pygame.draw.rect(self.screen, (150, 100, 50), option3_rect, 2)
            self.game.draw_text("床：行动点+2 健康值+5", option3_rect.x + 10, option3_rect.y + 10, (254, 247, 201))

        if self.game.message_timer > 0:
            self.game.draw_text(self.game.message, SCREEN_WIDTH // 2 - 150, SCREEN_HEIGHT - 110, (254, 247, 201), self.large_font)
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
                # 只有未玩游戏时才能点击玩游戏选项
                if not self.game.has_played_games and option1_rect.collidepoint(pos):
                    if self.game.player.action_points >= 1:
                        self.game.player.add_action_points(-1)
                        self.game.player.add_mood(40)
                        self.game.has_played_games = True
                        self.game.message = "你选择了玩游戏，心情+40，行动点-1"
                        self.game.message_timer = 90
                    else:
                        self.game.message = "行动点不足！"
                        self.game.message_timer = 60
                # 只有未看书时才能点击看书选项
                elif not self.game.has_read_book and option2_rect.collidepoint(pos):
                    if self.game.player.action_points >= 1:
                        self.game.player.add_action_points(-1)
                        current_year = self.game.time_system.get_year()
                        self.game.player.add_knowledge(10, current_year)
                        self.game.player.add_mood(-10)
                        self.game.has_read_book = True
                        self.game.message = "你选择了看书，学识+10，心情-10，行动点-1"
                        self.game.message_timer = 90
                    else:
                        self.game.message = "行动点不足！"
                        self.game.message_timer = 60
                # 只有未休息时才能点击休息选项
                elif not self.game.has_rested and option3_rect.collidepoint(pos):
                    self.game.player.add_action_points(2)
                    self.game.player.add_health(5)
                    self.game.has_rested = True
                    self.game.message = "你选择了休息，行动点+2，健康值+5"
                    self.game.message_timer = 90
