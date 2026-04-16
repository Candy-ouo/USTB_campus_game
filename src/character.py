"""角色数据模型"""
from dataclasses import dataclass, field
import random
from typing import Dict

# 学院与专业映射
COLLEGE_MAJORS = {
    "材料": ["材料科学与工程", "材料物理", "材料化学"],
    "冶金": ["冶金工程", "钢铁冶金", "有色金属冶金"],
    "计通": ["计算机科学与技术", "通信工程", "信息安全"],
    "经管": ["工商管理", "经济学", "金融学"],
    "文法": ["法学", "行政管理", "社会学"],
    "数理": ["数学与应用数学", "信息与计算科学", "应用物理学"]
}


@dataclass
class Character:
    """角色类"""
    # 基础信息
    name: str = ""
    gender: str = "男"
    height: int = 170
    weight: int = 60
    birthday: str = "01-01"
    college: str = "材料"
    major: str = "材料科学与工程"
    
    # 主属性
    knowledge: int = 30
    charm: int = 30
    energy: int = 30
    
    # 行动属性
    money: int = 1000  # 生活费
    action_points: int = 10  # 行动力
    mood: int = 100  # 心情 0-100
    health: int = 80  # 健康值 0-100
    
    # 副属性
    skill: int = 0
    social_network: int = 0
    reputation: int = 0
    
    # 学习属性
    theory_experiment: int = 0
    employment_entrepreneurship: int = 0
    aesthetic_literacy: int = 0
    

    
    def __post_init__(self):
        """初始化后确保专业与学院匹配"""
        if not self.major or self.major not in COLLEGE_MAJORS.get(self.college, []):
            self.major = self.get_major_by_college(self.college)
    
    @staticmethod
    def get_major_by_college(college: str) -> str:
        """根据学院随机获取一个专业"""
        majors = COLLEGE_MAJORS.get(college, ["未知专业"])
        return random.choice(majors) if majors else "未知专业"
    
    def to_dict(self) -> Dict:
        """转换为字典，用于存档"""
        return {
            # 基础信息
            "name": self.name,
            "gender": self.gender,
            "height": self.height,
            "weight": self.weight,
            "birthday": self.birthday,
            "college": self.college,
            "major": self.major,
            # 主属性
            "knowledge": self.knowledge,
            "charm": self.charm,
            "energy": self.energy,
            # 行动属性
            "money": self.money,
            "action_points": self.action_points,
            "mood": self.mood,
            "health": self.health,
            # 副属性
            "skill": self.skill,
            "social_network": self.social_network,
            "reputation": self.reputation,
            # 学习属性
            "theory_experiment": self.theory_experiment,
            "employment_entrepreneurship": self.employment_entrepreneurship,
            "aesthetic_literacy": self.aesthetic_literacy
        }
    
    @classmethod
    def from_dict(cls, data: Dict) -> "Character":
        """从字典创建实例"""
        return cls(
            name=data.get("name", ""),
            gender=data.get("gender", "男"),
            height=data.get("height", 170),
            weight=data.get("weight", 60),
            birthday=data.get("birthday", "01-01"),
            college=data.get("college", "材料"),
            major=data.get("major", "材料科学与工程"),
            # 主属性
            knowledge=data.get("knowledge", 30),
            charm=data.get("charm", 30),
            energy=data.get("energy", 30),
            # 行动属性
            money=data.get("money", 1000),
            action_points=data.get("action_points", 10),
            mood=data.get("mood", 100),
            health=data.get("health", 80),
            # 副属性
            skill=data.get("skill", 0),
            social_network=data.get("social_network", 0),
            reputation=data.get("reputation", 0),
            # 学习属性
            theory_experiment=data.get("theory_experiment", 0),
            employment_entrepreneurship=data.get("employment_entrepreneurship", 0),
            aesthetic_literacy=data.get("aesthetic_literacy", 0)
        )
