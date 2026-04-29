import json
import os

class SimpleAI:
    def __init__(self):
        self.config = self._load_config()
        self.client = None
        
    def _load_config(self):
        config_path = os.path.join(os.path.dirname(__file__), '..', 'ai_config.json')
        try:
            with open(config_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except:
            return {"enabled": False, "provider": "volcengine", "api_key": "", "secret_key": "", "probability": 0.3}
    
    def is_enabled(self):
        if not self.config.get("enabled", False):
            return False
        provider = self.config.get("provider", "volcengine")
        if provider == "mock":
            return True
        if not self.config.get("api_key"):
            return False
        if provider == "baidu" and not self.config.get("secret_key"):
            return False
        return True
    
    def generate_event(self):
        provider = self.config.get("provider", "volcengine")
        
        if provider == "mock":
            return self._generate_mock()
        elif provider == "volcengine":
            return self._generate_volcengine()
        else:
            return self._generate_baidu()
    
    def _generate_mock(self):
        import random
        
        mock_events = [
            {
                "title": "图书馆占座",
                "description": "你发现有人用书包占座但人不在，怎么办？",
                "options": [
                    {"text": "直接坐下", "effects": {"mood": 2, "charm": -2}},
                    {"text": "耐心等待", "effects": {"knowledge": 1, "mood": -1}},
                    {"text": "找管理员", "effects": {"social": 1}}
                ]
            },
            {
                "title": "小组作业",
                "description": "小组作业有人划水，进度落后了。",
                "options": [
                    {"text": "自己全包", "effects": {"knowledge": 3, "mood": -5}},
                    {"text": "分工催促", "effects": {"social": 2, "mood": -2}},
                    {"text": "找老师反映", "effects": {"charm": -3}}
                ]
            },
            {
                "title": "食堂排队",
                "description": "食堂人很多，有人想插队到你前面。",
                "options": [
                    {"text": "让他插队", "effects": {"charm": 2, "mood": -2}},
                    {"text": "拒绝并指责", "effects": {"mood": -1}},
                    {"text": "提出轮流排", "effects": {"charm": 1, "social": 1}}
                ]
            },
            {
                "title": "快递丢失",
                "description": "你收到的快递包裹不见了。",
                "options": [
                    {"text": "联系快递员", "effects": {"social": 1, "action_points": -1}},
                    {"text": "去快递点找", "effects": {"physical": 1, "action_points": -1}},
                    {"text": "自认倒霉", "effects": {"mood": -5}}
                ]
            },
            {
                "title": "考试漏题",
                "description": "同学说有考试题目泄露，问你要不要看。",
                "options": [
                    {"text": "拒绝", "effects": {"charm": 2, "mood": -1}},
                    {"text": "看一点", "effects": {"knowledge": 2, "charm": -3}},
                    {"text": "告诉老师", "effects": {"reputation": 2}}
                ]
            }
        ]
        
        return random.choice(mock_events)
    
    def _generate_volcengine(self):
        api_key = self.config["api_key"]
        endpoint = self.config.get("endpoint", "")
        
        if not endpoint:
            raise Exception("请在配置中添加endpoint字段（推理接入点ID）")
        
        import requests
        
        url = "https://ark.cn-beijing.volces.com/api/v3/chat/completions"
        
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {api_key}"
        }
        
        prompt = """生成一个中国大学生校园生活随机事件，输出JSON格式：
{
    "title": "事件标题(不超过10字)",
    "description": "事件描述(不超过50字)",
    "options": [
        {"text": "选项1", "effects": {"knowledge":2,"mood":-3}},
        {"text": "选项2", "effects": {"charm":1}},
        {"text": "选项3", "effects": {"health":-2}}
    ]
}
属性: knowledge学识 charm魅力 physical体能 living_expenses生活费 action_points行动力 mood心情 health健康 social人脉
数值范围-10到+10，每个选项最多3个属性。"""
        
        data = {
            "model": endpoint,
            "messages": [{"role": "user", "content": prompt}]
        }
        
        try:
            response = requests.post(url, headers=headers, json=data)
            response.raise_for_status()
            result = response.json()
            content = result.get("choices", [{}])[0].get("message", {}).get("content", "")
            return json.loads(content)
        except requests.exceptions.RequestException as e:
            error_msg = str(e)
            if response:
                try:
                    error_detail = response.json()
                    error_msg = f"{error_msg} - {error_detail}"
                except:
                    pass
            raise Exception(f"火山引擎调用失败: {error_msg}")
        except json.JSONDecodeError:
            raise Exception(f"AI返回格式错误: {content}")
    
    def _generate_baidu(self):
        import requests
        import time
        
        if not hasattr(self, 'access_token') or not self.access_token or time.time() >= getattr(self, 'token_expire', 0):
            url = "https://aip.baidubce.com/oauth/2.0/token"
            params = {
                "grant_type": "client_credentials",
                "client_id": self.config["api_key"],
                "client_secret": self.config["secret_key"]
            }
            res = requests.post(url, params=params)
            data = res.json()
            self.access_token = data.get("access_token")
            self.token_expire = time.time() + data.get("expires_in", 3600) - 100
        
        url = f"https://aip.baidubce.com/rpc/2.0/ai_custom/v1/wenxinworkshop/chat/completions_pro?access_token={self.access_token}"
        
        prompt = """生成一个中国大学生校园生活随机事件，输出JSON格式：
{
    "title": "事件标题(不超过10字)",
    "description": "事件描述(不超过50字)",
    "options": [
        {"text": "选项1", "effects": {"knowledge":2,"mood":-3}},
        {"text": "选项2", "effects": {"charm":1}},
        {"text": "选项3", "effects": {"health":-2}}
    ]
}
属性: knowledge学识 charm魅力 physical体能 living_expenses生活费 action_points行动力 mood心情 health健康 social人脉
数值范围-10到+10，每个选项最多3个属性。"""
        
        try:
            res = requests.post(url, json={"model":"completions_pro","messages":[{"role":"user","content":prompt}]})
            data = res.json()
            content = data.get("result", {}).get("choices", [{}])[0].get("message", {}).get("content", "")
            return json.loads(content)
        except Exception as e:
            raise Exception(f"百度AI调用失败: {str(e)}")