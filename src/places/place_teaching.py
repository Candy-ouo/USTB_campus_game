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
        self.start_font = game.start_font
        self.classroom_background = None
        self.shangke_button = None
        self.zixi_button = None
        self._load_images()

    def _load_images(self):
        """加载教学区背景图片"""
        classroom_path = os.path.join(os.path.dirname(__file__), '..', '..', 'image', 'classroom_background.png')
        try:
            if os.path.exists(classroom_path):
                self.classroom_background = pygame.image.load(classroom_path)
        except:
            pass
        
        # 加载上课按钮图片
        shangke_button_path = os.path.join(os.path.dirname(__file__), '..', '..', 'image', 'shangke_button.png')
        try:
            if os.path.exists(shangke_button_path):
                self.shangke_button = pygame.image.load(shangke_button_path)
        except:
            pass
        
        # 加载自习按钮图片
        zixi_button_path = os.path.join(os.path.dirname(__file__), '..', '..', 'image', 'zixi_button.png')
        try:
            if os.path.exists(zixi_button_path):
                self.zixi_button = pygame.image.load(zixi_button_path)
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
            # 绘制上课按钮
            if self.shangke_button:
                # 保持图片原始比例，计算显示大小
                button_width = 150
                button_height = 78
                # 计算按钮位置
                self.shangke_button_rect = pygame.Rect(400, 200, button_width, button_height)
                # 缩放按钮图片
                scaled_button = pygame.transform.scale(self.shangke_button, (button_width, button_height))
                self.screen.blit(scaled_button, self.shangke_button_rect)
            else:
                # 如果图片加载失败，绘制默认矩形
                self.shangke_button_rect = pygame.Rect(400, 200, 500, 50)
                pygame.draw.rect(self.screen, (220, 180, 140), self.shangke_button_rect)
                pygame.draw.rect(self.screen, (150, 100, 50), self.shangke_button_rect, 2)
                self.game.draw_text("上课：行动点-2 学识+30 心情-30 健康值-5", self.shangke_button_rect.x + 10, self.shangke_button_rect.y + 10, (254, 247, 201))

            # 绘制自习按钮
            if self.zixi_button:
                # 保持图片原始比例，计算显示大小
                button_width = 150
                button_height = 78
                # 计算按钮位置
                self.zixi_button_rect = pygame.Rect(400, 280, button_width, button_height)
                # 缩放按钮图片
                scaled_button = pygame.transform.scale(self.zixi_button, (button_width, button_height))
                self.screen.blit(scaled_button, self.zixi_button_rect)
            else:
                # 如果图片加载失败，绘制默认矩形
                self.zixi_button_rect = pygame.Rect(400, 280, 500, 50)
                pygame.draw.rect(self.screen, (220, 180, 140), self.zixi_button_rect)
                pygame.draw.rect(self.screen, (150, 100, 50), self.zixi_button_rect, 2)
                self.game.draw_text("自习：行动点-1 学识+15 心情-20 健康值-5", self.zixi_button_rect.x + 10, self.zixi_button_rect.y + 10, (254, 247, 201))
        else:
            self.game.draw_text("已学习", SCREEN_WIDTH // 2 - 50, SCREEN_HEIGHT - 50, (141, 54, 25), self.start_font)

        time_display = self.game.time_system.get_time_display()
        self.game.ui_hud.draw_all(time_display, self.game.player)

    def handle_events(self, events):
        """处理教学区场景事件"""
        # 计算上课按钮矩形
        if self.shangke_button:
            button_width = 150
            button_height = 78
            button_height = min(button_height, 50)
            shangke_button_rect = pygame.Rect(400, 200, button_width, button_height)
        else:
            shangke_button_rect = pygame.Rect(400, 200, 500, 50)
        
        # 计算自习按钮矩形
        if self.zixi_button:
            button_width = 150
            button_height = 78
            button_height = min(button_height, 50)
            zixi_button_rect = pygame.Rect(400, 280, button_width, button_height)
        else:
            zixi_button_rect = pygame.Rect(400, 280, 500, 50)

        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.game.current_state = "MAIN_GAME"
                    self.game.map_system.toggle_map()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                if shangke_button_rect.collidepoint(pos):
                    # 使用add_action_points方法，确保健康状态检查
                    old_action_points = self.game.player.action_points
                    self.game.player.add_action_points(-2)
                    # 检查行动点是否真的减少了（生病时不会减少）
                    if self.game.player.action_points < old_action_points:
                        current_year = self.game.time_system.get_year()
                        self.game.player.add_knowledge(30, current_year)
                        self.game.player.add_skill(5)  # 增加技能
                        self.game.player.add_mood(-30)
                        self.game.player.add_health(-5)
                        self.game.message = "你选择了上课，学识+30，技能+5，心情-30，健康值-5"
                        self.game.message_timer = 90
                    else:
                        self.game.message = "行动点不足或生病了！"
                        self.game.message_timer = 60
                elif zixi_button_rect.collidepoint(pos):
                    # 使用add_action_points方法，确保健康状态检查
                    old_action_points = self.game.player.action_points
                    self.game.player.add_action_points(-1)
                    # 检查行动点是否真的减少了（生病时不会减少）
                    if self.game.player.action_points < old_action_points:
                        current_year = self.game.time_system.get_year()
                        self.game.player.add_knowledge(15, current_year)
                        self.game.player.add_skill(2)  # 增加技能
                        self.game.player.add_mood(-20)
                        self.game.player.add_health(-5)
                        self.game.message = "你选择了自习，学识+15，技能+2，心情-20，健康值-5"
                        self.game.message_timer = 90
                    else:
                        self.game.message = "行动点不足或生病了！"
                        self.game.message_timer = 60
