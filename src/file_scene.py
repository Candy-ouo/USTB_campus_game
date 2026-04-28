import pygame
import os
import sys

class FileScene:
    def __init__(self, screen, game, previous_state):
        self.screen = screen
        self.game = game
        self.previous_state = previous_state
        self.width, self.height = screen.get_size()
        self.font = None
        self.large_font = None
        self.small_font = None
        self.boy_image = None
        self.girl_image = None
        self.back_button = pygame.Rect(50, 650, 100, 40)
        self._initialize_fonts()
        self._load_images()
    
    def _initialize_fonts(self):
        """初始化字体"""
        font_path = os.path.join(os.path.dirname(__file__), '..', 'fonts', 'msyh.ttf')
        start_font_path = os.path.join(os.path.dirname(__file__), '..', 'fonts', 'fonts_start.ttf')
        
        try:
            if os.path.exists(start_font_path):
                self.large_font = pygame.font.Font(start_font_path, 28)
                self.font = pygame.font.Font(start_font_path, 18)
                self.small_font = pygame.font.Font(start_font_path, 14)
            elif os.path.exists(font_path):
                self.large_font = pygame.font.Font(font_path, 28)
                self.font = pygame.font.Font(font_path, 18)
                self.small_font = pygame.font.Font(font_path, 14)
            else:
                self.large_font = pygame.font.SysFont('SimHei', 28)
                self.font = pygame.font.SysFont('SimHei', 18)
                self.small_font = pygame.font.SysFont('SimHei', 14)
        except:
            self.large_font = pygame.font.Font(None, 28)
            self.font = pygame.font.Font(None, 18)
            self.small_font = pygame.font.Font(None, 14)
    
    def _load_images(self):
        """加载头像图片"""
        boy_path = os.path.join(os.path.dirname(__file__), '..', 'image', 'boy.png')
        girl_path = os.path.join(os.path.dirname(__file__), '..', 'image', 'girl.png')
        
        try:
            if os.path.exists(boy_path):
                self.boy_image = pygame.image.load(boy_path)
                self.boy_image = pygame.transform.scale(self.boy_image, (120, 120))
            if os.path.exists(girl_path):
                self.girl_image = pygame.image.load(girl_path)
                self.girl_image = pygame.transform.scale(self.girl_image, (120, 120))
        except Exception as e:
            print(f"加载头像图片失败: {e}")
    
    def draw(self):
        """绘制档案界面"""
        # 绘制背景（羊皮纸效果）
        self.screen.fill((254, 247, 201))
        
        # 绘制边框
        border_color = (150, 100, 50)
        pygame.draw.rect(self.screen, border_color, (20, 20, self.width - 40, self.height - 40), 4)
        
        # 绘制标题
        title = self.large_font.render("角色档案", True, (100, 60, 30))
        title_rect = title.get_rect(center=(self.width // 2, 60))
        self.screen.blit(title, title_rect)
        
        # 绘制分割线
        pygame.draw.line(self.screen, border_color, (40, 100), (self.width - 40, 100), 2)
        
        # 绘制基础信息区
        self._draw_basic_info()
        
        # 绘制属性面板区
        self._draw_attributes()
        
        # 绘制学期结算与课程进度区
        self._draw_course_progress()
        
        # 绘制返回按钮
        pygame.draw.rect(self.screen, (220, 180, 140), self.back_button)
        pygame.draw.rect(self.screen, border_color, self.back_button, 2)
        back_text = self.font.render("返回", True, (100, 60, 30))
        back_rect = back_text.get_rect(center=self.back_button.center)
        self.screen.blit(back_text, back_rect)
    
    def _draw_basic_info(self):
        """绘制基础信息区"""
        border_color = (150, 100, 50)
        
        # 绘制基础信息标题
        info_title = self.font.render("基础信息", True, (100, 60, 30))
        self.screen.blit(info_title, (180, 120))
        
        # 绘制信息表格
        table_x = 180
        table_y = 160
        table_width = 500
        table_height = 200
        
        # 绘制表格边框
        pygame.draw.rect(self.screen, border_color, (table_x, table_y, table_width, table_height), 2)
        
        # 从Character类获取基础信息
        character = getattr(self.game, 'character', None)
        if character is None:
            character = getattr(self.game, 'player', None)
        
        info_items = [
            ("姓名", getattr(character, 'name', '未知')),
            ("性别", getattr(character, 'gender', '未知')),
            ("身高", f"{getattr(character, 'height', 0)} cm"),
            ("体重", f"{getattr(character, 'weight', 0)} kg"),
            ("生日", getattr(character, 'birthday', '未知')),
            ("学院", getattr(character, 'college', '未知')),
            ("专业", getattr(character, 'major', '未知'))
        ]
        
        for i, (label, value) in enumerate(info_items):
            label_text = self.font.render(label, True, (100, 60, 30))
            value_text = self.font.render(str(value), True, (100, 60, 30))
            self.screen.blit(label_text, (table_x + 20, table_y + 20 + i * 25))
            self.screen.blit(value_text, (table_x + 150, table_y + 20 + i * 25))
    
    def _draw_attributes(self):
        """绘制属性面板区"""
        border_color = (150, 100, 50)
        
        # 绘制属性标题
        attr_title = self.font.render("属性信息", True, (100, 60, 30))
        self.screen.blit(attr_title, (180, 380))
        
        # 绘制主属性
        main_attrs_x = 180
        main_attrs_y = 420
        
        # 学识
        knowledge, knowledge_level = self.game.player.get_knowledge()
        knowledge_text = self.font.render(f"学识 LV{knowledge_level} {knowledge}/100", True, (60, 172, 100))
        self.screen.blit(knowledge_text, (main_attrs_x, main_attrs_y))
        
        # 魅力
        charm, charm_level = self.game.player.get_charm()
        charm_text = self.font.render(f"魅力 LV{charm_level} {charm}/100", True, (252, 173, 72))
        self.screen.blit(charm_text, (main_attrs_x, main_attrs_y + 30))
        
        # 体能
        physical, physical_level = self.game.player.get_physical()
        physical_text = self.font.render(f"体能 LV{physical_level} {physical}/100", True, (186, 50, 50))
        self.screen.blit(physical_text, (main_attrs_x, main_attrs_y + 60))
        
        # 绘制副属性
        secondary_attrs_x = 400
        secondary_attrs_y = 420
        
        skill = self.game.player.get_skill()
        social = self.game.player.get_social()
        reputation = self.game.player.get_reputation()
        
        skill_text = self.font.render(f"技能: {skill}", True, (100, 60, 30))
        social_text = self.font.render(f"人脉: {social}", True, (100, 60, 30))
        reputation_text = self.font.render(f"声望: {reputation}", True, (100, 60, 30))
        
        self.screen.blit(skill_text, (secondary_attrs_x, secondary_attrs_y))
        self.screen.blit(social_text, (secondary_attrs_x, secondary_attrs_y + 30))
        self.screen.blit(reputation_text, (secondary_attrs_x, secondary_attrs_y + 60))
        
        # 绘制学习属性
        study_attrs_x = 180
        study_attrs_y = 510
        
        theory_experiment = getattr(self.game.player, 'theory_experiment', 0)
        total_theory_experiment = getattr(self.game.player, 'total_theory_experiment', 0)
        employment_entrepreneurship = getattr(self.game.player, 'employment_entrepreneurship', 0)
        aesthetic_cultivation = getattr(self.game.player, 'aesthetic_cultivation', 0)
        
        theory_text = self.font.render(f"理论实验(本学期): {theory_experiment}", True, (100, 60, 30))
        total_theory_text = self.font.render(f"理论实验(累计): {total_theory_experiment}", True, (100, 60, 30))
        employment_text = self.font.render(f"创新创业: {employment_entrepreneurship}", True, (100, 60, 30))
        aesthetic_text = self.font.render(f"美育素养: {aesthetic_cultivation}", True, (100, 60, 30))
        
        self.screen.blit(theory_text, (study_attrs_x, study_attrs_y))
        self.screen.blit(total_theory_text, (study_attrs_x, study_attrs_y + 30))
        self.screen.blit(employment_text, (study_attrs_x, study_attrs_y + 60))
        self.screen.blit(aesthetic_text, (study_attrs_x, study_attrs_y + 90))
    
    def _draw_attribute_bar(self, x, y, label, value, max_value):
        """绘制属性条"""
        bar_width = 200
        bar_height = 20
        
        # 计算进度
        progress = min(value / max_value, 1.0) if max_value > 0 else 0
        
        # 绘制标签
        label_text = self.small_font.render(label, True, (100, 60, 30))
        self.screen.blit(label_text, (x, y - 15))
        
        # 绘制进度条背景
        pygame.draw.rect(self.screen, (200, 200, 200), (x, y, bar_width, bar_height))
        
        # 绘制进度条
        fill_width = int(bar_width * progress)
        pygame.draw.rect(self.screen, (150, 100, 50), (x, y, fill_width, bar_height))
        
        # 绘制数值
        value_text = self.small_font.render(f"{value}/{max_value}", True, (100, 60, 30))
        self.screen.blit(value_text, (x + bar_width + 10, y))
    
    def _draw_course_progress(self):
        """绘制学期结算与课程进度区"""
        border_color = (150, 100, 50)
        
        # 绘制课程进度标题
        course_title = self.font.render("课程进度", True, (100, 60, 30))
        self.screen.blit(course_title, (700, 120))
        
        # 绘制学期信息
        time_display = self.game.time_system.get_time_display()
        semester_text = self.font.render(f"当前学期: {time_display}", True, (100, 60, 30))
        self.screen.blit(semester_text, (700, 160))
        
        # 计算成绩和排名
        theory_experiment = getattr(self.game.player, 'theory_experiment', 0)
        employment_entrepreneurship = getattr(self.game.player, 'employment_entrepreneurship', 0)
        aesthetic_cultivation = getattr(self.game.player, 'aesthetic_cultivation', 0)
        
        # 计算平均成绩
        theory_experiment = getattr(self.game.player, 'theory_experiment', 0)
        employment_entrepreneurship = getattr(self.game.player, 'employment_entrepreneurship', 0)
        aesthetic_cultivation = getattr(self.game.player, 'aesthetic_cultivation', 0)
        
        # 检查是否经历过期末周
        final_scores = getattr(self.game, 'final_scores', [])
        print(f"Debug: final_scores = {final_scores}")
        if final_scores:
            # 计算期末周成绩的平均值
            avg_score = sum(final_scores) // len(final_scores)
            score_text = self.font.render(f"平均成绩: {avg_score}", True, (100, 60, 30))
        else:
            score_text = self.font.render("平均成绩: 无", True, (100, 60, 30))
        
        self.screen.blit(score_text, (700, 190))
        
        # 绘制已修课程列表
        course_list_title = self.font.render("已修课程:", True, (100, 60, 30))
        self.screen.blit(course_list_title, (700, 220))
        
        # 绘制课程列表
        course_y = 250
        if hasattr(self.game, 'course_study_counts'):
            for course_name, count in self.game.course_study_counts.items():
                # 查找课程信息
                course_info = self._get_course_info(course_name)
                if course_info:
                    hours = course_info['hours']
                    progress = min(count / hours, 1.0) * 100
                    course_text = self.small_font.render(
                        f"{course_name}: {count}/{hours} 学时 ({progress:.1f}%)", 
                        True, (100, 60, 30)
                    )
                    self.screen.blit(course_text, (700, course_y))
                    course_y += 20
    
    def _get_course_info(self, course_name):
        """获取课程信息"""
        # 课程数据
        courses = {
            "固体物理": {"hours": 16, "attribute": "theory_experiment", "value": 100},
            "材料分析技术": {"hours": 16, "attribute": "theory_experiment", "value": 100},
            "量子力学导论": {"hours": 16, "attribute": "theory_experiment", "value": 100},
            "大学物理实验": {"hours": 16, "attribute": "theory_experiment", "value": 100},
            "数理方法": {"hours": 16, "attribute": "theory_experiment", "value": 100},
            "材料合成与制备": {"hours": 12, "attribute": "theory_experiment", "value": 75},
            "金相分析实验": {"hours": 12, "attribute": "theory_experiment", "value": 75},
            "工程制图": {"hours": 12, "attribute": "theory_experiment", "value": 75},
            "计算机辅助设计": {"hours": 12, "attribute": "theory_experiment", "value": 75},
            "材料性能实验": {"hours": 12, "attribute": "theory_experiment", "value": 75},
            "大学英语": {"hours": 8, "attribute": "theory_experiment", "value": 50},
            "思修与法律基础": {"hours": 8, "attribute": "theory_experiment", "value": 50},
            "大学体育": {"hours": 8, "attribute": "theory_experiment", "value": 50},
            "科研项目实训": {"hours": 16, "attribute": "employment_entrepreneurship", "value": 100},
            "企业实习实践": {"hours": 16, "attribute": "employment_entrepreneurship", "value": 100},
            "专利撰写与申报": {"hours": 16, "attribute": "employment_entrepreneurship", "value": 100},
            "创业大赛指导": {"hours": 16, "attribute": "employment_entrepreneurship", "value": 100},
            "本科就业指导": {"hours": 8, "attribute": "employment_entrepreneurship", "value": 50},
            "科研伦理与规范": {"hours": 8, "attribute": "employment_entrepreneurship", "value": 50},
            "科技文献检索": {"hours": 8, "attribute": "employment_entrepreneurship", "value": 50},
            "交响乐团鉴赏": {"hours": 16, "attribute": "aesthetic_cultivation", "value": 100},
            "中国书法艺术": {"hours": 16, "attribute": "aesthetic_cultivation", "value": 100},
            "国画赏析": {"hours": 16, "attribute": "aesthetic_cultivation", "value": 100},
            "影视鉴赏": {"hours": 16, "attribute": "aesthetic_cultivation", "value": 100},
            "西方哲学史": {"hours": 16, "attribute": "aesthetic_cultivation", "value": 100},
            "演讲与口才": {"hours": 12, "attribute": "aesthetic_cultivation", "value": 75},
            "摄影技术": {"hours": 12, "attribute": "aesthetic_cultivation", "value": 75},
            "舞蹈基础": {"hours": 12, "attribute": "aesthetic_cultivation", "value": 75},
            "茶文化": {"hours": 12, "attribute": "aesthetic_cultivation", "value": 75},
            "中外民俗": {"hours": 12, "attribute": "aesthetic_cultivation", "value": 75},
            "心理健康": {"hours": 12, "attribute": "aesthetic_cultivation", "value": 75},
            "安全教育": {"hours": 8, "attribute": "aesthetic_cultivation", "value": 50},
            "通识课任选": {"hours": 8, "attribute": "aesthetic_cultivation", "value": 50},
        }
        return courses.get(course_name)
    
    def handle_events(self, events):
        """处理事件"""
        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # 左键点击
                    pos = pygame.mouse.get_pos()
                    if self.back_button.collidepoint(pos):
                        return self.previous_state
        return None