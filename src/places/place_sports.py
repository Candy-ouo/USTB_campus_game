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
                button_width = 500
                button_height = int(button_width * (self.walking_button.get_height() / self.walking_button.get_width()))
                # 确保按钮高度不超过50
                button_height = min(button_height, 50)
                # 计算按钮位置
                self.walking_button_rect = pygame.Rect(400, 200, button_width, button_height)
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
                button_width = 500
                button_height = int(button_width * (self.running_button.get_height() / self.running_button.get_width()))
                # 确保按钮高度不超过50
                button_height = min(button_height, 50)
                # 计算按钮位置
                self.running_button_rect = pygame.Rect(400, 280, button_width, button_height)
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
                button_width = 500
                button_height = int(button_width * (self.swimming_button.get_height() / self.swimming_button.get_width()))
                # 确保按钮高度不超过50
                button_height = min(button_height, 50)
                # 计算按钮位置
                self.swimming_button_rect = pygame.Rect(400, 360, button_width, button_height)
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
            button_width = 500
            button_height = int(button_width * (self.walking_button.get_height() / self.walking_button.get_width()))
            button_height = min(button_height, 50)
            walking_button_rect = pygame.Rect(400, 200, button_width, button_height)
        else:
            walking_button_rect = pygame.Rect(400, 200, 500, 50)
        
        # 计算跑步按钮矩形
        if self.running_button:
            button_width = 500
            button_height = int(button_width * (self.running_button.get_height() / self.running_button.get_width()))
            button_height = min(button_height, 50)
            running_button_rect = pygame.Rect(400, 280, button_width, button_height)
        else:
            running_button_rect = pygame.Rect(400, 280, 500, 50)
        
        # 计算游泳按钮矩形
        if self.swimming_button:
            button_width = 500
            button_height = int(button_width * (self.swimming_button.get_height() / self.swimming_button.get_width()))
            button_height = min(button_height, 50)
            swimming_button_rect = pygame.Rect(400, 360, button_width, button_height)
        else:
            swimming_button_rect = pygame.Rect(400, 360, 500, 50)

        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.game.current_state = "MAIN_GAME"
                    self.game.map_system.toggle_map()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                if walking_button_rect.collidepoint(pos):
                    # 使用add_action_points方法，确保健康状态检查
                    old_action_points = self.game.player.action_points
                    self.game.player.add_action_points(-1)
                    # 检查行动点是否真的减少了（生病时不会减少）
                    if self.game.player.action_points < old_action_points:
                        current_year = self.game.time_system.get_year()
                        self.game.player.add_physical(5, current_year)
                        self.game.player.add_reputation(1)  # 增加声望
                        self.game.message = "你选择了散步，体能+5，声望+1"
                        self.game.message_timer = 90
                    else:
                        self.game.message = "行动点不足或生病了！"
                        self.game.message_timer = 60
                elif running_button_rect.collidepoint(pos):
                    # 使用add_action_points方法，确保健康状态检查
                    old_action_points = self.game.player.action_points
                    self.game.player.add_action_points(-2)
                    # 检查行动点是否真的减少了（生病时不会减少）
                    if self.game.player.action_points < old_action_points:
                        current_year = self.game.time_system.get_year()
                        self.game.player.add_physical(10, current_year)
                        self.game.player.add_reputation(2)  # 增加声望
                        self.game.message = "你选择了跑步，体能+10，声望+2"
                        self.game.message_timer = 90
                    else:
                        self.game.message = "行动点不足或生病了！"
                        self.game.message_timer = 60
                elif swimming_button_rect.collidepoint(pos):
                    # 使用add_action_points方法，确保健康状态检查
                    old_action_points = self.game.player.action_points
                    self.game.player.add_action_points(-2)
                    # 检查行动点是否真的减少了（生病时不会减少）
                    if self.game.player.action_points < old_action_points and self.game.player.living_expenses >= 20:
                        self.game.player.living_expenses -= 20
                        current_year = self.game.time_system.get_year()
                        self.game.player.add_physical(15, current_year)
                        self.game.player.add_reputation(3)  # 增加声望
                        self.game.player.add_social(2)  # 增加人脉
                        self.game.message = "你选择了游泳，金钱-20，体能+15，声望+3，人脉+2"
                        self.game.message_timer = 90
                    elif old_action_points == self.game.player.action_points:
                        self.game.message = "行动点不足或生病了！"
                        self.game.message_timer = 60
                    else:
                        self.game.message = "金钱不足！"
                        self.game.message_timer = 60
