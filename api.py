import pymysql
import json
db = pymysql.connect(host='127.0.0.1', port=3306, user='choigod1023',
                     passwd='jjang486', db='choigod1023', charset='utf8')
cursor = db.cursor()
sql = "SELECT COUNT(*) FROM vlive"
cursor.execute(sql)
row2 = cursor.fetchone()
print(row2[0])
limit = int(row2[0])-1
f= open('./api.json',"a")
for i in range(0,limit):
    sql = 'select * from vlive order by id, name asc limit '+str(i)+',1'
    cursor.execute(sql)
    row2 = cursor.fetchone()
    jso = {"id":row2[0],"title":row2[1]}
    f.write(json.dumps(jso, ensure_ascii=False).encode("EUC-KR"))
f.close()


