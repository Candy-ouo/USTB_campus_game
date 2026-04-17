import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))


class TimeSystem:
    def __init__(self):
        self.day = 1  # 内部计数，从1到136
        self.ended = False
    
    def reset(self):
        self.day = 1
        self.ended = False
    
    def next_day(self):
        if self.ended:
            return False
        
        self.day += 1
        
        if self.day > 136:
            self.ended = True
        
        return True
    
    def next_week(self):
        if self.ended:
            return False
        
        # 进入下一周（增加1天，因为游戏中一周就是1天）
        self.day += 1
        
        if self.day > 136:
            self.ended = True
        
        return True
    
    def get_year(self):
        # 每过两个期末周（两个学期）才算一个学年
        semester = self.get_semester()
        
        # 每两个学期为一个学年
        # 第1-2学期 = 第1学年
        # 第3-4学期 = 第2学年
        # 第5-6学期 = 第3学年
        # 第7-8学期 = 第4学年
        return ((semester - 1) // 2) + 1
    
    def get_semester(self):
        semester = (self.day - 1) // 17 + 1
        return semester
    
    def get_month(self):
        semester = self.get_semester()
        week_in_semester = (self.day - 1) % 17  # 每学期17周（16周教学+1周期末）
        
        # 秋季学期（9-12月 + 1月期末）
        if semester % 2 == 1:
            if week_in_semester < 16:
                month_index = week_in_semester // 4
                months = [9, 10, 11, 12]
                return months[month_index]
            else:
                return 1  # 1月期末周
        # 春季学期（3-6月 + 7月期末）
        else:
            if week_in_semester < 16:
                month_index = week_in_semester // 4
                months = [3, 4, 5, 6]
                return months[month_index]
            else:
                return 7  # 7月期末周
    
    def get_week_in_month(self):
        week_in_semester = (self.day - 1) % 17  # 每学期17周（16周教学+1周期末）
        if week_in_semester == 16:
            return "期末周"
        else:
            return (week_in_semester % 4) + 1
    
    def get_total_days(self):
        return self.day
    
    def is_start_of_semester(self):
        week_in_semester = (self.day - 1) % 17
        return week_in_semester == 0
    
    def is_mid_term(self):
        week_in_semester = (self.day - 1) % 17
        return week_in_semester == 7  # 第8周（从0开始计数）
    
    def is_final_exam_week(self):
        week_in_semester = (self.day - 1) % 17
        # 每学期的第17周（索引16）是期末周
        return week_in_semester == 16
    
    def is_vacation(self):
        semester = self.get_semester()
        week_in_semester = (self.day - 1) % 17
        
        # 2月和8月为假期
        # 春季学期结束后是2月假期
        if semester % 2 == 0 and week_in_semester == 16:
            return True
        # 秋季学期结束后是8月假期
        if semester % 2 == 1 and week_in_semester == 16:
            return True
        
        return False
    
    def get_time_display(self):
        year = self.get_year()
        month = self.get_month()
        week_in_month = self.get_week_in_month()
        if week_in_month == "期末周":
            return f"第 {year} 年 | {month} 月 | 期末周"
        else:
            return f"第 {year} 年 | {month} 月 | 第 {week_in_month} 周"
    
    def is_ended(self):
        return self.ended
    
    def to_dict(self):
        return {
            'day': self.day,
            'ended': self.ended
        }
    
    def from_dict(self, data):
        if 'day' in data:
            self.day = data['day']
        if 'ended' in data:
            self.ended = data['ended']
