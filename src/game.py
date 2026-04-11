import pygame
import json
import os
import sys

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from data.config import (
    SCREEN_WIDTH, SCREEN_HEIGHT, FPS, BLACK, WHITE, GRAY,
    DAILY_ACTION_POINTS, SAVE_FILE
)
from src.player import Player
from src.time_system import TimeSystem
from src.map import MapSystem


class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("USTB校园养成游戏")
        self.clock = pygame.time.Clock()
        # 尝试使用本地字体文件
        font_path = os.path.join(os.path.dirname(__file__), '..', 'fonts', 'msyh.ttf')
        self.font = None
        self.large_font = None
        
        try:
            if os.path.exists(font_path):
                self.font = pygame.font.Font(font_path, 24)
                self.large_font = pygame.font.Font(font_path, 36)
        except:
            pass
        
        # 如果本地字体失败，尝试使用系统字体
        if self.font is None or self.large_font is None:
            font_names = ['SimHei', 'Microsoft YaHei', 'Arial Unicode MS', 'sans-serif']
            for font_name in font_names:
                try:
                    if self.font is None:
                        self.font = pygame.font.SysFont(font_name, 24)
                    if self.large_font is None:
                        self.large_font = pygame.font.SysFont(font_name, 36)
                    if self.font and self.large_font:
                        break
                except:
                    continue
        
        # 如果所有字体都失败，使用默认字体
        if self.font is None:
            self.font = pygame.font.Font(None, 24)
        if self.large_font is None:
            self.large_font = pygame.font.Font(None, 36)
        
        self.player = Player()
        self.time_system = TimeSystem()
        self.map_system = MapSystem()
        self.running = True
        self.message = ""
        self.message_timer = 0
        
        # 加载地图背景图片
        self.map_background = None
        map_image_path = os.path.join(os.path.dirname(__file__), '..', 'map_background.jpg')
        if os.path.exists(map_image_path):
            try:
                self.map_background = pygame.image.load(map_image_path)
                # 调整图片大小以适应屏幕
                self.map_background = pygame.transform.scale(self.map_background, (SCREEN_WIDTH, SCREEN_HEIGHT))
            except Exception as e:
                print(f"加载地图背景图片失败: {e}")
        
        self.player.action_points = DAILY_ACTION_POINTS
    
    def reset(self):
        self.player.reset()
        self.time_system.reset()
        self.player.action_points = DAILY_ACTION_POINTS
        self.message = "新游戏开始！"
        self.message_timer = 120
    
    def save_game(self):
        try:
            save_data = {
                'player': self.player.to_dict(),
                'time_system': self.time_system.to_dict()
            }
            os.makedirs(os.path.dirname(SAVE_FILE), exist_ok=True)
            with open(SAVE_FILE, 'w', encoding='utf-8') as f:
                json.dump(save_data, f, ensure_ascii=False, indent=2)
            self.message = "游戏已保存！"
            self.message_timer = 120
        except Exception as e:
            self.message = f"保存失败: {str(e)}"
            self.message_timer = 120
    
    def load_game(self):
        try:
            if os.path.exists(SAVE_FILE):
                with open(SAVE_FILE, 'r', encoding='utf-8') as f:
                    save_data = json.load(f)
                self.player.from_dict(save_data['player'])
                self.time_system.from_dict(save_data['time_system'])
                self.message = "游戏已加载！"
                self.message_timer = 120
            else:
                self.message = "没有找到存档！"
                self.message_timer = 120
        except Exception as e:
            self.message = f"加载失败: {str(e)}"
            self.message_timer = 120
    
    def advance_day(self):
        if self.time_system.is_ended():
            self.message = "游戏已结束！"
            self.message_timer = 120
            return
        
        self.time_system.next_day()
        self.player.action_points = DAILY_ACTION_POINTS
        
        self.player.change_attribute('mood', -2)
        self.player.change_attribute('health', -1)
        
        if self.time_system.is_ended():
            self.message = "恭喜！你完成了128天的校园生活！"
            self.message_timer = 300
        else:
            self.message = f"新的一天开始了！{self.time_system.get_time_display()}"
            self.message_timer = 120
    
    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    self.running = False
                elif event.key == pygame.K_SPACE:
                    if not self.map_system.is_map_showing():
                        self.advance_day()
                elif event.key == pygame.K_s:
                    if not self.map_system.is_map_showing():
                        self.save_game()
                elif event.key == pygame.K_l:
                    if not self.map_system.is_map_showing():
                        self.load_game()
                elif event.key == pygame.K_m:
                    self.map_system.toggle_map()
                    self.map_system.clear_active_area()
                elif event.key == pygame.K_1:
                    if not self.map_system.is_map_showing():
                        self.do_action("学习")
                    else:
                        self.handle_map_action(0)
                elif event.key == pygame.K_2:
                    if not self.map_system.is_map_showing():
                        self.do_action("运动")
                    else:
                        self.handle_map_action(1)
                elif event.key == pygame.K_3:
                    if not self.map_system.is_map_showing():
                        self.do_action("休息")
                elif event.key == pygame.K_4:
                    if not self.map_system.is_map_showing():
                        self.do_action("打工")
                elif event.key == pygame.K_5:
                    if not self.map_system.is_map_showing():
                        self.do_action("社交")
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if self.map_system.is_map_showing():
                    pos = pygame.mouse.get_pos()
                    area_id = self.map_system.get_area_at(pos)
                    if area_id:
                        self.map_system.set_active_area(area_id)
                    else:
                        self.map_system.clear_active_area()
    
    def do_action(self, action_name):
        if self.player.action_points <= 0:
            self.message = "行动点不足！"
            self.message_timer = 60
            return
        
        self.player.action_points -= 1
        
        if action_name == "学习":
            self.player.change_attribute('intelligence', 5)
            self.player.change_attribute('mood', -3)
            self.player.change_attribute('health', -2)
            self.message = "努力学习，智力+5"
        elif action_name == "运动":
            self.player.change_attribute('physical', 5)
            self.player.change_attribute('health', 3)
            self.player.change_attribute('mood', 2)
            self.message = "运动健身，体力+5"
        elif action_name == "休息":
            self.player.change_attribute('health', 5)
            self.player.change_attribute('mood', 5)
            self.player.change_attribute('physical', -1)
            self.message = "好好休息，恢复体力"
        elif action_name == "打工":
            self.player.change_attribute('gold', 100)
            self.player.change_attribute('mood', -5)
            self.player.change_attribute('health', -3)
            self.message = "辛苦打工，金币+100"
        elif action_name == "社交":
            self.player.change_attribute('charm', 3)
            self.player.change_attribute('mood', 5)
            self.player.change_attribute('gold', -20)
            self.message = "社交活动，魅力+3"
        
        self.message_timer = 90
    
    def handle_map_action(self, action_index):
        if self.player.action_points <= 0:
            self.message = "行动点不足！"
            self.message_timer = 60
            return
        
        active_area = self.map_system.active_area
        if not active_area:
            return
        
        area = self.map_system.get_area(active_area)
        if not area or action_index >= len(area['actions']):
            return
        
        action = area['actions'][action_index]
        self.player.action_points -= 1
        
        # 应用行动效果
        effects = action['effects']
        effect_messages = []
        for attr, value in effects.items():
            self.player.change_attribute(attr, value)
            effect_messages.append(f"{attr}: {value:+d}")
        
        self.message = f"{area['name']}: {action['name']} - {', '.join(effect_messages)}"
        self.message_timer = 90
    
    def draw_text(self, text, x, y, color=WHITE, font=None):
        if font is None:
            font = self.font
        text_surface = font.render(text, True, color)
        self.screen.blit(text_surface, (x, y))
    
    def draw_map(self):
        # 绘制地图背景图片
        if self.map_background:
            self.screen.blit(self.map_background, (0, 0))
        else:
            # 如果没有背景图片，使用默认背景色
            self.screen.fill((50, 50, 50))
        
        # 绘制地图标题
        self.draw_text("校园地图", SCREEN_WIDTH // 2 - 100, 30, (80, 40, 0), self.large_font)  # 深棕色文字
        
        # 绘制各个区域（带背景色和文字）
        for area_id, area in self.map_system.areas.items():
            # 绘制区域背景
            pygame.draw.rect(self.screen, area['bg_color'], area['rect'])
            # 绘制区域边框
            pygame.draw.rect(self.screen, area['border_color'], area['rect'], 2)
            
            # 绘制区域名称
            name_text = self.font.render(area['name'], True, area['text_color'])
            text_rect = name_text.get_rect(center=area['rect'].center)
            self.screen.blit(name_text, text_rect)
        
        # 绘制操作说明
        self.draw_text("点击区域查看详情，按M返回主界面", 20, SCREEN_HEIGHT - 50, (80, 40, 0))  # 深棕色文字
        
        pygame.display.flip()
    
    def draw(self):
        if self.map_system.is_map_showing():
            self.draw_map()
            return
        
        self.screen.fill(BLACK)
        
        self.draw_text(self.time_system.get_time_display(), 20, 20, WHITE, self.large_font)
        
        y_offset = 80
        attr_names = {
            'health': '健康',
            'mood': '心情',
            'intelligence': '智力',
            'physical': '体力',
            'charm': '魅力',
            'gold': '金币'
        }
        
        for attr, name in attr_names.items():
            value = self.player.get_attribute(attr)
            self.draw_text(f"{name}: {value}", 20, y_offset)
            y_offset += 30
        
        self.draw_text(f"行动点: {self.player.action_points}", 20, y_offset + 10)
        y_offset += 50
        
        self.draw_text("可用行动:", 20, y_offset)
        y_offset += 30
        actions = [
            "[1] 学习 (智力+5)",
            "[2] 运动 (体力+5)",
            "[3] 休息 (恢复)",
            "[4] 打工 (金币+100)",
            "[5] 社交 (魅力+3)"
        ]
        
        for action in actions:
            self.draw_text(action, 40, y_offset)
            y_offset += 25
        
        y_offset += 20
        self.draw_text("操作说明:", 20, y_offset)
        y_offset += 30
        self.draw_text("[空格] 推进一天  [S] 存档  [L] 读档  [M] 打开地图  [Q] 退出", 40, y_offset)
        
        if self.message_timer > 0:
            self.draw_text(self.message, SCREEN_WIDTH // 2 - 150, SCREEN_HEIGHT - 80, WHITE, self.large_font)
            self.message_timer -= 1
        
        pygame.display.flip()
    
    def run(self):
        while self.running:
            self.handle_events()
            self.draw()
            self.clock.tick(FPS)
        pygame.quit()
