import couchdb
import time

start = time.time()
dic1 = {}

try:
    couchclient = couchdb.Server('http://admin:admin@172.26.132.32:5984/')
except:
    print("Cannot connected to CouchDB Server\n")
    raise


try:
    db = couchclient['twitter']
    print("Connected to the user database")
except:
    print("Could not Connected to the twitter database")

duplicate_mango = {"selector": {},
                   "fields": ["_rev", "_id", "id", "createtime", "text", "user_id",
                              "lang", "general_emotion", "top_emotion"], "limit": db.__len__()}


# i = 0
# for item in db.find(duplicate_mango):
#     i = i + 1
#     print(i)

# couchclient.create('no_duplicate_twitter')
db2 = couchclient['no_duplicate_twitter']

def save(database, mango):
    print("start saving")
    n = 0
    for items in database.find(mango):
        n = n + 1
        print(n)
        # print(items["_rev"])
        if items["_rev"] not in dic1.keys():
            dic1.update({items["_rev"]: items})
        else:
            continue
    print(len(dic1))
    for items in dic1.values():
        db2.save(
            {"id": items["id"], "createtime": items["createtime"], "text": items["text"],
             "user_id": items["user_id"],
             "lang": items["lang"], 
             "general_emotion": items["general_emotion"],
             "top_emotion": items["top_emotion"]})


if db2.__len__() == 0:
    try:
        couchclient.delete('lines_processed')
        couchclient.create('lines_processed')
    except:
        couchclient.create('lines_processed')
    db3 = couchclient['lines_processed']
    db3.save({"lines_processed": db.__len__()})
    save(db, duplicate_mango)


else:
    print("coming here !")

    try:
        couchclient.delete('lines_processed')
        couchclient.create('lines_processed')
    except:
        couchclient.create('lines_processed')
    db3 = couchclient['lines_processed']
    db3.save({"lines_processed": db2.__len__()})

    lines_processedmango = {"selector": {}, "limit": db3.__len__()}
    for items in db3.find(lines_processedmango):
        lines_processed = (items["lines_processed"])
        print(lines_processed)
    if lines_processed != db.__len__():
        duplicate_mango2 = {"selector": {},
                            "fields": ["_rev", "_id", "id", "createtime", "user_id",
                                       "lang", "general_emotion", "top_emotion"], "limit": db.__len__(),
                            "skip": lines_processed}
        save(db, duplicate_mango2)
    couchclient.delete('lines_processed')
    couchclient.create('lines_processed')
    db4 = couchclient['lines_processed']
    db4.save({"lines_processed": db.__len__()})

end = time.time()
print(end - start)
