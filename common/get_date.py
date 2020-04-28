import datetime


class GetDate():
    #获取当天日期（返回时间格式）
    def get_today_date(self):
        return datetime.date.today()
    #获取当天日期（返回时间字符串格式）
    def get_today_str_data(self):
        today=datetime.datetime.today()
        return today.strftime("%Y-%m-%d")
    #获取昨天日期
    def get_yesterday_date(self):
        today=self.get_today_date()
        yesterday=today - datetime.timedelta(days=1)
        return yesterday
    #获取明天日期
    def get_tomorrow_date(self):
        today=self.get_today_date()
        tomorrow = today + datetime.timedelta(days=1)
        tomorrow=tomorrow.strftime("%Y-%m-%d")
        return tomorrow
    #获取第20天的日期
    def get_fengpan_date(self):
        today=self.get_today_date()
        fengpan = today + datetime.timedelta(days=20)
        fengpan=fengpan.strftime("%Y-%m-%d")
        return fengpan

    #获取第180天的日期
    def get_zanhuan_date(self):
        today=self.get_today_date()
        zanhuan = today + datetime.timedelta(days=180)
        zanhuan=zanhuan.strftime("%Y-%m-%d")
        return zanhuan

    #获取第二天的某个时间
    def get_tomorrow_date_time(self,time):
        b=self.get_tomorrow_date()
        b=datetime.datetime.strptime(b,"%Y-%m-%d")
        b=b.strftime('%Y-%m-%d')
        return b+" "+time

print(GetDate().get_today_date())