import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))


class Player:
    def __init__(self):
        # 主属性（等级1-4，经验0-100）
        self.knowledge = 0  # 学识经验
        self.knowledge_level = 1
        
        self.charm = 0  # 魅力经验
        self.charm_level = 1
        
        self.physical = 0  # 体能经验
        self.physical_level = 1
        
        # 行动属性
        self.living_expenses = 1000  # 生活费
        self.action_points = 10  # 行动力
        self.mood = 100  # 心情
        
        # 副属性
        self.skill = 0  # 技能
        self.social = 0  # 人脉
        self.reputation = 0  # 声望
    
    def reset(self):
        # 重置所有属性
        self.knowledge = 0
        self.knowledge_level = 1
        self.charm = 0
        self.charm_level = 1
        self.physical = 0
        self.physical_level = 1
        self.living_expenses = 1000
        self.action_points = 10
        self.mood = 100
        self.skill = 0
        self.social = 0
        self.reputation = 0
    
    def _level_up(self, exp, level):
        """处理等级升级逻辑"""
        while exp >= 100:
            exp -= 100
            level += 1
            if level > 4:
                level = 4
                exp = 100
                break
        return exp, level
    
    def add_knowledge(self, amount):
        """增加学识经验"""
        # 心情影响
        if self.mood < 50:
            amount = int(amount * 0.5)
        
        self.knowledge += amount
        self.knowledge, self.knowledge_level = self._level_up(self.knowledge, self.knowledge_level)
        return self.knowledge_level
    
    def add_charm(self, amount):
        """增加魅力经验"""
        # 心情影响
        if self.mood < 50:
            amount = int(amount * 0.5)
        
        self.charm += amount
        self.charm, self.charm_level = self._level_up(self.charm, self.charm_level)
        return self.charm_level
    
    def add_physical(self, amount):
        """增加体能经验"""
        # 心情影响
        if self.mood < 50:
            amount = int(amount * 0.5)
        
        old_level = self.physical_level
        self.physical += amount
        self.physical, self.physical_level = self._level_up(self.physical, self.physical_level)
        
        # 体能升级时增加行动力上限
        if self.physical_level > old_level:
            self.action_points = 10 + (self.physical_level - 1)
        
        return self.physical_level
    
    def add_living_expenses(self, amount):
        """增加生活费"""
        self.living_expenses += amount
        if self.living_expenses < 0:
            self.living_expenses = 0
        return self.living_expenses
    
    def add_action_points(self, amount):
        """增加行动力"""
        max_points = 10 + (self.physical_level - 1)
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
        # 心情影响
        if self.mood < 50:
            amount = int(amount * 0.5)
        
        self.skill += amount
        if self.skill < 0:
            self.skill = 0
        return self.skill
    
    def add_social(self, amount):
        """增加人脉"""
        # 心情影响
        if self.mood < 50:
            amount = int(amount * 0.5)
        
        self.social += amount
        if self.social < 0:
            self.social = 0
        return self.social
    
    def add_reputation(self, amount):
        """增加声望"""
        # 心情影响
        if self.mood < 50:
            amount = int(amount * 0.5)
        
        self.reputation += amount
        if self.reputation < 0:
            self.reputation = 0
        return self.reputation
    
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
            'skill': self.skill,
            'social': self.social,
            'reputation': self.reputation
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
        if 'skill' in data:
            self.skill = data['skill']
        if 'social' in data:
            self.social = data['social']
        if 'reputation' in data:
            self.reputation = data['reputation']
