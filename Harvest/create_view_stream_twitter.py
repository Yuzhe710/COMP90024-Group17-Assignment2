import logging
import couchdb

couchclient = couchdb.Server('http://admin:admin@172.26.132.32:5984/')
db = couchclient['twitter']


if db.__contains__('_design/textblob_sentiment_analysis'):
    db.__delitem__('_design/textblob_sentiment_analysis')


def createView(dbConn, designDoc, viewName, mapFunction, reduceFunction):
    data = {
        "_id": f"_design/{designDoc}",
        "views": {
            viewName: {
                "map": mapFunction,
                "reduce": reduceFunction
            }
        },
        "language": "javascript",
        "options": {"partitioned": False}
    }
    logging.info(f"creating view {designDoc}/{viewName}")
    dbConn.save(data)


def addView(db, designDoc, viewName, mapFunction, reduceFunction):
    db_add = db['_design/' + designDoc]['views'].keys()
    keys = []
    mapF = []
    for i in db_add:
        print(i)
        keys.append(i)
        func = db['_design/' + designDoc]['views'].get(i)
        mapF.append(func)
    db.__delitem__('_design/' + designDoc)
    new_views = {}
    for j in range(keys.__len__()):
        new_views[keys[j]] = mapF[j]
    new_views[viewName] = {"map": mapFunction, "reduce": reduceFunction}
    data = {
        "_id": f"_design/{designDoc}",
        "views": new_views,
        "language": "javascript",
        "options": {"partitioned": False}
    }
    db.save(data)


map_function_textblob_sentiment="""function (doc) {
    const general_emotion = doc.general_emotion
    const top_emotion = doc.top_emotion
    emit([general_emotion, top_emotion], 1)
}
"""

# reduce_function_textblob_sentiment="""function(keys, values, rereduce) {

#     if (rereduce) {
#       return{
#       'sum': values.reduce(function(a, b) { return a + b.sum }, 0),
#       'count': values.reduce(function(a, b) { return a + b.count }, 0),
#       'average':values.reduce(function(a, b) { return a + b.sum }, 0)/values.reduce(function(a, b) { return a + b.count }, 0)
#       }

#     } else {
#         return {
#             'sum': sum(values),
#             'min': Math.min.apply(null, values),
#             'max': Math.max.apply(null, values),
#             'count': values.length,
#             'sumsqr': (function() {
#             var sumsqr = 0;

#             values.forEach(function (value) {
#                 sumsqr += value * value;
#             });

#             return sumsqr;
#             })(),
#         }
#     }
# }
# """

reduce_function_textblob_sentiment ="""function(keys, values, rereduce) {
    if (rereduce) {
        return sum(values)
    } else {
        return values.length
    }
}
"""

design_doc_textblob_sentiment = "textblob_sentiment_analysis"
view_name_textblob_sentiment = "textblob_sentiment"
createView(dbConn=db, designDoc=design_doc_textblob_sentiment, viewName=view_name_textblob_sentiment, 
            mapFunction=map_function_textblob_sentiment, reduceFunction=reduce_function_textblob_sentiment)