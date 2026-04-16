import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))


class Player:
    def __init__(self):
        # 主属性（等级1-4，经验0-100）
        self.knowledge = 30  # 学识经验，第一级初始为30
        self.knowledge_level = 1
        
        self.charm = 30  # 魅力经验，第一级初始为30
        self.charm_level = 1
        
        self.physical = 30  # 体能经验，第一级初始为30
        self.physical_level = 1
        
        # 生活属性
        self.living_expenses = 200  # 生活费
        self.action_points = 5  # 行动力
        self.mood = 100  # 心情
        self.health = 80  # 健康值
        self.is_sick = False  # 是否生病
        
        # 副属性
        self.skill = 0  # 技能
        self.social = 0  # 人脉
        self.reputation = 0  # 声望
        
        # 学习属性
        self.theory_experiment = 0  # 理论/实验
        self.employment_entrepreneurship = 0  # 就业/创业
        self.aesthetic_cultivation = 0  # 美育/素养
    
    def reset(self):
        # 重置所有属性
        self.knowledge = 30  # 第一级初始为30
        self.knowledge_level = 1
        self.charm = 30  # 第一级初始为30
        self.charm_level = 1
        self.physical = 30  # 第一级初始为30
        self.physical_level = 1
        self.living_expenses = 200
        self.action_points = 5
        self.mood = 100
        self.health = 80
        self.is_sick = False
        self.skill = 0
        self.social = 0
        self.reputation = 0
        self.theory_experiment = 0
        self.employment_entrepreneurship = 0
        self.aesthetic_cultivation = 0
    
    def _level_up(self, exp, level, current_year=None):
        """处理等级升级逻辑"""
        # 如果提供了当前学年，检查等级限制
        if current_year is not None and level >= current_year:
            # 一学年只能最高只能达到当前等级的100/100+
            if exp >= 100:
                exp = 100
            return exp, level
        
        while exp >= 100:
            exp -= 100
            level += 1
            if level > 4:
                level = 4
                exp = 100
                break
            # 如果提供了当前学年，检查等级限制
            if current_year is not None and level >= current_year:
                break
        return exp, level
    
    def add_knowledge(self, amount, current_year=None):
        """增加学识经验"""
        self.knowledge += amount
        self.knowledge, self.knowledge_level = self._level_up(self.knowledge, self.knowledge_level, current_year)
        return self.knowledge_level
    
    def add_charm(self, amount, current_year=None):
        """增加魅力经验"""
        self.charm += amount
        self.charm, self.charm_level = self._level_up(self.charm, self.charm_level, current_year)
        return self.charm_level
    
    def add_physical(self, amount, current_year=None):
        """增加体能经验"""
        old_level = self.physical_level
        self.physical += amount
        self.physical, self.physical_level = self._level_up(self.physical, self.physical_level, current_year)
        
        # 体能升级时增加行动力上限
        if self.physical_level > old_level:
            self.action_points = 5 + (self.physical_level - 1)
        
        return self.physical_level
    
    def add_living_expenses(self, amount):
        """增加生活费"""
        self.living_expenses += amount
        if self.living_expenses < 0:
            self.living_expenses = 0
        return self.living_expenses
    
    def add_action_points(self, amount):
        """增加行动力"""
        max_points = 5 + (self.physical_level - 1)
        # 健康值影响
        if self.health < 60:
            max_points = max(1, max_points // 2)
        self.action_points += amount
        if self.action_points > max_points:
            self.action_points = max_points
        if self.action_points < 0:
            self.action_points = 0
        return self.action_points
    
    def add_mood(self, amount):
        """增加心情"""
        self.mood += amount
        if self.mood > 100:
            self.mood = 100
        if self.mood < 0:
            self.mood = 0
        return self.mood
    
    def add_skill(self, amount):
        """增加技能"""
        self.skill += amount
        if self.skill < 0:
            self.skill = 0
        return self.skill
    
    def add_social(self, amount):
        """增加人脉"""
        self.social += amount
        if self.social < 0:
            self.social = 0
        return self.social
    
    def add_reputation(self, amount):
        """增加声望"""
        self.reputation += amount
        if self.reputation < 0:
            self.reputation = 0
        return self.reputation
    
    def add_health(self, amount):
        """增加健康值"""
        self.health += amount
        if self.health > 100:
            self.health = 100
        if self.health < 0:
            self.health = 0
        # 检查是否生病
        if self.health < 40:
            self.is_sick = True
        else:
            self.is_sick = False
        return self.health
    
    def add_theory_experiment(self, amount):
        """增加理论/实验"""
        self.theory_experiment += amount
        if self.theory_experiment < 0:
            self.theory_experiment = 0
        return self.theory_experiment
    
    def add_employment_entrepreneurship(self, amount):
        """增加就业/创业"""
        self.employment_entrepreneurship += amount
        if self.employment_entrepreneurship < 0:
            self.employment_entrepreneurship = 0
        return self.employment_entrepreneurship
    
    def add_aesthetic_cultivation(self, amount):
        """增加美育/素养"""
        self.aesthetic_cultivation += amount
        if self.aesthetic_cultivation < 0:
            self.aesthetic_cultivation = 0
        return self.aesthetic_cultivation
    
    def get_knowledge(self):
        """获取学识经验和等级"""
        return self.knowledge, self.knowledge_level
    
    def get_charm(self):
        """获取魅力经验和等级"""
        return self.charm, self.charm_level
    
    def get_physical(self):
        """获取体能经验和等级"""
        return self.physical, self.physical_level
    
    def get_living_expenses(self):
        """获取生活费"""
        return self.living_expenses
    
    def get_action_points(self):
        """获取行动力"""
        return self.action_points
    
    def get_mood(self):
        """获取心情"""
        return self.mood
    
    def get_skill(self):
        """获取技能"""
        return self.skill
    
    def get_social(self):
        """获取人脉"""
        return self.social
    
    def get_reputation(self):
        """获取声望"""
        return self.reputation
    
    def get_health(self):
        """获取健康值"""
        return self.health
    
    def get_theory_experiment(self):
        """获取理论/实验"""
        return self.theory_experiment
    
    def get_employment_entrepreneurship(self):
        """获取就业/创业"""
        return self.employment_entrepreneurship
    
    def get_aesthetic_cultivation(self):
        """获取美育/素养"""
        return self.aesthetic_cultivation
    
    def to_dict(self):
        """转换为字典用于存档"""
        return {
            'knowledge': self.knowledge,
            'knowledge_level': self.knowledge_level,
            'charm': self.charm,
            'charm_level': self.charm_level,
            'physical': self.physical,
            'physical_level': self.physical_level,
            'living_expenses': self.living_expenses,
            'action_points': self.action_points,
            'mood': self.mood,
            'health': self.health,
            'skill': self.skill,
            'social': self.social,
            'reputation': self.reputation,
            'theory_experiment': self.theory_experiment,
            'employment_entrepreneurship': self.employment_entrepreneurship,
            'aesthetic_cultivation': self.aesthetic_cultivation
        }
    
    def from_dict(self, data):
        """从字典加载存档"""
        if 'knowledge' in data:
            self.knowledge = data['knowledge']
        if 'knowledge_level' in data:
            self.knowledge_level = data['knowledge_level']
        if 'charm' in data:
            self.charm = data['charm']
        if 'charm_level' in data:
            self.charm_level = data['charm_level']
        if 'physical' in data:
            self.physical = data['physical']
        if 'physical_level' in data:
            self.physical_level = data['physical_level']
        if 'living_expenses' in data:
            self.living_expenses = data['living_expenses']
        if 'action_points' in data:
            self.action_points = data['action_points']
        if 'mood' in data:
            self.mood = data['mood']
        if 'health' in data:
            self.health = data['health']
        if 'skill' in data:
            self.skill = data['skill']
        if 'social' in data:
            self.social = data['social']
        if 'reputation' in data:
            self.reputation = data['reputation']
        if 'theory_experiment' in data:
            self.theory_experiment = data['theory_experiment']
        if 'employment_entrepreneurship' in data:
            self.employment_entrepreneurship = data['employment_entrepreneurship']
        if 'aesthetic_cultivation' in data:
            self.aesthetic_cultivation = data['aesthetic_cultivation']
    
    def is_sick(self):
        """检查是否生病（健康值低于40）"""
        return self.health < 40
    
    def can_interact(self):
        """检查是否可以交互（除了校医院）"""
        return self.health >= 40
    
    def reset_monthly(self):
        """每月重置生活费"""
        self.living_expenses = 200
    
    def reset_daily(self):
        """每天重置行动点"""
        max_points = 5 + (self.physical_level - 1)
        # 健康值影响
        if self.health < 60:
            max_points = max(1, max_points // 2)
        self.action_points = max_points
