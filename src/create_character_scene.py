
import pygame
from typing import Optional
from src.character import Character, COLLEGE_MAJORS


class CreateCharacterScene:
    
    
    # 颜色定义
    COLOR_BG = (255, 223, 186)  # 暖橙色背景
    COLOR_WOOD = (139, 69, 19)   # 棕色木质边框
    COLOR_WOOD_LIGHT = (160, 82, 45)  # 浅棕色
    COLOR_WOOD_DARK = (101, 67, 33)   # 深棕色
    COLOR_TEXT = (85, 45, 17)     # 文字颜色
    COLOR_HIGHLIGHT = (178, 34, 34)  # 高亮颜色
    COLOR_ACTIVE = (255, 165, 0)     # 激活颜色
    COLOR_INPUT_BG = (255, 250, 240)  # 输入框背景
    
    # 配色方案
    COLOR_SCHEMES = [
        (255, 100, 100),  # 红色
        (100, 255, 100),  # 绿色
        (100, 100, 255),  # 蓝色
        (255, 255, 100),  # 黄色
        (255, 100, 255),  # 紫色
        (255, 255, 255),  # 白色
        (0, 0, 0),          # 黑色
    ]
    
    # 样式名称
    HAIR_STYLES = ["短发", "中发", "长发", "马尾辫", "爆炸头"]
    TOP_STYLES = ["T恤", "衬衫", "卫衣", "西装", "运动衫"]
    PANTS_STYLES = ["牛仔裤", "休闲裤", "短裤", "运动裤", "裙子"]
    
    def __init__(self, screen: pygame.Surface, font, large_font):
        self.screen = screen
        self.font = font
        self.large_font = large_font
        # 动态获取窗口大小
        self.screen_width = screen.get_width()
        self.screen_height = screen.get_height()
        # 保持与 game.py 的兼容性
        self.width = self.screen_width
        self.height = self.screen_height
        
        # 角色数据
        self.name = ""
        self.gender = "男"
        self.character_height = 170
        self.weight = 60
        self.birth_month = 1
        self.birth_day = 1
        self.college_index = 0
        self.college_list = list(COLLEGE_MAJORS.keys())
        self.hair_style = 0
        self.top_style = 0
        self.pants_style = 0
        self.hair_color = 0  # 发型颜色索引
        self.top_color = 1   # 上衣颜色索引
        self.pants_color = 2  # 裤子颜色索引
        
        # 激活的输入框/选项
        self.active_field = "name"  # name, gender, height, weight, birthday_month, birthday_day, college, hair, hair_color, top, top_color, pants, pants_color
        
        # 光标闪烁
        self.cursor_visible = True
        self.cursor_timer = 0
        self.cursor_interval = 500  # 毫秒
        
        # 字段顺序，用于方向键导航
        self.fields = ["name", "gender", "height", "weight", "birthday_month", "birthday_day", "college", "hair", "hair_color", "top", "top_color", "pants", "pants_color"]
        self.current_field_index = 0
        
        # 下拉框状态
        self.college_dropdown_open = False
    
    def handle_events(self, events: list) -> Optional[Character]:
        """处理事件，返回 Character 表示创建完成"""
        for event in events:
            if event.type == pygame.QUIT:
                return None
            
            elif event.type == pygame.KEYDOWN:
                # ESC 退出
                if event.key == pygame.K_ESCAPE:
                    return None
                
                # Enter 确认
                elif event.key == pygame.K_RETURN:
                    # 检查姓名是否为空
                    if not self.name:
                        self.name = "玩家"
                    return self._create_character()
                
                # 方向键导航
                elif event.key == pygame.K_TAB:
                    # 切换到下一个字段
                    self.current_field_index = (self.current_field_index + 1) % len(self.fields)
                    self.active_field = self.fields[self.current_field_index]
                    # 关闭下拉框
                    self.college_dropdown_open = False
                
                # 方向键调整数值
                elif event.key in (pygame.K_UP, pygame.K_DOWN, pygame.K_LEFT, pygame.K_RIGHT):
                    self._handle_navigation(event.key)
                
                # 退格键
                elif event.key == pygame.K_BACKSPACE and self.active_field == "name":
                    self.name = self.name[:-1]
                
                # 文本输入（处理中文）
                elif self.active_field == "name" and event.unicode:
                    if len(self.name) < 10:
                        # 直接添加 unicode 字符，包括中文
                        self.name += event.unicode
            
            # 文本输入事件（处理中文输入）
            elif event.type == pygame.TEXTINPUT and self.active_field == "name":
                if len(self.name) < 10:
                    # 直接添加文本，包括中文
                    self.name += event.text
            
            # 鼠标事件
            elif event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                result = self._handle_mouse_click(pos)
                if result is not None:
                    return result
        
        return None
    
    def _handle_navigation(self, key):
        """处理方向键导航"""
        if self.active_field == "gender":
            if key in (pygame.K_UP, pygame.K_DOWN):
                self.gender = "女" if self.gender == "男" else "男"
        
        elif self.active_field == "height":
            if key == pygame.K_UP and self.character_height < 210:
                self.character_height += 1
            elif key == pygame.K_DOWN and self.character_height > 140:
                self.character_height -= 1
            elif key == pygame.K_LEFT and self.character_height > 140:
                self.character_height -= 1
            elif key == pygame.K_RIGHT and self.character_height < 210:
                self.character_height += 1
        
        elif self.active_field == "weight":
            if key == pygame.K_UP and self.weight < 150:
                self.weight += 1
            elif key == pygame.K_DOWN and self.weight > 40:
                self.weight -= 1
            elif key == pygame.K_LEFT and self.weight > 40:
                self.weight -= 1
            elif key == pygame.K_RIGHT and self.weight < 150:
                self.weight += 1
        
        elif self.active_field == "birthday_month":
            if key == pygame.K_UP and self.birth_month < 12:
                self.birth_month += 1
                # 调整日期
                max_day = self._get_max_day(self.birth_month)
                if self.birth_day > max_day:
                    self.birth_day = max_day
            elif key == pygame.K_DOWN and self.birth_month > 1:
                self.birth_month -= 1
                # 调整日期
                max_day = self._get_max_day(self.birth_month)
                if self.birth_day > max_day:
                    self.birth_day = max_day
        
        elif self.active_field == "birthday_day":
            max_day = self._get_max_day(self.birth_month)
            if key == pygame.K_UP and self.birth_day < max_day:
                self.birth_day += 1
            elif key == pygame.K_DOWN and self.birth_day > 1:
                self.birth_day -= 1
        
        elif self.active_field == "college":
            if key == pygame.K_UP and self.college_index > 0:
                self.college_index -= 1
            elif key == pygame.K_DOWN and self.college_index < len(self.college_list) - 1:
                self.college_index += 1
        
        elif self.active_field == "hair":
            if key == pygame.K_LEFT and self.hair_style > 0:
                self.hair_style -= 1
            elif key == pygame.K_RIGHT and self.hair_style < 4:
                self.hair_style += 1
        
        elif self.active_field == "hair_color":
            if key == pygame.K_LEFT and self.hair_color > 0:
                self.hair_color -= 1
            elif key == pygame.K_RIGHT and self.hair_color < 6:
                self.hair_color += 1
        
        elif self.active_field == "top":
            if key == pygame.K_LEFT and self.top_style > 0:
                self.top_style -= 1
            elif key == pygame.K_RIGHT and self.top_style < 4:
                self.top_style += 1
        
        elif self.active_field == "top_color":
            if key == pygame.K_LEFT and self.top_color > 0:
                self.top_color -= 1
            elif key == pygame.K_RIGHT and self.top_color < 6:
                self.top_color += 1
        
        elif self.active_field == "pants":
            if key == pygame.K_LEFT and self.pants_style > 0:
                self.pants_style -= 1
            elif key == pygame.K_RIGHT and self.pants_style < 4:
                self.pants_style += 1
        
        elif self.active_field == "pants_color":
            if key == pygame.K_LEFT and self.pants_color > 0:
                self.pants_color -= 1
            elif key == pygame.K_RIGHT and self.pants_color < 6:
                self.pants_color += 1
    
    def _handle_mouse_click(self, pos):
        """处理鼠标点击"""
        # 实时更新窗口大小
        self.screen_width = self.screen.get_width()
        self.screen_height = self.screen.get_height()
        # 保持与 game.py 的兼容性
        self.width = self.screen_width
        self.height = self.screen_height
        
        # 计算编辑区起始位置
        preview_width = min(400, self.screen_width // 2 - 40)
        editor_start_x = preview_width + 30
        editor_width = self.screen_width - preview_width - 60
        
        # 计算可用高度和元素间距
        available_height = self.screen_height - 120  # 顶部60 + 底部60
        element_count = 8  # 姓名、性别、身高体重、生日、学院、发型、上衣、裤子
        base_spacing = 45  # 增加间距
        
        # 确保间距合适，避免重叠
        if available_height < element_count * base_spacing:
            spacing = available_height // element_count
        else:
            spacing = base_spacing
        
        # 姓名输入框
        y_offset = 100
        name_rect = pygame.Rect(editor_start_x + 90, y_offset - 10, min(200, editor_width - 100), 30)  # 减小框大小
        if name_rect.collidepoint(pos):
            self.active_field = "name"
            self.current_field_index = self.fields.index("name")
            self.college_dropdown_open = False
        
        # 性别选择
        y_offset += spacing
        gender_rect = pygame.Rect(editor_start_x + 90, y_offset - 10, 150, 35)  # 减小框大小
        if gender_rect.collidepoint(pos):
            self.active_field = "gender"
            self.current_field_index = self.fields.index("gender")
            self.college_dropdown_open = False
        
        # 身高
        y_offset += spacing
        height_rect = pygame.Rect(editor_start_x + 90, y_offset - 10, 70, 30)  # 减小框大小
        if height_rect.collidepoint(pos):
            self.active_field = "height"
            self.current_field_index = self.fields.index("height")
            self.college_dropdown_open = False
        
        # 体重
        weight_rect = pygame.Rect(editor_start_x + 240, y_offset - 10, 70, 30)  # 减小框大小，再靠右一点
        if weight_rect.collidepoint(pos):
            self.active_field = "weight"
            self.current_field_index = self.fields.index("weight")
            self.college_dropdown_open = False
        
        # 生日
        y_offset += spacing
        month_rect = pygame.Rect(editor_start_x + 90, y_offset - 10, 50, 30)  # 减小框大小
        day_rect = pygame.Rect(editor_start_x + 150, y_offset - 10, 50, 30)  # 减小框大小
        if month_rect.collidepoint(pos):
            self.active_field = "birthday_month"
            self.current_field_index = self.fields.index("birthday_month")
            self.college_dropdown_open = False
        elif day_rect.collidepoint(pos):
            self.active_field = "birthday_day"
            self.current_field_index = self.fields.index("birthday_day")
            self.college_dropdown_open = False
        
        # 学院
        y_offset += spacing
        college_rect = pygame.Rect(editor_start_x + 90, y_offset - 10, min(180, editor_width - 100), 30)  # 减小框大小
        if college_rect.collidepoint(pos):
            self.active_field = "college"
            self.current_field_index = self.fields.index("college")
            self.college_dropdown_open = not self.college_dropdown_open
        
        # 学院下拉框选项
        if self.college_dropdown_open:
            dropdown_y = 100 + spacing * 4 - 10 + 35  # 学院字段的位置
            for i, college in enumerate(self.college_list):
                option_rect = pygame.Rect(editor_start_x + 90, dropdown_y + 2 + i * 30, min(180, editor_width - 100), 30)
                if option_rect.collidepoint(pos):
                    self.college_index = i
                    self.college_dropdown_open = False
        
        # 形象编辑 - 发型
        y_offset += spacing
        hair_rect = pygame.Rect(editor_start_x + 90, y_offset - 10, 70, 30)  # 减小框大小
        hair_color_rect = pygame.Rect(editor_start_x + 240, y_offset - 10, 70, 30)  # 减小框大小，再靠右一点
        if hair_rect.collidepoint(pos):
            self.active_field = "hair"
            self.current_field_index = self.fields.index("hair")
            self.college_dropdown_open = False
        elif hair_color_rect.collidepoint(pos):
            self.active_field = "hair_color"
            self.current_field_index = self.fields.index("hair_color")
            self.college_dropdown_open = False
        
        # 形象编辑 - 上衣
        y_offset += spacing
        top_rect = pygame.Rect(editor_start_x + 90, y_offset - 10, 70, 30)  # 减小框大小
        top_color_rect = pygame.Rect(editor_start_x + 240, y_offset - 10, 70, 30)  # 减小框大小，再靠右一点
        if top_rect.collidepoint(pos):
            self.active_field = "top"
            self.current_field_index = self.fields.index("top")
            self.college_dropdown_open = False
        elif top_color_rect.collidepoint(pos):
            self.active_field = "top_color"
            self.current_field_index = self.fields.index("top_color")
            self.college_dropdown_open = False
        
        # 形象编辑 - 裤子
        y_offset += spacing
        pants_rect = pygame.Rect(editor_start_x + 90, y_offset - 10, 70, 30)  # 减小框大小
        pants_color_rect = pygame.Rect(editor_start_x + 240, y_offset - 10, 70, 30)  # 减小框大小，再靠右一点
        if pants_rect.collidepoint(pos):
            self.active_field = "pants"
            self.current_field_index = self.fields.index("pants")
            self.college_dropdown_open = False
        elif pants_color_rect.collidepoint(pos):
            self.active_field = "pants_color"
            self.current_field_index = self.fields.index("pants_color")
            self.college_dropdown_open = False
        
        # 确认按钮
        confirm_rect = pygame.Rect(self.screen_width - 130, self.screen_height - 70, 100, 40)
        if confirm_rect.collidepoint(pos):
            if not self.name:
                self.name = "玩家"
            return self._create_character()
    
    def _get_max_day(self, month: int) -> int:
        """获取月份的最大天数"""
        if month in (1, 3, 5, 7, 8, 10, 12):
            return 31
        elif month in (4, 6, 9, 11):
            return 30
        else:  # 2月
            return 28
    
    def _create_character(self) -> Character:
        """创建角色对象"""
        college = self.college_list[self.college_index]
        birthday = f"{self.birth_month:02d}-{self.birth_day:02d}"
        
        character = Character(
            name=self.name,
            gender=self.gender,
            height=self.character_height,
            weight=self.weight,
            birthday=birthday,
            college=college,
            major=Character.get_major_by_college(college),
            hair_style=self.hair_style,
            top_style=self.top_style,
            pants_style=self.pants_style,
            color=self.hair_color  # 保存头发颜色作为主颜色
        )
        
        # 打印角色数据
        print("角色创建完成！")
        print(f"姓名: {character.name}")
        print(f"性别: {character.gender}")
        print(f"身高: {character.height} cm")
        print(f"体重: {character.weight} kg")
        print(f"生日: {character.birthday}")
        print(f"学院: {character.college}")
        print(f"专业: {character.major}")
        print(f"发型: {self.HAIR_STYLES[character.hair_style]}")
        print(f"上衣: {self.TOP_STYLES[character.top_style]}")
        print(f"裤子: {self.PANTS_STYLES[character.pants_style]}")
        print(f"发型颜色: {self.hair_color}")
        print(f"上衣颜色: {self.top_color}")
        print(f"裤子颜色: {self.pants_color}")
        print(f"绩点: {character.gpa}")
        print(f"体能: {character.energy}")
        print(f"人脉: {character.social}")
        print(f"技能: {character.skill}")
        print(f"心情: {character.mood}")
        print(f"逻辑: {character.logic}")
        print(f"创造: {character.creativity}")
        print(f"情商: {character.eq}")
        print(f"魅力: {character.charm}")
        print(f"专注: {character.focus}")
        print(f"幸运: {character.luck}")
        
        return character
    
    def update(self):
        """更新状态"""
        current_time = pygame.time.get_ticks()
        if current_time - self.cursor_timer > self.cursor_interval:
            self.cursor_visible = not self.cursor_visible
            self.cursor_timer = current_time
    
    def draw(self):
        """绘制界面"""
        # 动态更新窗口大小
        self.screen_width = self.screen.get_width()
        self.screen_height = self.screen.get_height()
        # 保持与 game.py 的兼容性
        self.width = self.screen_width
        self.height = self.screen_height
        
        # 背景
        self.screen.fill(self.COLOR_BG)
        
        # 木质边框
        self._draw_wooden_frame()
        
        # 左侧角色预览区
        self._draw_character_preview()
        
        # 右侧属性编辑区
        self._draw_attribute_editor()
        
        # 确认按钮
        self._draw_confirm_button()
    
    def _draw_wooden_frame(self):
        """绘制木质边框"""
        # 实时更新窗口大小
        self.screen_width = self.screen.get_width()
        self.screen_height = self.screen.get_height()
        # 保持与 game.py 的兼容性
        self.width = self.screen_width
        self.height = self.screen_height
        
        # 外边框
        pygame.draw.rect(self.screen, self.COLOR_WOOD_DARK, (10, 10, self.screen_width - 20, self.screen_height - 20), 4)
        # 内边框
        pygame.draw.rect(self.screen, self.COLOR_WOOD, (15, 15, self.screen_width - 30, self.screen_height - 30), 2)
        # 内填充
        pygame.draw.rect(self.screen, self.COLOR_WOOD_LIGHT, (17, 17, self.screen_width - 34, self.screen_height - 34), 1)
    
    def _draw_character_preview(self):
        """绘制角色预览区"""
        # 实时更新窗口大小
        self.screen_width = self.screen.get_width()
        self.screen_height = self.screen.get_height()
        # 保持与 game.py 的兼容性
        self.width = self.screen_width
        self.height = self.screen_height
        
        # 预览框
        preview_width = min(400, self.screen_width // 2 - 40)
        preview_rect = pygame.Rect(30, 30, preview_width, self.screen_height - 60)
        self._draw_wooden_box(preview_rect)
        
        # 标题
        self._draw_text("角色预览", 30 + preview_width // 2, 60, font=self.large_font, color=self.COLOR_HIGHLIGHT)
        
        # 背景
        sky_width = min(240, preview_width - 60)
        sky_height = min(200, (self.screen_height - 180) // 2)
        sky_x = 30 + (preview_width - sky_width) // 2
        sky_y = 120
        pygame.draw.rect(self.screen, (135, 206, 235), (sky_x, sky_y, sky_width, sky_height))  # 天空
        pygame.draw.rect(self.screen, (34, 139, 34), (sky_x, sky_y + sky_height, sky_width, 40))  # 草地
        
        # 角色坐标
        x, y = 30 + preview_width // 2, 150
        
        # 获取颜色
        hair_color = self.COLOR_SCHEMES[self.hair_color]
        top_color = self.COLOR_SCHEMES[self.top_color]
        pants_color = self.COLOR_SCHEMES[self.pants_color]
        
        # 绘制角色
        self._draw_pixel_character(x, y, hair_color, top_color, pants_color)
        
        # 角色信息
        preview_width = min(400, self.screen_width // 2 - 40)
        info_y = 380  # 增加图片和姓名之间的间隔
        if self.screen_height < 500:
            info_y = 120 + sky_height + 90  # 增加图片和姓名之间的间隔
        self._draw_text(f"姓名: {self.name}", 30 + preview_width // 2, info_y, font=self.font)
        self._draw_text(f"性别: {self.gender}", 30 + preview_width // 2, info_y + 35, font=self.font)  # 增加行间距
        self._draw_text(f"学院: {self.college_list[self.college_index]}", 30 + preview_width // 2, info_y + 70, font=self.font)  # 增加行间距
        self._draw_text(f"专业: {Character.get_major_by_college(self.college_list[self.college_index])}", 30 + preview_width // 2, info_y + 105, font=self.font)  # 增加行间距
    
    def _draw_pixel_character(self, x, y, hair_color, top_color, pants_color):
        """绘制像素风格角色"""
        # 头部
        pygame.draw.rect(self.screen, (255, 228, 196), (x-20, y, 40, 40))  # 头部
        
        # 发型（根据发型索引绘制不同样式）
        if self.hair_style == 0:
            # 短发
            pygame.draw.rect(self.screen, hair_color, (x-25, y-5, 50, 25))
        elif self.hair_style == 1:
            # 中发
            pygame.draw.rect(self.screen, hair_color, (x-25, y-10, 50, 35))
        elif self.hair_style == 2:
            # 长发
            pygame.draw.rect(self.screen, hair_color, (x-25, y-15, 50, 45))
        elif self.hair_style == 3:
            # 马尾辫
            pygame.draw.rect(self.screen, hair_color, (x-25, y-10, 35, 35))
            pygame.draw.rect(self.screen, hair_color, (x+10, y, 15, 30))
        elif self.hair_style == 4:
            # 爆炸头
            pygame.draw.rect(self.screen, hair_color, (x-30, y-15, 60, 50))
        
        # 眼睛
        pygame.draw.rect(self.screen, (0, 0, 0), (x-10, y+15, 8, 8))
        pygame.draw.rect(self.screen, (0, 0, 0), (x+2, y+15, 8, 8))
        
        # 身体（上衣）
        if self.top_style == 0:
            # T恤
            pygame.draw.rect(self.screen, top_color, (x-25, y+40, 50, 40))
        elif self.top_style == 1:
            # 衬衫
            pygame.draw.rect(self.screen, top_color, (x-25, y+40, 50, 45))
            pygame.draw.rect(self.screen, (200, 200, 200), (x-20, y+45, 40, 5))
        elif self.top_style == 2:
            # 卫衣
            pygame.draw.rect(self.screen, top_color, (x-30, y+35, 60, 45))
        elif self.top_style == 3:
            # 西装
            pygame.draw.rect(self.screen, top_color, (x-30, y+35, 60, 50))
            pygame.draw.rect(self.screen, (0, 0, 0), (x-25, y+40, 50, 5))
        elif self.top_style == 4:
            # 运动衫
            pygame.draw.rect(self.screen, top_color, (x-25, y+40, 50, 40))
            pygame.draw.rect(self.screen, (255, 255, 255), (x-15, y+50, 30, 10))
        
        # 裤子
        if self.pants_style == 0:
            # 牛仔裤
            pygame.draw.rect(self.screen, pants_color, (x-20, y+80, 40, 40))
        elif self.pants_style == 1:
            # 休闲裤
            pygame.draw.rect(self.screen, pants_color, (x-22, y+80, 44, 45))
        elif self.pants_style == 2:
            # 短裤
            pygame.draw.rect(self.screen, pants_color, (x-20, y+80, 40, 25))
        elif self.pants_style == 3:
            # 运动裤
            pygame.draw.rect(self.screen, pants_color, (x-25, y+80, 50, 40))
        elif self.pants_style == 4:
            # 裙子
            pygame.draw.polygon(self.screen, pants_color, [
                (x-25, y+80),
                (x+25, y+80),
                (x+30, y+120),
                (x-30, y+120)
            ])
        
        # 手臂
        pygame.draw.rect(self.screen, (255, 228, 196), (x-35, y+45, 15, 30))  # 左臂
        pygame.draw.rect(self.screen, (255, 228, 196), (x+20, y+45, 15, 30))  # 右臂
        
        # 腿部
        pygame.draw.rect(self.screen, (255, 228, 196), (x-15, y+120, 15, 30))  # 左腿
        pygame.draw.rect(self.screen, (255, 228, 196), (x+0, y+120, 15, 30))   # 右腿
    
    def _draw_attribute_editor(self):
        """绘制属性编辑区"""
        # 实时更新窗口大小
        self.screen_width = self.screen.get_width()
        self.screen_height = self.screen.get_height()
        # 保持与 game.py 的兼容性
        self.width = self.screen_width
        self.height = self.screen_height
        
        # 编辑框
        preview_width = min(400, self.screen_width // 2 - 40)
        editor_width = self.screen_width - preview_width - 60
        editor_rect = pygame.Rect(preview_width + 30, 30, editor_width, self.screen_height - 60)
        self._draw_wooden_box(editor_rect)
        
        # 标题
        self._draw_text("角色创建", preview_width + 30 + editor_width // 2, 60, font=self.large_font, color=self.COLOR_HIGHLIGHT)
        
        # 计算编辑区起始位置和元素间距
        editor_start_x = preview_width + 30
        
        # 计算可用高度和元素间距
        available_height = self.screen_height - 120  # 顶部60 + 底部60
        element_count = 8  # 姓名、性别、身高体重、生日、学院、发型、上衣、裤子
        base_spacing = 45  # 增加间距
        
        # 确保间距合适，避免重叠
        if available_height < element_count * base_spacing:
            spacing = available_height // element_count
        else:
            spacing = base_spacing
        
        # 姓名输入
        y_offset = 100
        self._draw_text("姓名:", editor_start_x + 30, y_offset, font=self.font)
        name_rect = pygame.Rect(editor_start_x + 90, y_offset - 10, min(200, editor_width - 100), 30)  # 减小框大小
        self._draw_input_box(name_rect, self.active_field == "name")
        display_name = self.name
        if self.active_field == "name" and self.cursor_visible:
            display_name += "|"
        self._draw_text(display_name, name_rect.x + 10, name_rect.centery, left=True, font=self.font)
        
        # 性别选择
        y_offset += spacing
        self._draw_text("性别:", editor_start_x + 30, y_offset, font=self.font)
        gender_rect = pygame.Rect(editor_start_x + 90, y_offset - 10, 150, 35)  # 减小框大小
        self._draw_input_box(gender_rect, self.active_field == "gender")
        self._draw_text(f"{self.gender}", gender_rect.centerx, gender_rect.centery, font=self.font)
        # 上下箭头
        if self.active_field == "gender":
            pygame.draw.polygon(self.screen, self.COLOR_TEXT, [(gender_rect.x + gender_rect.width - 30, y_offset - 10), (gender_rect.x + gender_rect.width - 20, y_offset - 20), (gender_rect.x + gender_rect.width - 10, y_offset - 10)])  # 上箭头
            pygame.draw.polygon(self.screen, self.COLOR_TEXT, [(gender_rect.x + gender_rect.width - 30, y_offset + 10), (gender_rect.x + gender_rect.width - 20, y_offset + 20), (gender_rect.x + gender_rect.width - 10, y_offset + 10)])  # 下箭头
        
        # 身高/体重
        y_offset += spacing
        self._draw_text("身高:", editor_start_x + 30, y_offset, font=self.font)
        height_rect = pygame.Rect(editor_start_x + 90, y_offset - 10, 70, 30)  # 减小框大小
        self._draw_input_box(height_rect, self.active_field == "height")
        self._draw_text(f"{self.character_height} cm", height_rect.x + 10, height_rect.centery, left=True, font=self.font)
        
        self._draw_text("体重:", editor_start_x + 190, y_offset, font=self.font)  # 调整位置，再靠右一点
        weight_rect = pygame.Rect(editor_start_x + 240, y_offset - 10, 70, 30)  # 减小框大小，再靠右一点
        self._draw_input_box(weight_rect, self.active_field == "weight")
        self._draw_text(f"{self.weight} kg", weight_rect.x + 10, weight_rect.centery, left=True, font=self.font)
        
        # 生日
        y_offset += spacing
        self._draw_text("生日:", editor_start_x + 30, y_offset, font=self.font)
        month_rect = pygame.Rect(editor_start_x + 90, y_offset - 10, 50, 30)  # 减小框大小
        day_rect = pygame.Rect(editor_start_x + 150, y_offset - 10, 50, 30)  # 减小框大小
        self._draw_input_box(month_rect, self.active_field == "birthday_month")
        self._draw_input_box(day_rect, self.active_field == "birthday_day")
        self._draw_text(f"{self.birth_month:02d}", month_rect.x + 10, month_rect.centery, left=True, font=self.font)
        self._draw_text("-", month_rect.x + month_rect.width + 5, y_offset, font=self.font)
        self._draw_text(f"{self.birth_day:02d}", day_rect.x + 10, day_rect.centery, left=True, font=self.font)
        
        # 学院
        y_offset += spacing
        self._draw_text("学院:", editor_start_x + 30, y_offset, font=self.font)
        college_rect = pygame.Rect(editor_start_x + 90, y_offset - 10, min(180, editor_width - 100), 30)  # 减小框大小
        self._draw_input_box(college_rect, self.active_field == "college")
        self._draw_text(self.college_list[self.college_index], college_rect.x + 10, college_rect.centery, left=True, font=self.font)
        # 下拉箭头
        pygame.draw.polygon(self.screen, self.COLOR_TEXT, [(college_rect.x + college_rect.width - 20, y_offset - 5), (college_rect.x + college_rect.width - 10, y_offset + 5), (college_rect.x + college_rect.width - 30, y_offset + 5)])
        
        # 发型
        y_offset += spacing
        self._draw_text("发型:", editor_start_x + 30, y_offset, font=self.font)
        hair_rect = pygame.Rect(editor_start_x + 90, y_offset - 10, 70, 30)  # 减小框大小
        self._draw_input_box(hair_rect, self.active_field == "hair")
        self._draw_text(f"{self.HAIR_STYLES[self.hair_style]}", hair_rect.x + 10, hair_rect.centery, left=True, font=self.font)
        
        # 发型颜色
        self._draw_text("颜色:", editor_start_x + 190, y_offset, font=self.font)  # 调整位置，再靠右一点
        hair_color_rect = pygame.Rect(editor_start_x + 240, y_offset - 10, 70, 30)  # 减小框大小，再靠右一点
        self._draw_input_box(hair_color_rect, self.active_field == "hair_color")
        # 颜色预览
        pygame.draw.rect(self.screen, self.COLOR_SCHEMES[self.hair_color], (hair_color_rect.x + 10, hair_color_rect.centery - 7, 50, 15))  # 减小颜色预览大小，垂直居中
        
        # 上衣
        y_offset += spacing
        self._draw_text("上衣:", editor_start_x + 30, y_offset, font=self.font)
        top_rect = pygame.Rect(editor_start_x + 90, y_offset - 10, 70, 30)  # 减小框大小
        self._draw_input_box(top_rect, self.active_field == "top")
        self._draw_text(f"{self.TOP_STYLES[self.top_style]}", top_rect.x + 10, top_rect.centery, left=True, font=self.font)
        
        # 上衣颜色
        self._draw_text("颜色:", editor_start_x + 190, y_offset, font=self.font)  # 调整位置，再靠右一点
        top_color_rect = pygame.Rect(editor_start_x + 240, y_offset - 10, 70, 30)  # 减小框大小，再靠右一点
        self._draw_input_box(top_color_rect, self.active_field == "top_color")
        # 颜色预览
        pygame.draw.rect(self.screen, self.COLOR_SCHEMES[self.top_color], (top_color_rect.x + 10, top_color_rect.centery - 7, 50, 15))  # 减小颜色预览大小，垂直居中
        
        # 裤子
        y_offset += spacing
        self._draw_text("裤子:", editor_start_x + 30, y_offset, font=self.font)
        pants_rect = pygame.Rect(editor_start_x + 90, y_offset - 10, 70, 30)  # 减小框大小
        self._draw_input_box(pants_rect, self.active_field == "pants")
        self._draw_text(f"{self.PANTS_STYLES[self.pants_style]}", pants_rect.x + 10, pants_rect.centery, left=True, font=self.font)
        
        # 裤子颜色
        self._draw_text("颜色:", editor_start_x + 190, y_offset, font=self.font)  # 调整位置，再靠右一点
        pants_color_rect = pygame.Rect(editor_start_x + 240, y_offset - 10, 70, 30)  # 减小框大小，再靠右一点
        self._draw_input_box(pants_color_rect, self.active_field == "pants_color")
        # 颜色预览
        pygame.draw.rect(self.screen, self.COLOR_SCHEMES[self.pants_color], (pants_color_rect.x + 10, pants_color_rect.centery - 7, 50, 15))  # 减小颜色预览大小，垂直居中
        
        # 学院下拉框 - 绘制在最上层
        if self.college_dropdown_open:
            # 绘制下拉框背景，覆盖其他元素
            dropdown_y = 100 + spacing * 4 - 10 + 35  # 学院字段的位置
            dropdown_height = len(self.college_list) * 30
            pygame.draw.rect(self.screen, self.COLOR_BG, (editor_start_x + 88, dropdown_y, min(184, editor_width - 96), dropdown_height + 4))
            pygame.draw.rect(self.screen, self.COLOR_WOOD, (editor_start_x + 88, dropdown_y, min(184, editor_width - 96), dropdown_height + 4), 2)
            
            for i, college in enumerate(self.college_list):
                option_rect = pygame.Rect(editor_start_x + 90, dropdown_y + 2 + i * 30, min(180, editor_width - 100), 30)
                if i == self.college_index:
                    pygame.draw.rect(self.screen, self.COLOR_ACTIVE, option_rect, 2)
                else:
                    pygame.draw.rect(self.screen, self.COLOR_WOOD, option_rect, 1)
                pygame.draw.rect(self.screen, self.COLOR_INPUT_BG, option_rect.inflate(-2, -2))
                self._draw_text(college, option_rect.x + 10, dropdown_y + 17 + i * 30, left=True, font=self.font)
    
    def _draw_confirm_button(self):
        """绘制确认按钮"""
        # 实时更新窗口大小
        self.screen_width = self.screen.get_width()
        self.screen_height = self.screen.get_height()
        # 保持与 game.py 的兼容性
        self.width = self.screen_width
        self.height = self.screen_height
        
        confirm_rect = pygame.Rect(self.screen_width - 130, self.screen_height - 70, 100, 40)
        self._draw_button(confirm_rect, "确认", False, True)
    
    def _draw_wooden_box(self, rect):
        """绘制木质盒子"""
        # 外边框
        pygame.draw.rect(self.screen, self.COLOR_WOOD_DARK, rect, 3)
        # 内边框
        pygame.draw.rect(self.screen, self.COLOR_WOOD, rect.inflate(-2, -2), 2)
        # 内填充
        pygame.draw.rect(self.screen, self.COLOR_BG, rect.inflate(-4, -4))
    
    def _draw_input_box(self, rect, active):
        """绘制输入框"""
        # 外边框
        if active:
            pygame.draw.rect(self.screen, self.COLOR_ACTIVE, rect, 2)
        else:
            pygame.draw.rect(self.screen, self.COLOR_WOOD, rect, 2)
        # 内填充
        pygame.draw.rect(self.screen, self.COLOR_INPUT_BG, rect.inflate(-4, -4))
    
    def _draw_button(self, rect, text, active, is_confirm=False):
        """绘制按钮"""
        # 外边框
        if active or is_confirm:
            pygame.draw.rect(self.screen, self.COLOR_ACTIVE, rect, 2)
        else:
            pygame.draw.rect(self.screen, self.COLOR_WOOD, rect, 2)
        # 内填充
        if is_confirm:
            pygame.draw.rect(self.screen, self.COLOR_HIGHLIGHT, rect.inflate(-4, -4))
            text_color = self.COLOR_BG
        else:
            pygame.draw.rect(self.screen, self.COLOR_INPUT_BG, rect.inflate(-4, -4))
            text_color = self.COLOR_TEXT
        # 文字
        self._draw_text(text, rect.centerx, rect.centery, color=text_color, font=self.font)
    
    def _draw_text(self, text, x, y, color=None, left=False, font=None):
        """绘制文字"""
        if color is None:
            color = self.COLOR_TEXT
        if font is None:
            font = self.font
        surface = font.render(text, True, color)
        if left:
            rect = surface.get_rect(topleft=(x, y - surface.get_height() // 2))
        else:
            rect = surface.get_rect(center=(x, y))
        self.screen.blit(surface, rect)
