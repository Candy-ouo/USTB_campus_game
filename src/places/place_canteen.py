import pygame
import os
import sys
from data.config import SCREEN_WIDTH, SCREEN_HEIGHT

class Canteen:
    def __init__(self, game):
        self.game = game
        self.screen = game.screen
        self.font = game.font
        self.large_font = game.large_font
        self.start_font = game.start_font
        self.canteen_background = None
        self.food_1_button = None
        self.food_2_button = None
        self.food_3_button = None
        self._load_images()

    def _load_images(self):
        """加载食堂背景图片"""
        canteen_path = os.path.join(os.path.dirname(__file__), '..', '..', 'image', 'canteen_background.png')
        try:
            if os.path.exists(canteen_path):
                self.canteen_background = pygame.image.load(canteen_path)
        except:
            pass
        
        # 加载鸡腿套餐按钮图片
        food_1_button_path = os.path.join(os.path.dirname(__file__), '..', '..', 'image', 'food_1.png')
        try:
            if os.path.exists(food_1_button_path):
                self.food_1_button = pygame.image.load(food_1_button_path)
        except:
            pass
        
        # 加载营养套餐按钮图片
        food_2_button_path = os.path.join(os.path.dirname(__file__), '..', '..', 'image', 'food_2.png')
        try:
            if os.path.exists(food_2_button_path):
                self.food_2_button = pygame.image.load(food_2_button_path)
        except:
            pass
        
        # 加载特色美食按钮图片
        food_3_button_path = os.path.join(os.path.dirname(__file__), '..', '..', 'image', 'food_3.png')
        try:
            if os.path.exists(food_3_button_path):
                self.food_3_button = pygame.image.load(food_3_button_path)
        except:
            pass

    def draw(self):
        """绘制食堂场景"""
        if self.canteen_background:
            scaled_bg = pygame.transform.scale(self.canteen_background, (SCREEN_WIDTH, SCREEN_HEIGHT))
            self.screen.blit(scaled_bg, (0, 0))
        else:
            self.screen.fill((50, 50, 50))

        if not self.game.has_eaten:
            # 绘制鸡腿套餐按钮
            if self.food_1_button:
                # 保持图片原始比例，计算显示大小
                button_width = 150
                button_height = 78
                # 计算按钮位置
                self.food_1_button_rect = pygame.Rect(400, 200, button_width, button_height)
                # 缩放按钮图片
                scaled_button = pygame.transform.scale(self.food_1_button, (button_width, button_height))
                self.screen.blit(scaled_button, self.food_1_button_rect)
            else:
                # 如果图片加载失败，绘制默认矩形
                self.food_1_button_rect = pygame.Rect(400, 200, 500, 50)
                pygame.draw.rect(self.screen, (220, 180, 140), self.food_1_button_rect)
                pygame.draw.rect(self.screen, (150, 100, 50), self.food_1_button_rect, 2)
                self.game.draw_text("鸡腿套餐：金钱-10 心情+10 健康值+10 行动点+1", self.food_1_button_rect.x + 10, self.food_1_button_rect.y + 10, (254, 247, 201))

            # 绘制营养套餐按钮
            if self.food_2_button:
                # 保持图片原始比例，计算显示大小
                button_width = 150
                button_height = 78
                # 计算按钮位置
                self.food_2_button_rect = pygame.Rect(400, 280, button_width, button_height)
                # 缩放按钮图片
                scaled_button = pygame.transform.scale(self.food_2_button, (button_width, button_height))
                self.screen.blit(scaled_button, self.food_2_button_rect)
            else:
                # 如果图片加载失败，绘制默认矩形
                self.food_2_button_rect = pygame.Rect(400, 280, 500, 50)
                pygame.draw.rect(self.screen, (220, 180, 140), self.food_2_button_rect)
                pygame.draw.rect(self.screen, (150, 100, 50), self.food_2_button_rect, 2)
                self.game.draw_text("营养套餐：金钱-15 心情+20 健康值+10 行动点+2", self.food_2_button_rect.x + 10, self.food_2_button_rect.y + 10, (254, 247, 201))

            # 绘制特色美食按钮
            if self.food_3_button:
                # 保持图片原始比例，计算显示大小
                button_width = 150
                button_height = 78
                # 计算按钮位置
                self.food_3_button_rect = pygame.Rect(400, 360, button_width, button_height)
                # 缩放按钮图片
                scaled_button = pygame.transform.scale(self.food_3_button, (button_width, button_height))
                self.screen.blit(scaled_button, self.food_3_button_rect)
            else:
                # 如果图片加载失败，绘制默认矩形
                self.food_3_button_rect = pygame.Rect(400, 360, 500, 50)
                pygame.draw.rect(self.screen, (220, 180, 140), self.food_3_button_rect)
                pygame.draw.rect(self.screen, (150, 100, 50), self.food_3_button_rect, 2)
                self.game.draw_text("特色美食：金钱-20 心情+30 健康值+10 行动点+3", self.food_3_button_rect.x + 10, self.food_3_button_rect.y + 10, (254, 247, 201))
        else:
            self.game.draw_text("已用餐", SCREEN_WIDTH // 2 - 50, 200, (254, 247, 201), self.large_font)

        time_display = self.game.time_system.get_time_display()
        self.game.ui_hud.draw_all(time_display, self.game.player)

    def handle_events(self, events):
        """处理食堂场景事件"""
        # 计算鸡腿套餐按钮矩形
        if self.food_1_button:
            button_width = 150
            button_height = 78
            food_1_button_rect = pygame.Rect(400, 200, button_width, button_height)
        else:
            food_1_button_rect = pygame.Rect(400, 200, 500, 50)
        
        # 计算营养套餐按钮矩形
        if self.food_2_button:
            button_width = 150
            button_height = 78
            food_2_button_rect = pygame.Rect(400, 280, button_width, button_height)
        else:
            food_2_button_rect = pygame.Rect(400, 280, 500, 50)
        
        # 计算特色美食按钮矩形
        if self.food_3_button:
            button_width = 150
            button_height = 78
            food_3_button_rect = pygame.Rect(400, 360, button_width, button_height)
        else:
            food_3_button_rect = pygame.Rect(400, 360, 500, 50)

        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.game.current_state = "MAIN_GAME"
                    self.game.map_system.toggle_map()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                if not self.game.has_eaten:
                    if food_1_button_rect.collidepoint(pos):
                        if self.game.player.living_expenses >= 10:
                            self.game.player.living_expenses -= 10
                            self.game.player.add_mood(10)
                            self.game.player.add_health(10)
                            self.game.player.action_points += 1
                            self.game.has_eaten = True
                            self.game.message = "你选择了鸡腿套餐，金钱-10，心情+10，健康值+10，行动点+1"
                            self.game.message_timer = 90
                        else:
                            self.game.message = "金钱不足！"
                            self.game.message_timer = 60
                    elif food_2_button_rect.collidepoint(pos):
                        if self.game.player.living_expenses >= 15:
                            self.game.player.living_expenses -= 15
                            self.game.player.add_mood(20)
                            self.game.player.add_health(10)
                            self.game.player.action_points += 2
                            self.game.has_eaten = True
                            self.game.message = "你选择了营养套餐，金钱-15，心情+20，健康值+10，行动点+2"
                            self.game.message_timer = 90
                        else:
                            self.game.message = "金钱不足！"
                            self.game.message_timer = 60
                    elif food_3_button_rect.collidepoint(pos):
                        if self.game.player.living_expenses >= 20:
                            self.game.player.living_expenses -= 20
                            self.game.player.add_mood(30)
                            self.game.player.add_health(10)
                            self.game.player.action_points += 3
                            self.game.has_eaten = True
                            self.game.message = "你选择了特色美食，金钱-20，心情+30，健康值+10，行动点+3"
                            self.game.message_timer = 90
                        else:
                            self.game.message = "金钱不足！"
                            self.game.message_timer = 60
