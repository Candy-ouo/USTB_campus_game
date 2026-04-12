import pygame
import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from data.config import SCREEN_WIDTH, SCREEN_HEIGHT, FPS


class StartScene:
    def __init__(self, screen):
        self.screen = screen
        self.running = True
        
        # 加载背景图片
        self.background = None
        background_path = os.path.join(os.path.dirname(__file__), '..', 'image', 'start_background.png')
        try:
            if os.path.exists(background_path):
                self.background = pygame.image.load(background_path)
                self.background = pygame.transform.scale(self.background, (SCREEN_WIDTH, SCREEN_HEIGHT))
        except Exception as e:
            print(f"加载背景图片失败: {e}")
        
        # 加载标题图片
        self.title_image = None
        title_path = os.path.join(os.path.dirname(__file__), '..', 'image', 'start_title.png')
        try:
            if os.path.exists(title_path):
                self.title_image = pygame.image.load(title_path)
        except Exception as e:
            print(f"加载标题图片失败: {e}")
        
        # 加载按钮背景图片
        self.button_background = None
        button_bg_path = os.path.join(os.path.dirname(__file__), '..', 'image', 'start_button_background.png')
        try:
            if os.path.exists(button_bg_path):
                self.button_background = pygame.image.load(button_bg_path)
        except Exception as e:
            print(f"加载按钮背景图片失败: {e}")
        
        # 加载字体
        self.font = None
        font_path = os.path.join(os.path.dirname(__file__), '..', 'fonts', 'fonts_start.ttf')
        try:
            if os.path.exists(font_path):
                self.font = pygame.font.Font(font_path, 40)
            else:
                self.font = pygame.font.SysFont('SimHei', 32)
        except:
            self.font = pygame.font.Font(None, 32)
        
        # 按钮配置（水平排列，靠下）
        self.button_width = 200
        self.button_height = 100
        self.button_spacing = 30
        
        # 计算按钮位置（水平居中，靠下）
        total_width = 3 * self.button_width + 2 * self.button_spacing
        start_x = (SCREEN_WIDTH - total_width) // 2
        start_y = SCREEN_HEIGHT - self.button_height - 100  # 距离底部100像素
        
        # 创建按钮矩形（只创建一次）
        self.buttons = {
            'new_game': pygame.Rect(start_x, start_y, self.button_width, self.button_height),
            'load_game': pygame.Rect(start_x + self.button_width + self.button_spacing, start_y, self.button_width, self.button_height),
            'exit': pygame.Rect(start_x + 2 * (self.button_width + self.button_spacing), start_y, self.button_width, self.button_height)
        }
        
        # 按钮文字
        self.button_texts = {
            'new_game': '新游戏',
            'load_game': '读档',
            'exit': '退出'
        }
    
    def handle_events(self, events):
        """处理事件，返回要切换的场景状态"""
        for event in events:
            if event.type == pygame.QUIT:
                self._exit_game()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # 左键点击
                    result = self._handle_mouse_click(event.pos)
                    if result:
                        return result
        return None
    
    def update(self):
        """更新状态"""
        pass
    
    def draw(self):
        """绘制界面"""
        # 绘制背景
        if self.background:
            self.screen.blit(self.background, (0, 0))
        else:
            # 如果背景图片加载失败，使用纯色背景
            self.screen.fill((0, 0, 0))
        
        # 绘制标题图片（水平居中靠上，缩小显示）
        if self.title_image:
            title_width, title_height = self.title_image.get_size()
            # 缩小图片到80%大小
            scale_factor = 0.8
            new_width = int(title_width * scale_factor)
            new_height = int(title_height * scale_factor)
            scaled_title = pygame.transform.scale(self.title_image, (new_width, new_height))
            # 计算位置
            title_x = (SCREEN_WIDTH - new_width) // 2
            title_y = 100  # 距离顶部像素
            self.screen.blit(scaled_title, (title_x, title_y))
        
        # 绘制按钮
        for button_name, rect in self.buttons.items():
            if self.button_background:
                # 保持图片比例缩放
                bg_width, bg_height = self.button_background.get_size()
                scale_factor = min(self.button_width / bg_width, self.button_height / bg_height)
                new_width = int(bg_width * scale_factor)
                new_height = int(bg_height * scale_factor)
                scaled_button = pygame.transform.scale(self.button_background, (new_width, new_height))
                # 居中显示
                x = rect.x + (self.button_width - new_width) // 2
                y = rect.y + (self.button_height - new_height) // 2
                self.screen.blit(scaled_button, (x, y))
            else:
                # 如果按钮背景加载失败，使用纯色按钮
                pygame.draw.rect(self.screen, (100, 100, 100), rect)
                pygame.draw.rect(self.screen, (200, 200, 200), rect, 2)
            
            # 绘制按钮文字
            text = self.font.render(self.button_texts[button_name], True, (197, 110, 57))
            text_rect = text.get_rect(center=rect.center)
            self.screen.blit(text, text_rect)
    
    def _handle_mouse_click(self, pos):
        """处理鼠标点击事件"""
        for button_name, rect in self.buttons.items():
            if rect.collidepoint(pos):
                if button_name == 'new_game':
                    return 'CREATE_CHARACTER_SCENE'
                elif button_name == 'load_game':
                    # 尝试读取存档
                    save_file = os.path.join(os.path.dirname(__file__), '..', 'save', 'savegame.json')
                    if os.path.exists(save_file):
                        return 'GAME_SCENE'
                    else:
                        # 存档不存在，可以添加提示
                        print("存档不存在")
                elif button_name == 'exit':
                    self._exit_game()
        return None
    
    def _draw(self):
        """绘制界面"""
        # 绘制背景
        if self.background:
            self.screen.blit(self.background, (0, 0))
        else:
            # 如果背景图片加载失败，使用纯色背景
            self.screen.fill((0, 0, 0))
        
        # 绘制按钮
        for button_name, rect in self.buttons.items():
            if self.button_background:
                # 保持图片比例缩放
                bg_width, bg_height = self.button_background.get_size()
                scale_factor = min(self.button_width / bg_width, self.button_height / bg_height)
                new_width = int(bg_width * scale_factor)
                new_height = int(bg_height * scale_factor)
                scaled_button = pygame.transform.scale(self.button_background, (new_width, new_height))
                # 居中显示
                x = rect.x + (self.button_width - new_width) // 2
                y = rect.y + (self.button_height - new_height) // 2
                self.screen.blit(scaled_button, (x, y))
            else:
                # 如果按钮背景加载失败，使用纯色按钮
                pygame.draw.rect(self.screen, (100, 100, 100), rect)
                pygame.draw.rect(self.screen, (200, 200, 200), rect, 2)
            
            # 绘制按钮文字
            text = self.font.render(self.button_texts[button_name], True, (255, 255, 255))
            text_rect = text.get_rect(center=rect.center)
            self.screen.blit(text, text_rect)
    
    def _exit_game(self):
        """安全退出游戏"""
        pygame.quit()
        sys.exit()
