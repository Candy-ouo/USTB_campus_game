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
    hair_style: int = 0
    top_style: int = 0
    pants_style: int = 0
    color: int = 0
    
    # 主属性 (初始值 40-60)
    gpa: int = field(default_factory=lambda: random.randint(40, 60))
    energy: int = field(default_factory=lambda: random.randint(40, 60))
    social: int = field(default_factory=lambda: random.randint(40, 60))
    skill: int = field(default_factory=lambda: random.randint(40, 60))
    mood: int = field(default_factory=lambda: random.randint(40, 60))
    
    # 子属性 (初始值 30-70)
    logic: int = field(default_factory=lambda: random.randint(30, 70))
    creativity: int = field(default_factory=lambda: random.randint(30, 70))
    eq: int = field(default_factory=lambda: random.randint(30, 70))
    charm: int = field(default_factory=lambda: random.randint(30, 70))
    focus: int = field(default_factory=lambda: random.randint(30, 70))
    luck: int = field(default_factory=lambda: random.randint(30, 70))
    
    # 隐藏属性 (初始值 0)
    skip_count: int = 0
    night_count: int = 0
    competition_wins: int = 0
    papers: int = 0
    certificates: int = 0
    
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
            "hair_style": self.hair_style,
            "top_style": self.top_style,
            "pants_style": self.pants_style,
            "color": self.color,
            # 主属性
            "gpa": self.gpa,
            "energy": self.energy,
            "social": self.social,
            "skill": self.skill,
            "mood": self.mood,
            # 子属性
            "logic": self.logic,
            "creativity": self.creativity,
            "eq": self.eq,
            "charm": self.charm,
            "focus": self.focus,
            "luck": self.luck,
            # 隐藏属性
            "skip_count": self.skip_count,
            "night_count": self.night_count,
            "competition_wins": self.competition_wins,
            "papers": self.papers,
            "certificates": self.certificates
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
            hair_style=data.get("hair_style", 0),
            top_style=data.get("top_style", 0),
            pants_style=data.get("pants_style", 0),
            color=data.get("color", 0),
            gpa=data.get("gpa", 50),
            energy=data.get("energy", 50),
            social=data.get("social", 50),
            skill=data.get("skill", 50),
            mood=data.get("mood", 50),
            logic=data.get("logic", 50),
            creativity=data.get("creativity", 50),
            eq=data.get("eq", 50),
            charm=data.get("charm", 50),
            focus=data.get("focus", 50),
            luck=data.get("luck", 50),
            skip_count=data.get("skip_count", 0),
            night_count=data.get("night_count", 0),
            competition_wins=data.get("competition_wins", 0),
            papers=data.get("papers", 0),
            certificates=data.get("certificates", 0)
        )
