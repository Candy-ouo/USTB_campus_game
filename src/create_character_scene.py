
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
        self.character_height = ""
        self.weight = ""
        self.birth_month = 1
        self.birth_day = 1
        self.college_index = 0
        self.college_list = list(COLLEGE_MAJORS.keys())
        self.major = Character.get_major_by_college(self.college_list[self.college_index])
        
        # 激活的输入框/选项
        self.active_field = "name"  # name, gender, height, weight, birthday_month, birthday_day, college
        
        # 光标闪烁
        self.cursor_visible = True
        self.cursor_timer = 0
        self.cursor_interval = 500  # 毫秒
        
        # 字段顺序，用于方向键导航
        self.fields = ["name", "gender", "height", "weight", "birthday_month", "birthday_day", "college"]
        self.current_field_index = 0
        
        # 下拉框状态
        self.college_dropdown_open = False
        
        # 加载图片素材
        import os
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        self.input_default = pygame.image.load(os.path.join(base_dir, "image", "input_default.png"))
        self.input_focus = pygame.image.load(os.path.join(base_dir, "image", "input_focus.png"))
        self.dropdown_arrow = pygame.image.load(os.path.join(base_dir, "image", "dropdown_arrow.png"))
        self.btn_ok = pygame.image.load(os.path.join(base_dir, "image", "btn_ok.png"))
    
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
                elif event.key == pygame.K_BACKSPACE:
                    if self.active_field == "name":
                        self.name = self.name[:-1]
                    elif self.active_field == "height":
                        # 退格删除最后一位数字
                        if isinstance(self.character_height, str):
                            self.character_height = self.character_height[:-1]
                        else:
                            height_str = str(self.character_height)
                            if len(height_str) > 1:
                                self.character_height = height_str[:-1]
                            else:
                                self.character_height = ""
                    elif self.active_field == "weight":
                        # 退格删除最后一位数字
                        if isinstance(self.weight, str):
                            self.weight = self.weight[:-1]
                        else:
                            weight_str = str(self.weight)
                            if len(weight_str) > 1:
                                self.weight = weight_str[:-1]
                            else:
                                self.weight = ""
                
                # 文本输入（处理中文）
                elif event.unicode:
                    if self.active_field == "name":
                        if len(self.name) < 10:
                            # 直接添加 unicode 字符，包括中文
                            self.name += event.unicode
                    elif self.active_field == "height" and event.unicode.isdigit():
                        # 只允许输入数字，类似于姓名的输入模式
                        if isinstance(self.character_height, str):
                            self.character_height += event.unicode
                        else:
                            self.character_height = str(self.character_height) + event.unicode
                    elif self.active_field == "weight" and event.unicode.isdigit():
                        # 只允许输入数字，类似于姓名的输入模式
                        if isinstance(self.weight, str):
                            self.weight += event.unicode
                        else:
                            self.weight = str(self.weight) + event.unicode
            
            # 文本输入事件（处理中文输入）
            elif event.type == pygame.TEXTINPUT:
                if self.active_field == "name":
                    if len(self.name) < 10:
                        # 直接添加文本，包括中文
                        self.name += event.text
                elif self.active_field == "height" and event.text.isdigit():
                    # 只允许输入数字，类似于姓名的输入模式
                    if isinstance(self.character_height, str):
                        self.character_height += event.text
                    else:
                        self.character_height = str(self.character_height) + event.text
                elif self.active_field == "weight" and event.text.isdigit():
                    # 只允许输入数字，类似于姓名的输入模式
                    if isinstance(self.weight, str):
                        self.weight += event.text
                    else:
                        self.weight = str(self.weight) + event.text
            
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
                self.major = Character.get_major_by_college(self.college_list[self.college_index])
            elif key == pygame.K_DOWN and self.college_index < len(self.college_list) - 1:
                self.college_index += 1
                self.major = Character.get_major_by_college(self.college_list[self.college_index])
    
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
        element_count = 5  # 姓名、性别、身高体重、生日、学院
        base_spacing = 60  # 增加间距
        
        # 确保间距合适，避免重叠
        if available_height < element_count * base_spacing:
            spacing = available_height // element_count
        else:
            spacing = base_spacing
        
        # 左对齐起始位置，离中间竖线有一定距离
        left_align_x = editor_start_x + 50
        label_width = 50
        
        # 姓名输入框
        y_offset = 100
        input_x = left_align_x + label_width
        name_rect = pygame.Rect(input_x, y_offset - 10, 200, 30)  # 减小框大小
        if name_rect.collidepoint(pos):
            self.active_field = "name"
            self.current_field_index = self.fields.index("name")
            self.college_dropdown_open = False
        
        # 性别选择 - 单选按钮组
        y_offset += spacing
        input_x = left_align_x + label_width
        button_size = 40
        button_spacing = 10
        # 向右移动20像素，与绘制位置一致
        male_button_rect = pygame.Rect(input_x + 20, y_offset - 15, button_size, button_size)
        female_button_rect = pygame.Rect(input_x + 20 + button_size + button_spacing, y_offset - 15, button_size, button_size)
        
        if male_button_rect.collidepoint(pos):
            self.gender = "男"
            self.college_dropdown_open = False
        elif female_button_rect.collidepoint(pos):
            self.gender = "女"
            self.college_dropdown_open = False
        
        # 身高/体重
        y_offset += spacing
        small_input_width = 80
        input_height = 84
        gap = 30
        label_x = left_align_x
        move_right = 20  # 向右移动的像素数
        
        height_rect = pygame.Rect(label_x + label_width + move_right, y_offset - input_height // 2, small_input_width, input_height)
        if height_rect.collidepoint(pos):
            self.active_field = "height"
            self.current_field_index = self.fields.index("height")
            # 清空现有值，让用户直接输入
            self.character_height = ""
            self.college_dropdown_open = False
        
        weight_rect = pygame.Rect(label_x + label_width * 2 + small_input_width + gap + 50 + move_right, y_offset - input_height // 2, small_input_width, input_height)
        if weight_rect.collidepoint(pos):
            self.active_field = "weight"
            self.current_field_index = self.fields.index("weight")
            # 清空现有值，让用户直接输入
            self.weight = ""
            self.college_dropdown_open = False
        
        # 生日
        y_offset += spacing
        small_input_width = 80
        input_height = 84
        gap = 10
        label_x = left_align_x
        
        month_rect = pygame.Rect(label_x + label_width + move_right, y_offset - input_height // 2, small_input_width, input_height)
        day_rect = pygame.Rect(label_x + label_width + small_input_width + gap + move_right, y_offset - input_height // 2, small_input_width, input_height)
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
        input_width = 200  # 与绘制时的宽度一致
        input_height = 84
        label_x = left_align_x
        input_x = label_x + label_width
        college_rect = pygame.Rect(input_x, y_offset - input_height // 2, input_width, input_height)
        if college_rect.collidepoint(pos):
            self.active_field = "college"
            self.current_field_index = self.fields.index("college")
            self.college_dropdown_open = not self.college_dropdown_open
        
        # 学院下拉框选项
        if self.college_dropdown_open:
            dropdown_y = y_offset + input_height // 2 + 2  # 学院字段的位置
            option_height = 50  # 减小选项高度
            dropdown_width = input_width - 20  # 减小下拉框宽度
            dropdown_x = input_x + 10  # 居中对齐
            for i, college in enumerate(self.college_list):
                option_rect = pygame.Rect(dropdown_x, dropdown_y + 2 + i * option_height, dropdown_width, option_height)
                if option_rect.collidepoint(pos):
                    self.college_index = i
                    self.major = Character.get_major_by_college(self.college_list[self.college_index])
                    self.college_dropdown_open = False
        
        # 确认按钮 - 使用draw方法中保存的按钮矩形
        if hasattr(self, 'confirm_rect') and self.confirm_rect.collidepoint(pos):
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
        
        # 处理身高体重为空的情况
        height = self.character_height
        if not height:
            height = 170
        else:
            try:
                height = int(height)
            except ValueError:
                height = 170
        
        weight = self.weight
        if not weight:
            weight = 60
        else:
            try:
                weight = int(weight)
            except ValueError:
                weight = 60
        
        character = Character(
            name=self.name,
            gender=self.gender,
            height=height,
            weight=weight,
            birthday=birthday,
            college=college,
            major=self.major
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
        print("\n主属性:")
        print(f"学识: LV{character.knowledge // 25} {character.knowledge % 100}/100")
        print(f"魅力: LV{character.charm // 25} {character.charm % 100}/100")
        print(f"体能: LV{character.energy // 25} {character.energy % 100}/100")
        print("\n行动属性:")
        print(f"生活费: {character.money} 元")
        print(f"行动力: {character.action_points} 点")
        print(f"心情: {character.mood}/100")
        print("\n副属性:")
        print(f"技能: {character.skill}")
        print(f"人脉: {character.social_network}")
        print(f"声望: {character.reputation}")
        print("\n学习属性:")
        print(f"理论实验: {character.theory_experiment}")
        print(f"就业创业: {character.employment_entrepreneurship}")
        print(f"美育素养: {character.aesthetic_literacy}")
        
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
        # 绘制确认按钮并保存按钮矩形
        self.confirm_rect = self._draw_confirm_button()
    
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
        
        # 加载角色立绘
        try:
            # 使用绝对路径加载图片
            import os
            base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            if self.gender == "男":
                character_image = pygame.image.load(os.path.join(base_dir, "image", "boy.png"))
            else:
                character_image = pygame.image.load(os.path.join(base_dir, "image", "girl.png"))
            
            # 调整立绘大小，保持比例
            max_height = min(250, (self.screen_height - 250))
            scale_factor = max_height / character_image.get_height()
            new_width = int(character_image.get_width() * scale_factor)
            character_image = pygame.transform.scale(character_image, (new_width, max_height))
            
            # 计算立绘位置（居中）
            character_x = 30 + (preview_width - new_width) // 2
            character_y = 100
            
            # 绘制木质相框
            frame_thickness = 10
            frame_rect = pygame.Rect(character_x - frame_thickness, character_y - frame_thickness, 
                                   new_width + frame_thickness * 2, max_height + frame_thickness * 2)
            # 相框外边框 - 深棕色
            pygame.draw.rect(self.screen, (101, 67, 33), frame_rect, frame_thickness)
            # 相框内边框 - 浅棕色
            pygame.draw.rect(self.screen, (160, 82, 45), frame_rect.inflate(-frame_thickness, -frame_thickness), frame_thickness // 2)
            
            # 绘制立绘
            self.screen.blit(character_image, (character_x, character_y))
            
            # 角色信息
            info_y = character_y + max_height + 50  # 增加图片和姓名之间的间隔，离图片更远
            
            # 信息文本 - 直接显示，无白色框
            self._draw_text(f"姓名: {self.name}", 30 + preview_width // 2, info_y, font=self.font)
            self._draw_text(f"性别: {self.gender}", 30 + preview_width // 2, info_y + 40, font=self.font)  # 增加行间距
            self._draw_text(f"学院: {self.college_list[self.college_index]}", 30 + preview_width // 2, info_y + 80, font=self.font)  # 增加行间距
            self._draw_text(f"专业: {self.major}", 30 + preview_width // 2, info_y + 120, font=self.font)  # 增加行间距
        except Exception as e:
            # 如果图片加载失败，显示错误信息
            self._draw_text("立绘加载失败", 30 + preview_width // 2, 200, font=self.font, color=(255, 0, 0))
            print(f"立绘加载失败: {e}")
    
    def _draw_pixel_character(self, x, y, hair_color, top_color, pants_color):
        """绘制像素风格角色"""
        # 头部
        pygame.draw.rect(self.screen, (255, 228, 196), (x-20, y, 40, 40))  # 头部
        
        # 发型 - 默认短发
        pygame.draw.rect(self.screen, hair_color, (x-25, y-5, 50, 25))
        
        # 眼睛
        pygame.draw.rect(self.screen, (0, 0, 0), (x-10, y+15, 8, 8))
        pygame.draw.rect(self.screen, (0, 0, 0), (x+2, y+15, 8, 8))
        
        # 身体（上衣）- 默认T恤
        pygame.draw.rect(self.screen, top_color, (x-25, y+40, 50, 40))
        
        # 裤子 - 默认牛仔裤
        pygame.draw.rect(self.screen, pants_color, (x-20, y+80, 40, 40))
        
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
        
        # 计算编辑区起始位置
        editor_start_x = preview_width + 30
        # 左对齐起始位置，离中间竖线有一定距离
        left_align_x = editor_start_x + 50  # 增加距离，离中间竖线更远
        
        # 计算可用高度和元素间距
        available_height = self.screen_height - 120  # 顶部60 + 底部60
        element_count = 5  # 姓名、性别、身高体重、生日、学院
        base_spacing = 60  # 增加间距
        
        # 确保间距合适，避免重叠
        if available_height < element_count * base_spacing:
            spacing = available_height // element_count
        else:
            spacing = base_spacing
        
        # 姓名输入 - 左对齐
        y_offset = 100
        label_width = 50
        input_width = 260
        input_height = 84
        label_x = left_align_x
        input_x = label_x + label_width
        self._draw_text("姓名:", label_x, y_offset, font=self.font, left=True)
        name_rect = pygame.Rect(input_x, y_offset - input_height // 2, input_width, input_height)  # 调整框大小
        self._draw_input_box(name_rect, self.active_field == "name")
        display_name = self.name
        if self.active_field == "name" and self.cursor_visible:
            display_name += "|"
        # 文字水平和垂直居中
        text_surface = self.font.render(display_name, True, self.COLOR_TEXT)
        text_width = text_surface.get_width()
        text_height = text_surface.get_height()
        text_x = name_rect.x + (name_rect.width - text_width) // 2
        text_y = name_rect.y + (name_rect.height - text_height) // 2
        self.screen.blit(text_surface, (text_x, text_y))
        
        # 性别选择 - 左对齐，使用像素图标单选按钮组
        y_offset += spacing
        label_x = left_align_x
        input_x = label_x + label_width
        self._draw_text("性别:", label_x, y_offset, font=self.font, left=True)
        
        # 性别单选按钮组 - 星露谷物语风格
        button_size = 40
        button_spacing = 10  # 紧密排列
        # 向右移动20像素
        male_button_rect = pygame.Rect(input_x + 20, y_offset - 15, button_size, button_size)
        female_button_rect = pygame.Rect(input_x + 20 + button_size + button_spacing, y_offset - 15, button_size, button_size)
        
        # 鼠标位置
        mouse_pos = pygame.mouse.get_pos()
        
        # 加载像素图标
        import os
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        male_icon_path = os.path.join(base_dir, "image", "男性-pixelized.png")
        female_icon_path = os.path.join(base_dir, "image", "女性-pixelized .png")
        
        try:
            male_icon = pygame.image.load(male_icon_path)
            female_icon = pygame.image.load(female_icon_path)
            # 缩放图标到合适大小
            male_icon = pygame.transform.scale(male_icon, (button_size, button_size))
            female_icon = pygame.transform.scale(female_icon, (button_size, button_size))
        except pygame.error:
            # 如果图片加载失败，使用默认符号
            male_icon = None
            female_icon = None
        
        # 绘制男性图标按钮
        if male_button_rect.collidepoint(mouse_pos):
            # 鼠标悬停效果
            pygame.draw.rect(self.screen, (255, 215, 0), male_button_rect, 3)
        if self.gender == "男":
            # 选中状态
            pygame.draw.rect(self.screen, (255, 215, 0), male_button_rect, 3)
            pygame.draw.rect(self.screen, (255, 215, 0), male_button_rect.inflate(-4, -4), 1)
            # 选中时轻微放大
            if male_icon:
                scaled_male_icon = pygame.transform.scale(male_icon, (int(button_size * 1.1), int(button_size * 1.1)))
                icon_rect = scaled_male_icon.get_rect(center=male_button_rect.center)
                self.screen.blit(scaled_male_icon, icon_rect)
            else:
                # 绘制默认男性符号
                pygame.draw.polygon(self.screen, (0, 0, 255), [(male_button_rect.centerx, male_button_rect.y + 5), 
                                                             (male_button_rect.x + 5, male_button_rect.bottom - 5), 
                                                             (male_button_rect.x + 15, male_button_rect.bottom - 5), 
                                                             (male_button_rect.x + 15, male_button_rect.centerx + 5), 
                                                             (male_button_rect.x + 25, male_button_rect.centerx + 5), 
                                                             (male_button_rect.x + 25, male_button_rect.bottom - 5), 
                                                             (male_button_rect.right - 5, male_button_rect.bottom - 5), 
                                                             (male_button_rect.centerx, male_button_rect.y + 5)])
        else:
            # 未选中状态
            if male_icon:
                self.screen.blit(male_icon, male_button_rect)
            else:
                # 绘制默认男性符号
                pygame.draw.polygon(self.screen, (0, 0, 150), [(male_button_rect.centerx, male_button_rect.y + 5), 
                                                             (male_button_rect.x + 5, male_button_rect.bottom - 5), 
                                                             (male_button_rect.x + 15, male_button_rect.bottom - 5), 
                                                             (male_button_rect.x + 15, male_button_rect.centerx + 5), 
                                                             (male_button_rect.x + 25, male_button_rect.centerx + 5), 
                                                             (male_button_rect.x + 25, male_button_rect.bottom - 5), 
                                                             (male_button_rect.right - 5, male_button_rect.bottom - 5), 
                                                             (male_button_rect.centerx, male_button_rect.y + 5)])
        
        # 绘制女性图标按钮
        if female_button_rect.collidepoint(mouse_pos):
            # 鼠标悬停效果
            pygame.draw.rect(self.screen, (255, 215, 0), female_button_rect, 3)
        if self.gender == "女":
            # 选中状态
            pygame.draw.rect(self.screen, (255, 215, 0), female_button_rect, 3)
            pygame.draw.rect(self.screen, (255, 215, 0), female_button_rect.inflate(-4, -4), 1)
            # 选中时轻微放大
            if female_icon:
                scaled_female_icon = pygame.transform.scale(female_icon, (int(button_size * 1.1), int(button_size * 1.1)))
                icon_rect = scaled_female_icon.get_rect(center=female_button_rect.center)
                self.screen.blit(scaled_female_icon, icon_rect)
            else:
                # 绘制默认女性符号
                pygame.draw.circle(self.screen, (255, 0, 100), (female_button_rect.centerx, female_button_rect.centery - 5), 10)
                pygame.draw.rect(self.screen, (255, 0, 100), (female_button_rect.centerx - 2, female_button_rect.centery + 5, 4, 15))
                pygame.draw.polygon(self.screen, (255, 0, 100), [(female_button_rect.centerx - 8, female_button_rect.centery + 10), 
                                                               (female_button_rect.centerx + 8, female_button_rect.centery + 10), 
                                                               (female_button_rect.centerx, female_button_rect.centery + 20)])
        else:
            # 未选中状态
            if female_icon:
                self.screen.blit(female_icon, female_button_rect)
            else:
                # 绘制默认女性符号
                pygame.draw.circle(self.screen, (150, 0, 50), (female_button_rect.centerx, female_button_rect.centery - 5), 10)
                pygame.draw.rect(self.screen, (150, 0, 50), (female_button_rect.centerx - 2, female_button_rect.centery + 5, 4, 15))
                pygame.draw.polygon(self.screen, (150, 0, 50), [(female_button_rect.centerx - 8, female_button_rect.centery + 10), 
                                                               (female_button_rect.centerx + 8, female_button_rect.centery + 10), 
                                                               (female_button_rect.centerx, female_button_rect.centery + 20)])
        
        # 身高/体重 - 左对齐
        y_offset += spacing
        small_input_width = 80
        input_height = 84
        gap = 30
        label_x = left_align_x
        
        self._draw_text("身高:", label_x, y_offset, font=self.font, left=True)
        height_rect = pygame.Rect(label_x + label_width + 20, y_offset - input_height // 2, small_input_width, input_height)  # 调整框大小，向右移动20像素
        self._draw_input_box(height_rect, self.active_field == "height")
        # 文字水平和垂直居中 - 仅显示数字
        height_text = str(self.character_height) if self.character_height else ""
        text_surface = self.font.render(height_text, True, self.COLOR_TEXT)
        text_width = text_surface.get_width()
        text_height = text_surface.get_height()
        text_x = height_rect.x + (height_rect.width - text_width) // 2
        text_y = height_rect.y + (height_rect.height - text_height) // 2
        self.screen.blit(text_surface, (text_x, text_y))
        # 显示单位 cm
        unit_text = "cm"
        unit_surface = self.font.render(unit_text, True, self.COLOR_TEXT)
        unit_x = height_rect.x + height_rect.width + 5  # 5px间距，离输入框更近
        unit_y = y_offset
        self.screen.blit(unit_surface, (unit_x, unit_y - unit_surface.get_height() // 2))
        
        self._draw_text("体重:", label_x + label_width + small_input_width + gap + 50, y_offset, font=self.font, left=True)  # 调整位置，再靠右一点，离cm更远
        weight_rect = pygame.Rect(label_x + label_width * 2 + small_input_width + gap + 50 + 20, y_offset - input_height // 2, small_input_width, input_height)  # 调整框大小，再靠右一点，向右移动20像素
        self._draw_input_box(weight_rect, self.active_field == "weight")
        # 文字水平和垂直居中 - 仅显示数字
        weight_text = str(self.weight) if self.weight else ""
        text_surface = self.font.render(weight_text, True, self.COLOR_TEXT)
        text_width = text_surface.get_width()
        text_height = text_surface.get_height()
        text_x = weight_rect.x + (weight_rect.width - text_width) // 2
        text_y = weight_rect.y + (weight_rect.height - text_height) // 2
        self.screen.blit(text_surface, (text_x, text_y))
        # 显示单位 kg
        unit_text = "kg"
        unit_surface = self.font.render(unit_text, True, self.COLOR_TEXT)
        unit_x = weight_rect.x + weight_rect.width + 5  # 5px间距，离输入框更近
        unit_y = y_offset
        self.screen.blit(unit_surface, (unit_x, unit_y - unit_surface.get_height() // 2))
        
        # 生日 - 左对齐
        y_offset += spacing
        small_input_width = 80
        input_height = 84
        gap = 10
        label_x = left_align_x
        
        self._draw_text("生日:", label_x, y_offset, font=self.font, left=True)
        month_rect = pygame.Rect(label_x + label_width + 20, y_offset - input_height // 2, small_input_width, input_height)  # 调整框大小，向右移动20像素
        day_rect = pygame.Rect(label_x + label_width + small_input_width + gap + 20, y_offset - input_height // 2, small_input_width, input_height)  # 调整框大小，向右移动20像素
        self._draw_input_box(month_rect, self.active_field == "birthday_month")
        self._draw_input_box(day_rect, self.active_field == "birthday_day")
        # 月份文字水平和垂直居中
        month_text = f"{self.birth_month:02d}"
        text_surface = self.font.render(month_text, True, self.COLOR_TEXT)
        text_width = text_surface.get_width()
        text_height = text_surface.get_height()
        text_x = month_rect.x + (month_rect.width - text_width) // 2
        text_y = month_rect.y + (month_rect.height - text_height) // 2
        self.screen.blit(text_surface, (text_x, text_y))
        
        # 绘制连接符
        self._draw_text("-", month_rect.x + month_rect.width + 5, y_offset, font=self.font)
        
        # 日期文字水平和垂直居中
        day_text = f"{self.birth_day:02d}"
        text_surface = self.font.render(day_text, True, self.COLOR_TEXT)
        text_width = text_surface.get_width()
        text_height = text_surface.get_height()
        text_x = day_rect.x + (day_rect.width - text_width) // 2
        text_y = day_rect.y + (day_rect.height - text_height) // 2
        self.screen.blit(text_surface, (text_x, text_y))
        
        # 学院 - 左对齐
        y_offset += spacing
        input_width = 200  # 减小下拉框宽度
        input_height = 84
        label_x = left_align_x
        input_x = label_x + label_width
        self._draw_text("学院:", label_x, y_offset, font=self.font, left=True)
        college_rect = pygame.Rect(input_x, y_offset - input_height // 2, input_width, input_height)  # 调整框大小
        self._draw_input_box(college_rect, self.active_field == "college")
        # 文字水平和垂直居中
        college_text = self.college_list[self.college_index]
        text_surface = self.font.render(college_text, True, self.COLOR_TEXT)
        text_width = text_surface.get_width()
        text_height = text_surface.get_height()
        text_x = college_rect.x + (college_rect.width - text_width) // 2
        text_y = college_rect.y + (college_rect.height - text_height) // 2
        self.screen.blit(text_surface, (text_x, text_y))
        # 下拉箭头 - 使用图片素材，增大箭头大小
        arrow_size = 35  # 增大箭头大小
        arrow_rect = pygame.Rect(college_rect.x + college_rect.width - arrow_size - 5, y_offset - arrow_size // 2, arrow_size, arrow_size)
        scaled_arrow = pygame.transform.scale(self.dropdown_arrow, (arrow_rect.width, arrow_rect.height))
        self.screen.blit(scaled_arrow, arrow_rect)
        
        # 学院下拉框 - 绘制在最上层
        if self.college_dropdown_open:
            # 绘制下拉框背景，覆盖其他元素 - 星露谷物语风格
            dropdown_y = y_offset + input_height // 2 + 2  # 学院字段的位置
            option_height = 50  # 减小选项高度
            dropdown_height = len(self.college_list) * option_height
            dropdown_width = input_width - 20  # 减小下拉框宽度
            dropdown_x = input_x + 10  # 居中对齐
            
            # 外边框 - 深棕色
            pygame.draw.rect(self.screen, (101, 67, 33), (dropdown_x, dropdown_y, dropdown_width, dropdown_height), 2)
            # 内边框 - 浅棕色
            pygame.draw.rect(self.screen, (160, 82, 45), (dropdown_x + 1, dropdown_y + 1, dropdown_width - 2, dropdown_height - 2), 1)
            # 内填充 - 暖米色
            pygame.draw.rect(self.screen, (255, 248, 220), (dropdown_x + 2, dropdown_y + 2, dropdown_width - 4, dropdown_height - 4))
            
            for i, college in enumerate(self.college_list):
                option_rect = pygame.Rect(dropdown_x + 2, dropdown_y + 2 + i * option_height, dropdown_width - 4, option_height - 4)
                if i == self.college_index:
                    # 选中项 - 高亮边框
                    pygame.draw.rect(self.screen, (255, 215, 0), option_rect, 2)
                    pygame.draw.rect(self.screen, (255, 182, 193), option_rect.inflate(-2, -2), 1)
                # 绘制选项文字 - 水平和垂直居中
                text_surface = self.font.render(college, True, self.COLOR_TEXT)
                text_width = text_surface.get_width()
                text_height = text_surface.get_height()
                text_x = option_rect.x + (option_rect.width - text_width) // 2
                text_y = option_rect.y + (option_rect.height - text_height) // 2
                self.screen.blit(text_surface, (text_x, text_y))
    
    def _draw_confirm_button(self):
        """绘制确认按钮"""
        # 实时更新窗口大小
        self.screen_width = self.screen.get_width()
        self.screen_height = self.screen.get_height()
        # 保持与 game.py 的兼容性
        self.width = self.screen_width
        self.height = self.screen_height
        
        # 增大确认按钮大小
        button_width = 200
        button_height = 150
        confirm_rect = pygame.Rect(self.screen_width - button_width - 40, self.screen_height - button_height - 40, button_width, button_height)
            
        # 缩放确认图片
        scaled_btn = pygame.transform.scale(self.btn_ok, (button_width, button_height))
        self.screen.blit(scaled_btn, confirm_rect)
        
        return confirm_rect
    
    def _draw_wooden_box(self, rect):
        """绘制木质盒子"""
        # 外边框
        pygame.draw.rect(self.screen, self.COLOR_WOOD_DARK, rect, 3)
        # 内边框
        pygame.draw.rect(self.screen, self.COLOR_WOOD, rect.inflate(-2, -2), 2)
        # 内填充
        pygame.draw.rect(self.screen, self.COLOR_BG, rect.inflate(-4, -4))
    
    def _draw_input_box(self, rect, active):
        """绘制输入框 - 使用图片素材"""
        # 选择合适的图片
        if active:
            input_image = self.input_focus
        else:
            input_image = self.input_default
        
        # 缩放图片到输入框大小
        scaled_image = pygame.transform.scale(input_image, (rect.width, rect.height))
        # 绘制图片
        self.screen.blit(scaled_image, rect)
    

    
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
