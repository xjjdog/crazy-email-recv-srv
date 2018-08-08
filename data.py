import datetime
import sqlite3
import json


class DataAccess:
    def __init__(self):
        self.conn = sqlite3.connect(":memory:", check_same_thread=False);
        c = self.conn.cursor()
        c.execute("CREATE TABLE msg(frm TEXT, to0 TEXT, tos TEXT, subject TEXT, content TEXT,createDate timestamp)");
        c.execute("CREATE INDEX index_frm ON msg (frm);")
        c.execute("CREATE INDEX index_to0 ON msg (to0);")
        self.conn.commit()

    def store_msg(self, msg):
        c = self.conn.cursor()
        c.execute("insert into msg values(?,?,?,?,?,?)",
                  (msg['from'], msg['to'][0], json.dumps(msg['to']), msg['subject'], msg['content'],
                   datetime.datetime.now()))
        self.conn.commit()

    def read_from(self, frm):
        c = self.conn.cursor()
        t = c.execute("select * from msg where frm = ? order by createDate desc limit 100", (frm,))
        rs = t.fetchall()
        return self.transform(rs)

    def read_to(self, to):
        c = self.conn.cursor()
        t = c.execute("select * from msg where to0 = ? order by createDate desc limit 100", (to,))
        rs = t.fetchall()
        return self.transform(rs)

    def read_all(self):
        c = self.conn.cursor()
        t = c.execute("select * from msg order by createDate desc limit 100")
        rs = t.fetchall()
        return self.transform(rs)

    def transform(self, all):
        rs = []
        for item in all:
            p = {
                "from": item[0],
                "to0": item[1],
                "to": json.loads(item[2]),
                "subject": item[3],
                "content": item[4],
                "time": item[5],
            }
            rs.append(p)
        return rs


dataInstance = DataAccess()
