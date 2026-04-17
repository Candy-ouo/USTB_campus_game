import pygame
import os
import sys
from data.config import SCREEN_WIDTH, SCREEN_HEIGHT

class Supermarket:
    def __init__(self, game):
        self.game = game
        self.screen = game.screen
        self.font = game.font
        self.large_font = game.large_font
        self.supermarket_background = None
        self._load_images()

    def _load_images(self):
        """加载超市背景图片"""
        supermarket_path = os.path.join(os.path.dirname(__file__), '..', '..', 'image', 'supermarket_background.png')
        try:
            if os.path.exists(supermarket_path):
                self.supermarket_background = pygame.image.load(supermarket_path)
        except:
            pass

    def draw(self):
        """绘制超市场景"""
        if self.supermarket_background:
            scaled_bg = pygame.transform.scale(self.supermarket_background, (SCREEN_WIDTH, SCREEN_HEIGHT))
            self.screen.blit(scaled_bg, (0, 0))
        else:
            self.screen.fill((50, 50, 50))

        self.game.draw_text(f"今日购买次数：{self.game.supermarket_purchases}/2", 20, 100, (254, 247, 201), self.large_font)

        option1_rect = pygame.Rect(400, 150, 500, 50)
        option2_rect = pygame.Rect(400, 200, 500, 50)
        option3_rect = pygame.Rect(400, 250, 500, 50)
        option4_rect = pygame.Rect(400, 300, 500, 50)
        option5_rect = pygame.Rect(400, 350, 500, 50)
        option6_rect = pygame.Rect(400, 400, 500, 50)

        if self.game.supermarket_purchases < 2:
            pygame.draw.rect(self.screen, (220, 180, 140), option1_rect)
            pygame.draw.rect(self.screen, (150, 100, 50), option1_rect, 2)
            self.game.draw_text("美味蛋糕：金钱-15 心情+30", option1_rect.x + 10, option1_rect.y + 10, (254, 247, 201))

            pygame.draw.rect(self.screen, (220, 180, 140), option2_rect)
            pygame.draw.rect(self.screen, (150, 100, 50), option2_rect, 2)
            self.game.draw_text("潮流衣服：金钱-30 魅力+10", option2_rect.x + 10, option2_rect.y + 10, (254, 247, 201))

            pygame.draw.rect(self.screen, (220, 180, 140), option3_rect)
            pygame.draw.rect(self.screen, (150, 100, 50), option3_rect, 2)
            self.game.draw_text("课外教材：金钱-20 学识+10", option3_rect.x + 10, option3_rect.y + 10, (254, 247, 201))

            pygame.draw.rect(self.screen, (220, 180, 140), option4_rect)
            pygame.draw.rect(self.screen, (150, 100, 50), option4_rect, 2)
            self.game.draw_text("健身器材：金钱-30 体能+10", option4_rect.x + 10, option4_rect.y + 10, (254, 247, 201))

            pygame.draw.rect(self.screen, (220, 180, 140), option5_rect)
            pygame.draw.rect(self.screen, (150, 100, 50), option5_rect, 2)
            self.game.draw_text("不健康的零食：金钱-15 心情+40 健康-5", option5_rect.x + 10, option5_rect.y + 10, (254, 247, 201))

            pygame.draw.rect(self.screen, (220, 180, 140), option6_rect)
            pygame.draw.rect(self.screen, (150, 100, 50), option6_rect, 2)
            self.game.draw_text("体力药水：金钱-30 行动点+1", option6_rect.x + 10, option6_rect.y + 10, (254, 247, 201))
        else:
            self.game.draw_text("今日购买次数已达上限", SCREEN_WIDTH // 2 - 150, 200, (254, 247, 201), self.large_font)

        if self.game.message_timer > 0:
            self.game.draw_text(self.game.message, SCREEN_WIDTH // 2 - 150, SCREEN_HEIGHT - 110, (254, 247, 201), self.large_font)
            self.game.message_timer -= 1

        time_display = self.game.time_system.get_time_display()
        self.game.ui_hud.draw_all(time_display, self.game.player)

    def handle_events(self, events):
        """处理超市场景事件"""
        option1_rect = pygame.Rect(400, 150, 500, 50)
        option2_rect = pygame.Rect(400, 200, 500, 50)
        option3_rect = pygame.Rect(400, 250, 500, 50)
        option4_rect = pygame.Rect(400, 300, 500, 50)
        option5_rect = pygame.Rect(400, 350, 500, 50)
        option6_rect = pygame.Rect(400, 400, 500, 50)

        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.game.current_state = "MAIN_GAME"
                    self.game.map_system.toggle_map()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                if self.game.supermarket_purchases < 2:
                    if option1_rect.collidepoint(pos):
                        if self.game.player.living_expenses >= 15:
                            self.game.player.living_expenses -= 15
                            self.game.player.add_mood(30)
                            self.game.supermarket_purchases += 1
                            self.game.message = "你购买了美味蛋糕，金钱-15，心情+30"
                            self.game.message_timer = 90
                        else:
                            self.game.message = "金钱不足！"
                            self.game.message_timer = 60
                    elif option2_rect.collidepoint(pos):
                        if self.game.player.living_expenses >= 30:
                            self.game.player.living_expenses -= 30
                            current_year = self.game.time_system.get_year()
                            self.game.player.add_charm(10, current_year)
                            self.game.supermarket_purchases += 1
                            self.game.message = "你购买了潮流衣服，金钱-30，魅力+10"
                            self.game.message_timer = 90
                        else:
                            self.game.message = "金钱不足！"
                            self.game.message_timer = 60
                    elif option3_rect.collidepoint(pos):
                        if self.game.player.living_expenses >= 20:
                            self.game.player.living_expenses -= 20
                            current_year = self.game.time_system.get_year()
                            self.game.player.add_knowledge(10, current_year)
                            self.game.supermarket_purchases += 1
                            self.game.message = "你购买了课外教材，金钱-20，学识+10"
                            self.game.message_timer = 90
                        else:
                            self.game.message = "金钱不足！"
                            self.game.message_timer = 60
                    elif option4_rect.collidepoint(pos):
                        if self.game.player.living_expenses >= 30:
                            self.game.player.living_expenses -= 30
                            current_year = self.game.time_system.get_year()
                            self.game.player.add_physical(10, current_year)
                            self.game.supermarket_purchases += 1
                            self.game.message = "你购买了健身器材，金钱-30，体能+10"
                            self.game.message_timer = 90
                        else:
                            self.game.message = "金钱不足！"
                            self.game.message_timer = 60
                    elif option5_rect.collidepoint(pos):
                        if self.game.player.living_expenses >= 15:
                            self.game.player.living_expenses -= 15
                            self.game.player.add_mood(40)
                            self.game.player.add_health(-5)
                            self.game.supermarket_purchases += 1
                            self.game.message = "你购买了不健康的零食，金钱-15，心情+40，健康-5"
                            self.game.message_timer = 90
                        else:
                            self.game.message = "金钱不足！"
                            self.game.message_timer = 60
                    elif option6_rect.collidepoint(pos):
                        if self.game.player.living_expenses >= 30:
                            self.game.player.living_expenses -= 30
                            self.game.player.add_action_points(1)
                            self.game.supermarket_purchases += 1
                            self.game.message = "你购买了体力药水，金钱-30，行动点+1"
                            self.game.message_timer = 90
                        else:
                            self.game.message = "金钱不足！"
                            self.game.message_timer = 60
