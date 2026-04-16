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
        self.canteen_background = None
        self._load_images()
    
    def _load_images(self):
        """加载食堂背景图片"""
        canteen_path = os.path.join(os.path.dirname(__file__), '..', '..', 'image', 'canteen.png')
        try:
            if os.path.exists(canteen_path):
                self.canteen_background = pygame.image.load(canteen_path)
        except:
            pass
    
    def draw(self):
        """绘制食堂场景"""
        # 绘制背景图片（缩放以覆盖整个窗口）
        if self.canteen_background:
            scaled_bg = pygame.transform.scale(self.canteen_background, (SCREEN_WIDTH, SCREEN_HEIGHT))
            self.screen.blit(scaled_bg, (0, 0))
        else:
            # 如果没有背景图片，使用默认背景色
            self.screen.fill((50, 50, 50))
        
        # 绘制标题
        self.game.draw_text("食堂", SCREEN_WIDTH // 2 - 50, 50, (0, 0, 0), self.large_font)
        
        # 定义选项区域
        option1_rect = pygame.Rect(400, 200, 500, 50)
        option2_rect = pygame.Rect(400, 280, 500, 50)
        option3_rect = pygame.Rect(400, 360, 500, 50)
        back_rect = pygame.Rect(SCREEN_WIDTH // 2 - 50, 440, 100, 50)
        
        # 绘制选项框
        if not self.game.has_eaten:
            # 鸡腿套餐
            pygame.draw.rect(self.screen, (220, 180, 140), option1_rect)
            pygame.draw.rect(self.screen, (150, 100, 50), option1_rect, 2)
            self.game.draw_text("鸡腿套餐：金钱-10 心情+10 健康值+10 行动点+1", option1_rect.x + 10, option1_rect.y + 10, (254, 247, 201))
            
            # 营养套餐
            pygame.draw.rect(self.screen, (220, 180, 140), option2_rect)
            pygame.draw.rect(self.screen, (150, 100, 50), option2_rect, 2)
            self.game.draw_text("营养套餐：金钱-15 心情+20 健康值+10 行动点+2", option2_rect.x + 10, option2_rect.y + 10, (254, 247, 201))
            
            # 特色美食
            pygame.draw.rect(self.screen, (220, 180, 140), option3_rect)
            pygame.draw.rect(self.screen, (150, 100, 50), option3_rect, 2)
            self.game.draw_text("特色美食：金钱-20 心情+30 健康值+10 行动点+3", option3_rect.x + 10, option3_rect.y + 10, (254, 247, 201))
        else:
            # 已用餐提示
            self.game.draw_text("已用餐", SCREEN_WIDTH // 2 - 50, 200, (254, 247, 201), self.large_font)
        
        # 绘制返回按钮
        pygame.draw.rect(self.screen, (220, 180, 140), back_rect)
        pygame.draw.rect(self.screen, (150, 100, 50), back_rect, 2)
        self.game.draw_text("返回地图", back_rect.x + 10, back_rect.y + 10, (254, 247, 201))
        
        # 绘制消息
        if self.game.message_timer > 0:
            self.game.draw_text(self.game.message, SCREEN_WIDTH // 2 - 300, SCREEN_HEIGHT - 60, (254, 247, 201), self.large_font)
            self.game.message_timer -= 1
    
    def handle_events(self, events):
        """处理食堂场景事件"""
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
                if not self.game.has_eaten:
                    if option1_rect.collidepoint(pos):
                        # 选择鸡腿套餐
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
                    elif option2_rect.collidepoint(pos):
                        # 选择营养套餐
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
                    elif option3_rect.collidepoint(pos):
                        # 选择特色美食
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
                # 返回地图
                if back_rect.collidepoint(pos):
                    self.game.current_state = "MAIN_GAME"
                    self.game.map_system.toggle_map()  # 确保地图显示
