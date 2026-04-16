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
        self._load_images()
    
    def _load_images(self):
        """加载操场背景图片"""
        gym_path = os.path.join(os.path.dirname(__file__), '..', '..', 'image', 'gym.png')
        try:
            if os.path.exists(gym_path):
                self.gym_background = pygame.image.load(gym_path)
        except:
            pass
    
    def draw(self):
        """绘制操场场景"""
        # 绘制背景图片（缩放以覆盖整个窗口）
        if self.gym_background:
            scaled_bg = pygame.transform.scale(self.gym_background, (SCREEN_WIDTH, SCREEN_HEIGHT))
            self.screen.blit(scaled_bg, (0, 0))
        else:
            # 如果没有背景图片，使用默认背景色
            self.screen.fill((50, 50, 50))
        
        # 绘制标题
        self.game.draw_text("操场", SCREEN_WIDTH // 2 - 50, 50, (0, 0, 0), self.large_font)
        
        # 定义选项区域
        option1_rect = pygame.Rect(400, 200, 500, 50)
        option2_rect = pygame.Rect(400, 280, 500, 50)
        option3_rect = pygame.Rect(400, 360, 500, 50)
        back_rect = pygame.Rect(SCREEN_WIDTH // 2 - 50, 440, 100, 50)
        
        # 绘制选项框
        if not self.game.has_exercised:
            # 散步
            pygame.draw.rect(self.screen, (220, 180, 140), option1_rect)
            pygame.draw.rect(self.screen, (150, 100, 50), option1_rect, 2)
            self.game.draw_text("散步：行动点-1 体能+5", option1_rect.x + 10, option1_rect.y + 10, (254, 247, 201))
            
            # 跑步
            pygame.draw.rect(self.screen, (220, 180, 140), option2_rect)
            pygame.draw.rect(self.screen, (150, 100, 50), option2_rect, 2)
            self.game.draw_text("跑步：行动点-2 体能+10", option2_rect.x + 10, option2_rect.y + 10, (254, 247, 201))
            
            # 游泳
            pygame.draw.rect(self.screen, (220, 180, 140), option3_rect)
            pygame.draw.rect(self.screen, (150, 100, 50), option3_rect, 2)
            self.game.draw_text("游泳：行动点-2 金钱-20 体能+15", option3_rect.x + 10, option3_rect.y + 10, (254, 247, 201))
        else:
            # 已运动提示
            self.game.draw_text("已运动", SCREEN_WIDTH // 2 - 50, 200, (254, 247, 201), self.large_font)
        
        # 绘制返回按钮
        pygame.draw.rect(self.screen, (220, 180, 140), back_rect)
        pygame.draw.rect(self.screen, (150, 100, 50), back_rect, 2)
        self.game.draw_text("返回地图", back_rect.x + 10, back_rect.y + 10, (254, 247, 201))
        
        # 绘制消息
        if self.game.message_timer > 0:
            self.game.draw_text(self.game.message, SCREEN_WIDTH // 2 - 300, SCREEN_HEIGHT - 60, (254, 247, 201), self.large_font)
            self.game.message_timer -= 1
    
    def handle_events(self, events):
        """处理操场场景事件"""
        # 定义选项区域
        option1_rect = pygame.Rect(400, 200, 500, 50)
        option2_rect = pygame.Rect(400, 280, 500, 50)
        option3_rect = pygame.Rect(400, 360, 500, 50)
        back_rect = pygame.Rect(SCREEN_WIDTH // 2 - 50, 440, 100, 50)
        
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    # 按ESC返回地图
                    self.game.current_state = "MAIN_GAME"
                    self.game.map_system.toggle_map()  # 确保地图显示
            elif event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                if option1_rect.collidepoint(pos):
                    # 选择散步
                    if self.game.player.action_points >= 1:
                        self.game.player.action_points -= 1
                        self.game.player.add_physical(5)
                        self.game.message = "你选择了散步，行动点-1，体能+5"
                        self.game.message_timer = 90
                    else:
                        self.game.message = "行动点不足！"
                        self.game.message_timer = 60
                elif option2_rect.collidepoint(pos):
                    # 选择跑步
                    if self.game.player.action_points >= 2:
                        self.game.player.action_points -= 2
                        self.game.player.add_physical(10)
                        self.game.message = "你选择了跑步，行动点-2，体能+10"
                        self.game.message_timer = 90
                    else:
                        self.game.message = "行动点不足！"
                        self.game.message_timer = 60
                elif option3_rect.collidepoint(pos):
                    # 选择游泳
                    if self.game.player.action_points >= 2 and self.game.player.living_expenses >= 20:
                        self.game.player.action_points -= 2
                        self.game.player.living_expenses -= 20
                        self.game.player.add_physical(15)
                        self.game.message = "你选择了游泳，行动点-2，金钱-20，体能+15"
                        self.game.message_timer = 90
                    elif self.game.player.action_points < 2:
                        self.game.message = "行动点不足！"
                        self.game.message_timer = 60
                    else:
                        self.game.message = "金钱不足！"
                        self.game.message_timer = 60
                # 返回地图
                if back_rect.collidepoint(pos):
                    self.game.current_state = "MAIN_GAME"
                    self.game.map_system.toggle_map()  # 确保地图显示
