
from pymongo import MongoClient
from datetime import datetime


def answer_time(bef_time,aft_time):

	bf_obj = datetime.strptime(bef_time, '%Y-%m-%d %H:%M:%S.%f')
	bf_milli = bf_obj.timestamp() * 1000

	af_obj = datetime.strptime(aft_time, '%Y-%m-%d %H:%M:%S.%f')
	af_milli = af_obj.timestamp() * 1000

	exec_time = af_milli - bf_milli

	return exec_time

db = MongoClient().dblp

print("CONSULTA 1: Mostrar todas las publicaciones de la base de datos")

before_time = str(datetime.now())

result = db.documents.find()

after_time = str(datetime.now())

execution_time = answer_time(before_time,after_time)

#print(list(result))
print("{0:.2f}".format(execution_time) + " ms")

print("CONSULTA 2: Mostrar todos los artículos en libros.")

before_time = str(datetime.now())

result = db.documents.find({"type":"incollection"})

after_time = str(datetime.now())

execution_time = answer_time(before_time,after_time)

#print(list(result))
print("{0:.2f}".format(execution_time) + " ms")

print("CONSULTA 3: Publicaciones entre los años 1990 y 2000")

before_time = str(datetime.now())

result = db.documents.find({"$and":[
		                        {"year":{"$gte":1990}},
		                        {"year":{"$lte":2000}}]})

after_time = str(datetime.now())

execution_time = answer_time(before_time,after_time)

#print(result)
print("{0:.2f}".format(execution_time) + " ms")

print("CONSULTA 4: Número de artículos en la base de datos")

before_time = str(datetime.now())

result = db.documents.find({"type":"article"}).count()

after_time = str(datetime.now())

execution_time = answer_time(before_time,after_time)

#print(list(result))
print("{0:.2f}".format(execution_time) + " ms")

print("CONSULTA 5: Publicaciones por año de un autor determinado (Lila Kari)")

before_time = str(datetime.now())

result = db.documents.aggregate([{"$match":{"author.Author":"Lila Kari"}},
							{"$group":{"_id":"$year","total":{"$sum":1}}},
							{"$sort":{"_id":1}}],
							allowDiskUse=True)

after_time = str(datetime.now())

execution_time = answer_time(before_time,after_time)

#print(list(result))
print("{0:.2f}".format(execution_time) + " ms")

print("CONSULTA 6: Número de documentos con más de 3 autores")

before_time = str(datetime.now())

result = db.documents.aggregate([{"$unwind":"$author"},
								{"$group":{"_id":"$title","Authors":{"$sum":1}}},
								{"$match":{"Authors":{"$gt":3}}},
								{"$count":"Documentos"}],
								allowDiskUse=True)

after_time = str(datetime.now())

execution_time = answer_time(before_time,after_time)

#print(list(result))
print("{0:.2f}".format(execution_time) + " ms")

print("CONSULTA 7: Coautores de un autor determinado (Lila Kari)")

before_time = str(datetime.now())

result = db.documents.aggregate([{"$match":{"author.Author":"Lila Kari"}},
								{"$unwind":"$author"},
								{"$group":{"_id":"$author.Author"}},
								{"$match":{"_id":{"$ne":"Lila Kari"}}}])

after_time = str(datetime.now())

execution_time = answer_time(before_time,after_time)

#print(list(result))
print("{0:.2f}".format(execution_time) + " ms")

print("CONSULTA 8: Autores que han publicado documentos de un solo tipo")

before_time = str(datetime.now())

db.documents.aggregate([{"$unwind":"$author"},
							{"$group":{"_id":"$author.Author","Tipos":{"$addToSet":"$type"}}},
							{"$out":"AutoresTipos"}],
					   allowDiskUse=True)

result = db.AutoresTipos.aggregate([{"$unwind":"$Tipos"},
									{"$group":{"_id":"$_id","types":{"$sum":1},"unique_type":{"$push":"$Tipos"}}},
									{"$match":{"types":{"$eq":1}}}],
								   allowDiskUse=True)

after_time = str(datetime.now())

execution_time = answer_time(before_time,after_time)

#print(list(result))
print("{0:.2f}".format(execution_time) + " ms")




