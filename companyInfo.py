from bs4 import BeautifulSoup
from common import common
import constants


class companyInfo:

    def method(self, code):
        url = constants.companyInfoUrl % code

        c = common()
        html = c.fakerHead(url)
        soup = BeautifulSoup(html, "lxml")
        soup = soup.findAll('table', attrs={"class": {"table_bg001 border_box limit_sale table_details"}})

        companyTemp = [code]
        for val in soup:
            temp = val.findAll('td')
            cnt = 0
            for tt in temp:
                t = tt.text
                t = t.replace('-', '').replace('\r', '').replace('\n', '')
                if cnt != 13:
                    t = t.replace(' ','')
                if cnt % 2 == 1:
                    companyTemp.append(t)
                cnt = cnt + 1

        print('读取股票代码'+code+'的上市公司基本数据成功')

        return companyTemp






