import pygame
import os
import sys
import json

class LoadGameScene:
    def __init__(self, screen):
        self.screen = screen
        self.running = True
        
        # 加载背景图片
        self.background = None
        background_path = os.path.join(os.path.dirname(__file__), '..', 'image', 'start_background.png')
        try:
            if os.path.exists(background_path):
                self.background = pygame.image.load(background_path)
                self.background = pygame.transform.scale(self.background, (1280, 720))
        except Exception as e:
            print(f"加载背景图片失败: {e}")
        
        # 加载字体
        self.font = None
        font_path = os.path.join(os.path.dirname(__file__), '..', 'fonts', 'msyh.ttf')
        try:
            if os.path.exists(font_path):
                self.font = pygame.font.Font(font_path, 24)
            else:
                self.font = pygame.font.SysFont('SimHei', 24)
        except:
            self.font = pygame.font.Font(None, 24)
        
        # 加载标题字体
        self.title_font = None
        try:
            if os.path.exists(font_path):
                self.title_font = pygame.font.Font(font_path, 36)
            else:
                self.title_font = pygame.font.SysFont('SimHei', 36)
        except:
            self.title_font = pygame.font.Font(None, 36)
        
        # 存档文件路径
        self.save_dir = os.path.join(os.path.dirname(__file__), '..', 'save')
        self.save_files = []
        self._load_save_files()
        
        # 按钮配置
        self.back_button = pygame.Rect(50, 620, 150, 50)
        
        # 滚动偏移
        self.scroll_offset = 0
        self.scroll_speed = 20
    
    def _load_save_files(self):
        """加载所有存档文件"""
        self.save_files = []
        if os.path.exists(self.save_dir):
            for file_name in os.listdir(self.save_dir):
                if file_name.endswith('.json') and file_name != 'savegame.json':
                    file_path = os.path.join(self.save_dir, file_name)
                    try:
                        with open(file_path, 'r', encoding='utf-8') as f:
                            save_data = json.load(f)
                        
                        # 提取存档信息
                        character_name = save_data.get('character', {}).get('name', '未知角色')
                        time_data = save_data.get('time_system', {})
                        day = time_data.get('day', 1)
                        
                        # 计算时间显示
                        time_display = self._calculate_time_display(day)
                        
                        # 获取文件修改时间
                        mtime = os.path.getmtime(file_path)
                        
                        self.save_files.append({
                            'file_name': file_name,
                            'file_path': file_path,
                            'name': character_name,
                            'time': time_display,
                            'mtime': mtime
                        })
                    except Exception as e:
                        print(f"读取存档文件失败: {e}")
            
            # 按修改时间排序，最新的在前
            self.save_files.sort(key=lambda x: x['mtime'], reverse=True)
    
    def _calculate_time_display(self, day):
        """计算时间显示"""
        semester = (day - 1) // 17 + 1
        year = ((semester - 1) // 2) + 1
        week_in_semester = (day - 1) % 17
        if semester % 2 == 1:
            if week_in_semester < 16:
                month_index = week_in_semester // 4
                months = [9, 10, 11, 12]
                month = months[month_index]
            else:
                month = 1
        else:
            if week_in_semester < 16:
                month_index = week_in_semester // 4
                months = [3, 4, 5, 6]
                month = months[month_index]
            else:
                month = 7
        if week_in_semester == 16:
            week_in_month = "期末周"
        else:
            week_in_month = (week_in_semester % 4) + 1
        if week_in_month == "期末周":
            return f"第 {year} 年 {month} 月 期末周"
        else:
            return f"第 {year} 年 {month} 月 第 {week_in_month} 周"
    
    def handle_events(self, events):
        """处理事件"""
        for event in events:
            if event.type == pygame.QUIT:
                self.running = False
                return None
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # 左键点击
                    result = self._handle_mouse_click(event.pos)
                    if result:
                        return result
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return 'START_SCENE'
        return None
    
    def _handle_mouse_click(self, pos):
        """处理鼠标点击"""
        # 检查返回按钮
        if self.back_button.collidepoint(pos):
            return 'START_SCENE'
        
        # 检查存档项和删除按钮
        y_start = 150
        for i, save_file in enumerate(self.save_files):
            save_rect = pygame.Rect(340, y_start + i * 80 - self.scroll_offset, 600, 60)
            delete_button_rect = pygame.Rect(880, y_start + i * 80 + 15 - self.scroll_offset, 60, 30)
            
            if delete_button_rect.collidepoint(pos):
                # 删除存档
                try:
                    os.remove(save_file['file_path'])
                    # 重新加载存档列表
                    self._load_save_files()
                except Exception as e:
                    print(f"删除存档失败: {e}")
                return None
            elif save_rect.collidepoint(pos):
                return {'GAME_SCENE': save_file['file_path']}
        
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
            self.screen.fill((0, 0, 0))
        
        # 绘制标题
        title = self.title_font.render("读档", True, (197, 110, 57))
        title_rect = title.get_rect(center=(640, 80))
        self.screen.blit(title, title_rect)
        
        # 绘制存档列表
        y_start = 150
        for i, save_file in enumerate(self.save_files):
            save_rect = pygame.Rect(340, y_start + i * 80 - self.scroll_offset, 600, 60)
            delete_button_rect = pygame.Rect(880, y_start + i * 80 + 15 - self.scroll_offset, 60, 30)
            
            # 绘制存档框（暖色调）
            pygame.draw.rect(self.screen, (220, 180, 140), save_rect)
            pygame.draw.rect(self.screen, (197, 110, 57), save_rect, 2)
            
            # 绘制删除按钮
            pygame.draw.rect(self.screen, (180, 80, 50), delete_button_rect)
            pygame.draw.rect(self.screen, (150, 60, 30), delete_button_rect, 2)
            delete_text = self.font.render("删除", True, (254, 247, 201))
            delete_text_rect = delete_text.get_rect(center=delete_button_rect.center)
            self.screen.blit(delete_text, delete_text_rect)
            
            # 绘制存档信息
            name_text = self.font.render(f"角色: {save_file['name']}", True, (255, 255, 255))
            time_text = self.font.render(f"时间: {save_file['time']}", True, (200, 200, 200))
            
            self.screen.blit(name_text, (save_rect.x + 20, save_rect.y + 10))
            self.screen.blit(time_text, (save_rect.x + 20, save_rect.y + 35))
        
        # 绘制返回按钮（暖色调）
        pygame.draw.rect(self.screen, (220, 180, 140), self.back_button)
        pygame.draw.rect(self.screen, (197, 110, 57), self.back_button, 2)
        back_text = self.font.render("返回", True, (254, 247, 201))
        back_text_rect = back_text.get_rect(center=self.back_button.center)
        self.screen.blit(back_text, back_text_rect)
        
        # 绘制提示文字
        if not self.save_files:
            # 绘制提示框
            no_save_box_rect = pygame.Rect(500, 250, 280, 100)
            pygame.draw.rect(self.screen, (220, 180, 140), no_save_box_rect)
            pygame.draw.rect(self.screen, (197, 110, 57), no_save_box_rect, 2)
            # 绘制提示文字
            no_save_text = self.font.render("没有找到存档", True, (254, 247, 201))
            no_save_rect = no_save_text.get_rect(center=(640, 300))
            self.screen.blit(no_save_text, no_save_rect)