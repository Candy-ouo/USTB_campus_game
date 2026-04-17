import pygame
import os
import sys
from data.config import SCREEN_WIDTH, SCREEN_HEIGHT

class Sports:
    def __init__(self, game):
        self.game = game
        self.screen = game.screen
        self.font = game.font
        self.large_font = game.large_font
        self.gym_background = None
        self.walking_button = None
        self.running_button = None
        self.swimming_button = None
        self._load_images()

    def _load_images(self):
        """加载操场背景图片"""
        gym_path = os.path.join(os.path.dirname(__file__), '..', '..', 'image', 'playground_background.png')
        try:
            if os.path.exists(gym_path):
                self.gym_background = pygame.image.load(gym_path)
        except:
            pass
        
        # 加载散步按钮图片
        walking_button_path = os.path.join(os.path.dirname(__file__), '..', '..', 'image', 'walking_button.png')
        try:
            if os.path.exists(walking_button_path):
                self.walking_button = pygame.image.load(walking_button_path)
        except:
            pass
        
        # 加载跑步按钮图片
        running_button_path = os.path.join(os.path.dirname(__file__), '..', '..', 'image', 'running_button.png')
        try:
            if os.path.exists(running_button_path):
                self.running_button = pygame.image.load(running_button_path)
        except:
            pass
        
        # 加载游泳按钮图片
        swimming_button_path = os.path.join(os.path.dirname(__file__), '..', '..', 'image', 'swimming_button.png')
        try:
            if os.path.exists(swimming_button_path):
                self.swimming_button = pygame.image.load(swimming_button_path)
        except:
            pass

    def draw(self):
        """绘制操场场景"""
        if self.gym_background:
            scaled_bg = pygame.transform.scale(self.gym_background, (SCREEN_WIDTH, SCREEN_HEIGHT))
            self.screen.blit(scaled_bg, (0, 0))
        else:
            self.screen.fill((50, 50, 50))

        option1_rect = pygame.Rect(400, 200, 500, 50)
        option2_rect = pygame.Rect(400, 280, 500, 50)
        option3_rect = pygame.Rect(400, 360, 500, 50)

        if not self.game.has_exercised:
            # 绘制散步按钮
            if self.walking_button:
                # 保持图片原始比例，计算显示大小
                button_width = 150
                button_height = 78
                # 计算按钮位置
                self.walking_button_rect = pygame.Rect(450, 550, button_width, button_height)
                # 缩放按钮图片
                scaled_button = pygame.transform.scale(self.walking_button, (button_width, button_height))
                self.screen.blit(scaled_button, self.walking_button_rect)
            else:
                # 如果图片加载失败，绘制默认矩形
                self.walking_button_rect = pygame.Rect(400, 200, 500, 50)
                pygame.draw.rect(self.screen, (220, 180, 140), self.walking_button_rect)
                pygame.draw.rect(self.screen, (150, 100, 50), self.walking_button_rect, 2)
                self.game.draw_text("散步：行动点-1 体能+5", self.walking_button_rect.x + 10, self.walking_button_rect.y + 10, (254, 247, 201))

            # 绘制跑步按钮
            if self.running_button:
                # 保持图片原始比例，计算显示大小
                button_width = 150
                button_height = 78
                # 计算按钮位置
                self.running_button_rect = pygame.Rect(800, 500, button_width, button_height)
                # 缩放按钮图片
                scaled_button = pygame.transform.scale(self.running_button, (button_width, button_height))
                self.screen.blit(scaled_button, self.running_button_rect)
            else:
                # 如果图片加载失败，绘制默认矩形
                self.running_button_rect = pygame.Rect(400, 280, 500, 50)
                pygame.draw.rect(self.screen, (220, 180, 140), self.running_button_rect)
                pygame.draw.rect(self.screen, (150, 100, 50), self.running_button_rect, 2)
                self.game.draw_text("跑步：行动点-2 体能+10", self.running_button_rect.x + 10, self.running_button_rect.y + 10, (254, 247, 201))

            # 绘制游泳按钮
            if self.swimming_button:
                # 保持图片原始比例，计算显示大小
                button_width = 150
                button_height = 78
                # 计算按钮位置
                self.swimming_button_rect = pygame.Rect(300, 300, button_width, button_height)
                # 缩放按钮图片
                scaled_button = pygame.transform.scale(self.swimming_button, (button_width, button_height))
                self.screen.blit(scaled_button, self.swimming_button_rect)
            else:
                # 如果图片加载失败，绘制默认矩形
                self.swimming_button_rect = pygame.Rect(400, 360, 500, 50)
                pygame.draw.rect(self.screen, (220, 180, 140), self.swimming_button_rect)
                pygame.draw.rect(self.screen, (150, 100, 50), self.swimming_button_rect, 2)
                self.game.draw_text("游泳：行动点-2 金钱-20 体能+15", self.swimming_button_rect.x + 10, self.swimming_button_rect.y + 10, (254, 247, 201))
        else:
            self.game.draw_text("已运动", SCREEN_WIDTH // 2 - 50, SCREEN_HEIGHT - 50, (141, 54, 25), self.start_font)

        time_display = self.game.time_system.get_time_display()
        self.game.ui_hud.draw_all(time_display, self.game.player)

    def handle_events(self, events):
        """处理操场场景事件"""
        # 计算散步按钮矩形
        if self.walking_button:
            button_width = 150
            button_height = 78
            walking_button_rect = pygame.Rect(450, 550, button_width, button_height)
        else:
            walking_button_rect = pygame.Rect(400, 550, 500, 50)
        
        # 计算跑步按钮矩形
        if self.running_button:
            button_width = 150
            button_height = 78
            running_button_rect = pygame.Rect(800, 500, button_width, button_height)
        else:
            running_button_rect = pygame.Rect(800, 500, 500, 50)
        
        # 计算游泳按钮矩形
        if self.swimming_button:
            button_width = 150
            button_height = 78
            swimming_button_rect = pygame.Rect(300, 300, button_width, button_height)
        else:
            swimming_button_rect = pygame.Rect(300, 300, 500, 50)

        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.game.current_state = "MAIN_GAME"
                    self.game.map_system.toggle_map()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                if walking_button_rect.collidepoint(pos):
                    if self.game.player.action_points >= 1:
                        self.game.player.action_points -= 1
                        current_year = self.game.time_system.get_year()
                        self.game.player.add_physical(5, current_year)
                        self.game.message = "你选择了散步，行动点-1，体能+5"
                        self.game.message_timer = 90
                    else:
                        self.game.message = "行动点不足！"
                        self.game.message_timer = 60
                elif running_button_rect.collidepoint(pos):
                    if self.game.player.action_points >= 2:
                        self.game.player.action_points -= 2
                        current_year = self.game.time_system.get_year()
                        self.game.player.add_physical(10, current_year)
                        self.game.message = "你选择了跑步，行动点-2，体能+10"
                        self.game.message_timer = 90
                    else:
                        self.game.message = "行动点不足！"
                        self.game.message_timer = 60
                elif swimming_button_rect.collidepoint(pos):
                    if self.game.player.action_points >= 2 and self.game.player.living_expenses >= 20:
                        self.game.player.action_points -= 2
                        self.game.player.living_expenses -= 20
                        current_year = self.game.time_system.get_year()
                        self.game.player.add_physical(15, current_year)
                        self.game.message = "你选择了游泳，行动点-2，金钱-20，体能+15"
                        self.game.message_timer = 90
                    elif self.game.player.action_points < 2:
                        self.game.message = "行动点不足！"
                        self.game.message_timer = 60
                    else:
                        self.game.message = "金钱不足！"
                        self.game.message_timer = 60
