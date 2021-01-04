from common import common
import constants
import threading

class stockInfo:
    def method(self, codeList, startTime, currentTime):

        c = common()
        # 创建目录
        mkpath = constants.stockInfoPath + currentTime + '/'
        c.mkdir(mkpath)

        for code in codeList:
            if startTime == '':
                urlTime = constants.stockInfoTimeEnd + currentTime
            else:
                urlTime = constants.stockInfoTimeStart + startTime + constants.stockInfoTimeEnd + currentTime

            url = constants.stockInfoUrlStart + ("0" if code.startswith('6') else "1") + code + urlTime
            url = url + constants.stockInfoUrlEnd

            filePath = mkpath + code + '.csv'
            threading.Thread(target=c.downloadFileSem, args=(url, filePath)).start()
