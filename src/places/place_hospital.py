import pygame
import os
import sys
from data.config import SCREEN_WIDTH, SCREEN_HEIGHT

class Hospital:
    def __init__(self, game):
        self.game = game
        self.screen = game.screen
        self.font = game.font
        self.large_font = game.large_font
        self.hospital_background = None
        self.zhibing_button = None
        self._load_images()

    def _load_images(self):
        """加载校医院背景图片"""
        hospital_path = os.path.join(os.path.dirname(__file__), '..', '..', 'image', 'hospital_background.png')
        try:
            if os.path.exists(hospital_path):
                self.hospital_background = pygame.image.load(hospital_path)
        except:
            pass
        
        # 加载治病按钮图片
        zhibing_button_path = os.path.join(os.path.dirname(__file__), '..', '..', 'image', 'zhibing_button.png')
        try:
            if os.path.exists(zhibing_button_path):
                self.zhibing_button = pygame.image.load(zhibing_button_path)
        except:
            pass

    def draw(self):
        """绘制校医院场景"""
        if self.hospital_background:
            scaled_bg = pygame.transform.scale(self.hospital_background, (SCREEN_WIDTH, SCREEN_HEIGHT))
            self.screen.blit(scaled_bg, (0, 0))
        else:
            self.screen.fill((50, 50, 50))

        option1_rect = pygame.Rect(400, 200, 500, 50)

        # 绘制治病按钮
        if self.zhibing_button:
            # 保持图片原始比例，计算显示大小
            button_width = 150
            button_height = 78
            # 计算按钮位置
            self.zhibing_button_rect = pygame.Rect(400, 200, button_width, button_height)
            # 缩放按钮图片
            scaled_button = pygame.transform.scale(self.zhibing_button, (button_width, button_height))
            self.screen.blit(scaled_button, self.zhibing_button_rect)
        else:
            # 如果图片加载失败，绘制默认矩形
            self.zhibing_button_rect = pygame.Rect(400, 200, 500, 50)
            pygame.draw.rect(self.screen, (220, 180, 140), self.zhibing_button_rect)
            pygame.draw.rect(self.screen, (150, 100, 50), self.zhibing_button_rect, 2)
            self.game.draw_text("治病：金钱-50 恢复健康状态", self.zhibing_button_rect.x + 10, self.zhibing_button_rect.y + 10, (254, 247, 201))

        time_display = self.game.time_system.get_time_display()
        self.game.ui_hud.draw_all(time_display, self.game.player)

    def handle_events(self, events):
        """处理校医院场景事件"""
        # 计算治病按钮矩形
        if self.zhibing_button:
            button_width = 150
            button_height = 78
            zhibing_button_rect = pygame.Rect(400, 200, button_width, button_height)
        else:
            zhibing_button_rect = pygame.Rect(400, 200, 500, 50)

        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.game.current_state = "MAIN_GAME"
                    self.game.map_system.toggle_map()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                if zhibing_button_rect.collidepoint(pos):
                    if self.game.player.get_health() < 60:
                        if self.game.player.living_expenses >= 50:
                            self.game.player.living_expenses -= 50
                            # 恢复健康状态到80
                            self.game.player.add_health(80 - self.game.player.get_health())
                            self.game.message = "你在医院治疗，金钱-50，健康状态已恢复到80"
                            self.game.message_timer = 90
                        else:
                            self.game.message = "金钱不足，无法治疗！"
                            self.game.message_timer = 60
                    else:
                        self.game.message = "你的健康状态良好，不需要治疗"
                        self.game.message_timer = 60
