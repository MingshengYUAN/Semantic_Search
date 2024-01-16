###############embedding_util.py#################
import time
import pandas as pd
import numpy as np
import requests
import torch
from transformers import AutoTokenizer, AutoModel
from embedding_model_configuration import *
from sentence_transformers import SentenceTransformer
import langid
from numpy.linalg import norm
import xlrd
import chromadb

client = chromadb.PersistentClient(path="./chromadb")

model_en = SentenceTransformer('sentence-transformers/all-mpnet-base-v2', device = "cuda:0")
model_ar = SentenceTransformer('sentence-transformers/paraphrase-multilingual-mpnet-base-v2', device = "cuda:0")

logger = logger
index_dict = {"question_ar":-1, "question_en":-1, "answer_ar":-1, "answer_en":-1}

################ empty collection

def empty_collection(collection_name):
	name_list = []
	if not len(collection_name):
		tmp = client.list_collections()
		for i in tmp:
			client.delete_collection(i.name)
			name_list.append(i.name)
		return name_list
	else:
		for i in collection_name:
			try:
				client.delete_collection(i)
				name_list.append(i)
			except:
				pass
		return name_list
		
################ read excel
def process_excel(files=None, file_path=None):
	if files:
		wb = xlrd.open_workbook(file_contents=files.read())
	elif file_path:
		wb = xlrd.open_workbook(file_path)
	data_sheet = wb.sheet_by_index(0) # get first sheet
	maxRows = data_sheet.nrows  # row num
	maxColumns = data_sheet.ncols  # column num
	# print(f"maxRows:{maxRows} |  maxCols:{maxColumns}")
	# print(f"test: {data_sheet.cell(0,1).value.lower()}")
	for i in range(0, maxColumns):
		# print(f"i_num:{i}")
		index_dict[data_sheet.cell(0,i).value.lower()] = i

	if index_dict['question_ar'] == -1:
		del index_dict['question_ar']
		del index_dict['answer_ar']
	elif index_dict['question_en'] == -1:
		del index_dict['question_en']
		del index_dict['answer_en']

	all_data = []
	for x in [("question_ar", "answer_ar"), ("question_en", "answer_en")]:
		embedding_candidates = []
		documents = []
		if x[0] in index_dict:
			question_candidates = []
			answer_candidates = []
			for i in range(1, maxRows):  # skip the first row data(line index)
				question = data_sheet.cell(i, index_dict[x[0]]).value
				answer = data_sheet.cell(i, index_dict[x[1]]).value
				question_candidates.append(question)
				answer_candidates.append(answer)
				documents.append(f"{question}|__|{answer}")
			embedding_candidates.append((question_candidates, answer_candidates))
			# print(f"test: {x[0]}")
			# exit()
			all_data.append((embedding_candidates, documents, "ar" if "ar" in x[0] else "en"))
	return all_data

################ embedding the data and store in the vector DB

def embedding_store(all_data, token_name):
	# check chromadb
	## TODO insert stead of add
	collection = client.get_or_create_collection(name=token_name, metadata={"hnsw:space": "cosine"})

	documents_list = []
	metadata_list = []
	id_list = []
	embedding_list = []
	for i in all_data:
		if i[2] == 'ar':
			question_embedding = model_ar.encode(i[0][0][0]).tolist()
			answer_embedding = model_ar.encode(i[0][0][1]).tolist()
		else:
			question_embedding = model_ar.encode(i[0][0][0]).tolist()
			answer_embedding = model_ar.encode(i[0][0][1]).tolist()
		for num, j in enumerate(i[1]):
			documents_list.append(j)
			documents_list.append(j)
			embedding_list.append(question_embedding[num])
			embedding_list.append(answer_embedding[num])
			id_list.append(f"Q|__|{token_name}|__|{num}|__|{i[2]}")
			id_list.append(f"A|__|{token_name}|__|{num}|__|{i[2]}")
			metadata_list.append({"source": token_name, "type": "Q", "lang":i[2]})
			metadata_list.append({"source": token_name, "type": "A", "lang":i[2]})

		collection.add(documents=documents_list, embeddings=embedding_list, metadatas=metadata_list, ids=id_list)
	
	return "Success"

def qa_pairs_search(question, token_name):
	try:
		collection = client.get_collection(name=token_name)
	except:
		return "Get Collection ERROR!"
	lang = check_lang_id(question)
	if lang == 'ar':
		question_embedding = model_ar.encode([question])[0].tolist()
	else:
		question_embedding = model_en.encode([question])[0].tolist()
	
	qa_pairs_candidates = collection.query(query_embeddings=[question_embedding], n_results=1, where={"type": "Q"})['documents'][0][0]
	# print(f"test : {qa_pairs_candidates}")
	# test : [["test is good?|__|Yes, it's good!!!", "test is good?|__|NO, it's good!!!"]]
	question_res = qa_pairs_candidates.split('|__|')[0]
	answer_res = qa_pairs_candidates.split('|__|')[1]

	question_res_embedding = model_en.encode([question_res])[0].tolist()

	score = np.dot(question_res_embedding,question_embedding)/(norm(question_res_embedding)*norm(question_embedding))[0]


	return {"Question": question_res, "Answer": answer_res, "Score": score}

		

################ check lang

langid.set_languages(['en', 'ar'])
def check_lang_id(text):
	if langid.rank(text)[0][0] == 'ar':
		return 'ar'
	elif langid.rank(text)[0][0] == 'en':
		return 'en'

'''
check_lang_id("hello, how are you?")

'en'

'''


################ en embedding

def text_embedding_en(sentence):
	try:
		return model_en.encode([sentence])[0].tolist()
	except:
		return None

'''
text_embedding_en("hello, how are you?")

[0.019096773117780685, 0.03446512296795845, 0.09162800759077072, 0.07016528397798538, -0.02994656376540661, -0.0841913

'''

############## arabic embedding

def text_embedding_ar(sentence):
	try:
		return model_ar.encode([sentence])[0].tolist()
	except:
		return None

'''
text_embedding_ar(u"مرحبا، كيف حالك؟")

[0.031213773414492607, 0.040902893990278244, -0.0034165638498961926, 0.04241234436631203,
'''

############## google excel download

def get_confirm_token(response):
    for key, value in response.cookies.items():
        if key.startswith('download_warning'):
            return value
    return None

def save_response_content(response, destination):
    CHUNK_SIZE = 32768
    with open(destination, "wb") as f:
        for chunk in response.iter_content(CHUNK_SIZE):
            if chunk: # filter out keep-alive new chunks
                f.write(chunk)

def download_file_from_google_drive(
	id, 
	destination,
	):
    URL = "https://docs.google.com/uc?export=download"
    session = requests.Session()
    response = session.get(URL, params = { 'id' : id }, stream = True)
    token = get_confirm_token(response)
    if token:
        params = { 'id' : id, 'confirm' : token }
        response = session.get(URL, params = params, stream = True)
    save_response_content(response, destination)


'''

download_file_from_google_drive(
	id = '1SadGNSpLDt4ZuRD6N4xwCAPmJvlfTrm3', 
	destination = qa_pair_excel,
	)

'''

################### redo embeddings

'''
https://github.com/nsadawi/Download-Large-File-From-Google-Drive-Using-Python/blob/master/Download-Large-File-from-Google-Drive.ipynb
'''

def redo_embedding(
	file_id = '1SadGNSpLDt4ZuRD6N4xwCAPmJvlfTrm3',
	question_answer_pair_path = './embeddings/QuestionAnsweringData.xlsx',
	):
	print('do the embedding of the questions')
	############### 
	print('re-downloading the excel of qa pairs.')
	download_file_from_google_drive(
		file_id, 
		question_answer_pair_path,
		)
	############### english
	qa_pairs = pd.read_excel(question_answer_pair_path)
	qa_pairs = qa_pairs[[
		'question',
		'answer',
		]]
	qa_pairs = qa_pairs[qa_pairs['question'].notnull()].drop_duplicates()
	qa_pairs = qa_pairs[qa_pairs['answer'].notnull()].drop_duplicates()

	all_embedding = qa_pairs.copy()
	all_embedding['question_embedding'] = all_embedding['question'].apply(text_embedding_en)
	all_embedding['answer_embedding'] = all_embedding['answer'].apply(text_embedding_en)
	all_embedding.to_json(
		all_embeddings_en_json,
		lines = True,
		orient = 'records',
		)

	###
	print(f'english question embeddings')

	question_embedding = qa_pairs.copy()
	question_embedding['question_embedding'] = question_embedding['question'].apply(text_embedding_en)
	question_embedding.to_json(
		question_embeddings_en_json,
		lines = True,
		orient = 'records',
		)
	##
	print(f'english answer embeddings')
	answer_embedding = qa_pairs.copy()
	answer_embedding['answer_embedding'] = answer_embedding['answer'].apply(text_embedding_en)
	answer_embedding.to_json(
		answer_embeddings_en_json,
		lines = True,
		orient = 'records',
		)

	############### arabic
	logger.info(f'arabic all embeddings')
	#question_ar	answer_ar
	qa_pairs = pd.read_excel(question_answer_pair_path)
	qa_pairs = qa_pairs[[
		'question_ar',
		'answer_ar',
		]]
	qa_pairs = qa_pairs[qa_pairs['question_ar'].notnull()].drop_duplicates()
	qa_pairs = qa_pairs[qa_pairs['answer_ar'].notnull()].drop_duplicates()

	all_embedding_ar = qa_pairs.copy()
	all_embedding_ar['question_embedding'] = all_embedding_ar['question_ar'].apply(text_embedding_ar)
	all_embedding_ar['answer_embedding'] = all_embedding_ar['answer_ar'].apply(text_embedding_ar)
	all_embedding_ar.to_json(
		all_embeddings_ar_json,
		lines = True,
		orient = 'records',

		)

	###
	logger.info(f'arabic question embeddings')

	question_embedding = qa_pairs.copy()
	question_embedding['question_embedding'] = question_embedding['question_ar'].apply(text_embedding_ar)
	question_embedding.to_json(
		question_embeddings_ar_json,
		lines = True,
		orient = 'records',
		)
	##
	print(f'arabic answer embeddings')
	answer_embedding = qa_pairs.copy()
	answer_embedding['answer_embedding'] = answer_embedding['answer_ar'].apply(text_embedding_ar)
	answer_embedding.to_json(
		answer_embeddings_ar_json,
		lines = True,
		orient = 'records',
		)
	###
	logger.info("Clear session!")
	return len(qa_pairs)

'''

from embedding_util import *

redo_embedding(
	file_id = '1SadGNSpLDt4ZuRD6N4xwCAPmJvlfTrm3',
	question_answer_pair_path = '/embeddings/QuestionAnsweringData.xlsx',
	)

'''

############ similarity
def similarity_embedding(
	query_question_embedding,
	question_embedding,
	):
	try:
		return np.dot(
			query_question_embedding,
			np.array(question_embedding),
		)
	except:
		return None   

def semantic_search_together(
	query_question,
	embeddings,
	embedding_field,
	returned_fields,
	language = 'en',
	threshold = 0.9,
	k = 10,
	):
	### embedding of the query 
	if language == 'en':
		query_question_embedding = text_embedding_en(query_question)	
	else:
		logger.info("Use ar embedding!")
		query_question_embedding = text_embedding_ar(query_question)

	### scoring
	embeddings_score = []

	# logger.info(f"embeddings[embedding_field]")
	if embedding_field == 'answer_embedding':
		only_embeddings = np.array(embeddings[1])
	else:
		logger.info("Use question embedding!")
		only_embeddings = np.array(embeddings[0])
	logger.info(f'ques embedding: {query_question_embedding[0]}')
	logger.info(f'first embedding: {only_embeddings[0][0]}')


	# (A,B)/(norm(A, axis=1)*norm(B))
	score = np.dot(only_embeddings, query_question_embedding) / (norm(only_embeddings, axis=1) * norm(query_question_embedding))

	# if the score not meet the threshold, use <ques + ans> bi search.
	if max(score) > threshold:
		arg_score = np.argsort(-score)
		score_result = {'score': score[arg_score[0]]}
		for j in returned_fields:
			if language == 'ar':
				j += '_ar'
			score_result[j] = embeddings[2][0][j]
		embeddings_score.append(score_result)
		return embeddings_score
	else:

		arg_score = np.argsort(-score)
		for i in arg_score[0:k]:
			score_result = {'score': score[i]}
			for j in returned_fields:
				if language == 'ar':
					j += '_ar'
				score_result[j] = embeddings[2][i][j]
			embeddings_score.append(score_result)
		
		only_embeddings = np.array(embeddings[1])
		score = np.dot(only_embeddings, query_question_embedding) / (norm(only_embeddings, axis=1) * norm(query_question_embedding))
		arg_score = np.argsort(-score)
		for i in arg_score[0:k]:
			score_result = {'score': score[i]}
			for j in returned_fields:
				if language == 'ar':
					j += '_ar'
				score_result[j] = embeddings[2][i][j]
			embeddings_score.append(score_result)
		
		return embeddings_score


	# logger.info(f"scores: {score[arg_score[0]]} | {score[arg_score[1]]} | {score[arg_score[2]]}")
	# logger.info(f"max_score: {max(score)}")

	# for i in arg_score[0:k]:
	# 	score_result = {'score': score[i]}
	# 	for j in returned_fields:
	# 		if language == 'ar':
	# 			j += '_ar'
	# 		score_result[j] = embeddings[2][i][j]
	# 	embeddings_score.append(score_result)
	# return embeddings_score

def semantic_search(
	query_question,
	embeddings,
	embedding_field,
	returned_fields,
	language = 'en',
	k = 10,
	):
	### embedding of the query 
	if language == 'en':
		query_question_embedding = text_embedding_en(query_question)	
	else:
		query_question_embedding = text_embedding_ar(query_question)	
	### scoring
	embeddings_score = []
	for r in embeddings:
		try:
			score = similarity_embedding(
				query_question_embedding, 
				r[embedding_field],
				)
			if score is not None:
				score_result = {'score':score}
				for f in returned_fields:
					score_result[f] = r[f]
				embeddings_score.append(score_result)
		except:
			pass
	### return top k 
	embeddings_score = sorted(embeddings_score, 
		key= lambda x: x['score'],
		reverse = True)
	return embeddings_score[0:k]

'''

question_embeddings_en = pd.read_json(
	question_embeddings_en_json,
	lines = True,
	orient = 'records',
	).to_dict('records')

results = semantic_search(
	query_question = 'What is visual pollution? ',
	embeddings = question_embeddings_en,
	embedding_field = 'question_embedding',
	returned_fields = ['question', 'answer', ],
	language = 'en',
	k = 3,
	)

[{'score': 1.0000000730223275, 'question': 'What is visual pollution?', 'answer': 'Visual pollution is a set of visual elements as defined in the national plan for visual pollution visible in the infrastructure or urban fabric that have worn out their original state or violate the regulations and instructions governing this in a way that affects the appearance of the city due to negligence in inspection, bypassing the various parties (e.g., residents, private companies, and others), and usually producing visual distortion in addition to the irregular diligence of the owners of private property.'},


###

answer_embeddings_en = pd.read_json(
	answer_embeddings_en_json,
	lines = True,
	orient = 'records',
	).to_dict('records')

results = semantic_search(
	query_question = 'What is visual pollution? ',
	embeddings = answer_embeddings_en,
	embedding_field = 'answer_embedding',
	returned_fields = ['question', 'answer', ],
	language = 'en',
	k = 3,
	)


[{'score': 0.8462431965194682, 'question': 'What is visual pollution?', 'answer': 'Visual pollution is a set of visual elements as defined in the national plan for visual pollution visible in the infrastructure or urban fabric that have worn out their original state or violate the regulations and instructions governing this in a way that affects the appearance of the city due to negligence in inspection, bypassing the various parties (e.g., residents, private companies, and others), and usually producing visual distortion in addition to the irregular diligence of the owners of private property.'}, 

###

question_embeddings_ar = pd.read_json(
	question_embeddings_ar_json,
	lines = True,
	orient = 'records',
	).to_dict('records')

results = semantic_search(
	query_question = f"""
	لماذا تساهم المركبات المتضررة في تلوث البصر وما هي الحلول التي يقترحها الخطة؟
	""",
	embeddings = question_embeddings_ar,
	embedding_field = 'question_embedding',
	returned_fields = ['question_ar', 'answer_ar',],
	language = 'ar',
	k = 3,
	)

[{'score': 0.9999999960760387, 'question_ar': 'لماذا تساهم المركبات المتضررة في تلوث البصر وما هي الحلول التي يقترحها الخطة؟', 'answer_ar': 'تؤدي المركبات المتضررة في الشوارع إلى تصور الإهمال وتقليل المساحة العامة. الأسباب الرئيسية لهذا هو إهمال أصحاب المركبات لإزالة مركباتهم بسبب التكلفة وعدم الوعي. تقتضي الخطة معالجة هذا الأمر من خلال تحديد النطاقات والاتفاقات على مستوى الخدمة (SLA) مع سلطات المرور، وزيادة الغرامات، وزيادة الوعي المجتمعي، وتوضيح المبادئ التوجيهية لإزالة المركبات، وتطوير نظام خصم، وتطبيق عواقب تصاعد عدم الامتثال.'},


###


answer_embeddings_ar = pd.read_json(
	answer_embeddings_ar_json,
	lines = True,
	orient = 'records',
	).to_dict('records')

results = semantic_search(
	query_question = f"""
	لماذا تساهم المركبات المتضررة في تلوث البصر وما هي الحلول التي يقترحها الخطة؟
	""",
	embeddings = answer_embeddings_ar,
	embedding_field = 'answer_embedding',
	returned_fields = ['question_ar', 'answer_ar',],
	language = 'ar',
	k = 3,
	)

[{'score': 0.8927517313920555, 'question_ar': 'ما العوامل التي تسهم في تلوث البصر من حيث التلفات في الرصيف والحفر في الطرق والشوارع، وما هي المبادرات المقترحة؟', 'answer_ar': 'تساهم الأرصفة والحفر المتضررة في التلوث البصري بسبب عدم وجود صيانة منتظمة أو ميزانية بنية تحتية غير كافية أو إدارة غير فعالة. على الرغم من أن الخطة لا تقترح صراحة حلول لهذه القضايا ، إلا أنها قد توصي بتنفيذ جدول أعمال الصيانة المنتظمة وزيادة ميزانية البنية التحتية لإصلاح الطرق وتحسين ممارسات الإدارة.'}, 

'''

###################


###############embedding_util.py#################