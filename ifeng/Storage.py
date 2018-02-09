import pymysql,traceback
class Storage(object):
    def __init__(self):
        self.userName = 'root'
        self.passWord = 'zhangyanping'
        self.dbName = 'ifeng'
        self.host = 'localhost'

    def connect(self):
        db = pymysql.connect(self.host,self.userName,self.passWord,self.dbName,)
        return db
    def insert(self,article):
        db = self.connect()
        cursor = db.cursor()
        if article is not None:
            sql = r'insert into ifeng_news(url,title,content,keyword,afrom,atime)VALUES("%s","%s","%s","%s","%s","%s")'%\
                   (article['url'],article['title'],article['content'],article['keyword'],article['from'],article['time'])
            try:
                cursor.execute(sql)
                db.commit()
            except Exception as e:
                traceback.print_exc(e)
                db.rollback()
            db.close()
if __name__ == '__main__':
    s = Storage()
    try:
      s.connect()
    except Exception as e:
        traceback.print_exception(e)