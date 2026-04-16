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
        self._load_images()
    
    def _load_images(self):
        """加载校医院背景图片"""
        hospital_path = os.path.join(os.path.dirname(__file__), '..', '..', 'image', 'hospital.png')
        try:
            if os.path.exists(hospital_path):
                self.hospital_background = pygame.image.load(hospital_path)
        except:
            pass
    
    def draw(self):
        """绘制校医院场景"""
        # 绘制背景图片（缩放以覆盖整个窗口）
        if self.hospital_background:
            scaled_bg = pygame.transform.scale(self.hospital_background, (SCREEN_WIDTH, SCREEN_HEIGHT))
            self.screen.blit(scaled_bg, (0, 0))
        else:
            # 如果没有背景图片，使用默认背景色
            self.screen.fill((50, 50, 50))
        
        # 绘制标题
        self.game.draw_text("校医院", SCREEN_WIDTH // 2 - 50, 50, (0, 0, 0), self.large_font)
        
        # 定义选项区域
        option1_rect = pygame.Rect(400, 200, 500, 50)
        back_rect = pygame.Rect(SCREEN_WIDTH // 2 - 50, 300, 100, 50)
        
        # 绘制选项框
        # 治病选项
        pygame.draw.rect(self.screen, (220, 180, 140), option1_rect)
        pygame.draw.rect(self.screen, (150, 100, 50), option1_rect, 2)
        self.game.draw_text("治病：金钱-50 恢复健康状态", option1_rect.x + 10, option1_rect.y + 10, (254, 247, 201))
        
        # 绘制返回按钮
        pygame.draw.rect(self.screen, (220, 180, 140), back_rect)
        pygame.draw.rect(self.screen, (150, 100, 50), back_rect, 2)
        self.game.draw_text("返回地图", back_rect.x + 10, back_rect.y + 10, (254, 247, 201))
        
        # 绘制消息
        if self.game.message_timer > 0:
            self.game.draw_text(self.game.message, SCREEN_WIDTH // 2 - 300, SCREEN_HEIGHT - 60, (254, 247, 201), self.large_font)
            self.game.message_timer -= 1
    
    def handle_events(self, events):
        """处理校医院场景事件"""
        # 定义选项区域
        option1_rect = pygame.Rect(400, 200, 500, 50)
        back_rect = pygame.Rect(SCREEN_WIDTH // 2 - 50, 300, 100, 50)
        
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    # 按ESC返回地图
                    self.game.current_state = "MAIN_GAME"
                    self.game.map_system.toggle_map()  # 确保地图显示
            elif event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                if option1_rect.collidepoint(pos):
                    # 选择治病
                    if self.game.player.get_health() < 60:
                        if self.game.player.living_expenses >= 50:
                            self.game.player.living_expenses -= 50
                            self.game.player.add_health(100)  # 恢复健康状态
                            self.game.message = "你在医院治疗，金钱-50，健康状态已恢复"
                            self.game.message_timer = 90
                        else:
                            self.game.message = "金钱不足，无法治疗！"
                            self.game.message_timer = 60
                    else:
                        self.game.message = "你的健康状态良好，不需要治疗"
                        self.game.message_timer = 60
                # 返回地图
                if back_rect.collidepoint(pos):
                    self.game.current_state = "MAIN_GAME"
                    self.game.map_system.toggle_map()  # 确保地图显示
