##############server_path.py##############
import time
import logging
import argsparser
import pandas as pd
import numpy as np
import requests
import re 
from flask import *
from flask_restx import *
from flask_session import *
from embedding_model_configuration import *
from embedding_util import *


################ check readed all embedding

def check_session(lang):
	# session.clear()
	if lang == 'en':
		## if not loaded the embedding then load it
		if not session.get("all_embeddings_en"):
			print(f'loading all_embeddings_en')
			session["all_embeddings_en"] = pd.read_json(
				all_embeddings_en_json,
				lines = True,
				orient = 'records',
				).to_dict('records')
		if not session.get("just_ques_embeddings_en"):
			print(f'loading just_ques_embeddings_en')
			embedding_list = []
			for i in session["all_embeddings_en"]:
				embedding_list.append(i['question_embedding'])
			session["just_ques_embeddings_en"] = embedding_list
		if not session.get("just_ans_embeddings_en"):
			print(f'loading just_ans_embeddings_en')
			embedding_list = []
			for i in session["all_embeddings_en"]:
				embedding_list.append(i['answer_embedding'])
			session["just_ans_embeddings_en"] = embedding_list

	elif lang == 'ar':
		## if not loaded the embedding then load it
		if not session.get("all_embeddings_ar"):
			print(f'loading all_embeddings_ar')
			session["all_embeddings_ar"] = pd.read_json(
				all_embeddings_ar_json,
				lines = True,
				orient = 'records',
				).to_dict('records')
		if not session.get("just_ques_embeddings_ar"):
			print(f'loading just_ques_embeddings_ar')
			embedding_list = []
			for i in session["all_embeddings_ar"]:
				embedding_list.append(i['question_embedding'])
			session["just_ques_embeddings_ar"] = embedding_list
		if not session.get("just_ans_embeddings_ar"):
			print(f'loading just_ans_embeddings_ar')
			embedding_list = []
			for i in session["all_embeddings_ar"]:
				embedding_list.append(i['answer_embedding'])
			session["just_ans_embeddings_ar"] = embedding_list

###########

ns = Namespace(
	'momrah_qa_semantic_search', 
	description='MOMRAH QA pairs search',
	)

args_global = argsparser.prepare_args()

####################################################

semantic_search_api_parser = ns.parser()
semantic_search_api_parser.add_argument('query', type=str, location='json')
# semantic_search_api_parser.add_argument('embedding_field', type=str, location='json', default='answer_embedding', required=False)

semantic_search_api_input = ns.model(
	'semantic_search_api', 
		{
			'query': fields.String(example = u"What is visual pollution?")
		}
	)

@ns.route('/semantic_search')
class semantic_search_api(Resource):
	def __init__(self, *args, **kwargs):
		super(semantic_search_api, self).__init__(*args, **kwargs)
	@ns.expect(semantic_search_api_input)
	def post(self):		
		start = time.time()
		# try:			
		args = semantic_search_api_parser.parse_args()		
		logger.info(f"Input : {args['query']}")
		output = {}
		lang_id = check_lang_id(args['query'])
		logger.info(f"Lang_id : {lang_id}")
		check_session(lang_id)
		# if lang_id == 'en':
		# 	embeddings_name = ['just_ques_embeddings_en', 'just_ans_embeddings_en']
		# else:
		# 	embeddings_name = ['just_ques_embeddings_ar', 'just_ans_embeddings_ar']
		# print(session.get('just_ques_embeddings_en')[0])

		# print(f"check <just_ques_embeddings_ar>: {session.get('just_ques_embeddings_ar')[0][0]}")
		if lang_id == 'en':
			output['results'] = semantic_search_together(
				query_question = args['query'],
				embeddings = [session.get('just_ques_embeddings_en'), session.get('just_ans_embeddings_en'), session.get('all_embeddings_en')],
				embedding_field = args_global.embeddings,
				returned_fields = ['question', 'answer', ],
				language = lang_id,
				threshold = args_global.threshold,
				k = 10,
				)
		else:
			logger.info("Server into ar part!")
			output['results'] = semantic_search_together(
				query_question = args['query'],
				embeddings = [session.get('just_ques_embeddings_ar'), session.get('just_ans_embeddings_ar'), session.get('all_embeddings_ar')],
				embedding_field = args_global.embeddings,
				returned_fields = ['question', 'answer', ],
				language = lang_id,
				k = 10,
				)
		output['status'] = 'success'
		output['running_time'] = float(time.time()- start)
		return output, 200
		# except Exception as e:
		# 	output = {}
		# 	output['status'] = str(e)
		# 	output['running_time'] = float(time.time()- start)
		# 	return output

####################################################

question_search_en_parser = ns.parser()
question_search_en_parser.add_argument('query', type=str, location='json')
question_search_en_inputs = ns.model(
	'question_search_en', 
		{
			'query': fields.String(example = u"What is visual pollution?")
		}
	)

@ns.route('/question_search_en')
class question_search_en_api(Resource):
	def __init__(self, *args, **kwargs):
		super(question_search_en_api, self).__init__(*args, **kwargs)
	@ns.expect(question_search_en_inputs)
	def post(self):		
		start = time.time()
		try:			
			args = question_search_en_parser.parse_args()		

			output = {}

			## if not loaded the embedding then load it
			if not session.get("question_embeddings_en"):
				print(f'loading question_embeddings_en')
				session["question_embeddings_en"] = pd.read_json(
					question_embeddings_en_json,
					lines = True,
					orient = 'records',
					).to_dict('records')

			output['results'] = semantic_search(
				query_question = args['query'],
				embeddings = session.get("question_embeddings_en"),
				embedding_field = 'question_embedding',
				returned_fields = ['question', 'answer', ],
				language = 'en',
				k = 10,
				)
			output['status'] = 'success'
			output['running_time'] = float(time.time()- start)
			return output, 200
		except Exception as e:
			output = {}
			output['status'] = str(e)
			output['running_time'] = float(time.time()- start)
			return output

####################################################

answer_search_en_parser = ns.parser()
answer_search_en_parser.add_argument('query', type=str, location='json')
answer_search_en_inputs = ns.model(
	'answer_search_en', 
		{
			'query': fields.String(example = u"What is visual pollution?")
		}
	)

@ns.route('/answer_search_en')
class answer_search_en_api(Resource):
	def __init__(self, *args, **kwargs):
		super(answer_search_en_api, self).__init__(*args, **kwargs)
	@ns.expect(answer_search_en_inputs)
	def post(self):		
		start = time.time()
		try:			
			args = answer_search_en_parser.parse_args()		

			output = {}

			## if not loaded the embedding then load it
			if not session.get("answer_embeddings_en"):
				print(f'loading answer_embeddings_en')
				session["answer_embeddings_en"] = pd.read_json(
					answer_embeddings_en_json,
					lines = True,
					orient = 'records',
					).to_dict('records')

			output['results'] = semantic_search(
				query_question = args['query'],
				embeddings = session.get("answer_embeddings_en"),
				embedding_field = 'answer_embedding',
				returned_fields = ['question', 'answer', ],
				language = 'en',
				k = 10,
				)
			output['status'] = 'success'
			output['running_time'] = float(time.time()- start)
			return output, 200
		except Exception as e:
			output = {}
			output['status'] = str(e)
			output['running_time'] = float(time.time()- start)
			return output

####################################################

question_search_ar_parser = ns.parser()
question_search_ar_parser.add_argument('query', type=str, location='json')
question_search_ar_inputs = ns.model(
	'question_search_ar', 
		{
			'query': fields.String(example = u"What is visual pollution?")
		}
	)

@ns.route('/question_search_ar')
class question_search_ar_api(Resource):
	def __init__(self, *args, **kwargs):
		super(question_search_ar_api, self).__init__(*args, **kwargs)
	@ns.expect(question_search_ar_inputs)
	def post(self):		
		start = time.time()
		try:			
			args = question_search_ar_parser.parse_args()		

			output = {}

			## if not loaded the embedding then load it
			if not session.get("question_embeddings_ar"):
				print(f'loading question_embeddings_ar')
				session["question_embeddings_ar"] = pd.read_json(
					question_embeddings_ar_json,
					lines = True,
					orient = 'records',
					).to_dict('records')

			output['results'] = semantic_search(
				query_question = args['query'],
				embeddings = session.get("question_embeddings_ar"),
				embedding_field = 'question_embedding',
				returned_fields = ['question_ar', 'answer_ar', ],
				language = 'ar',
				k = 10,
				)
			output['status'] = 'success'
			output['running_time'] = float(time.time()- start)
			return output, 200
		except Exception as e:
			output = {}
			output['status'] = str(e)
			output['running_time'] = float(time.time()- start)
			return output

####################################################

answer_search_ar_parser = ns.parser()
answer_search_ar_parser.add_argument('query', type=str, location='json')
answer_search_ar_inputs = ns.model(
	'answer_search_ar', 
		{
			'query': fields.String(example = u"What is visual pollution?")
		}
	)

@ns.route('/answer_search_ar')
class answer_search_ar_api(Resource):
	def __init__(self, *args, **kwargs):
		super(answer_search_ar_api, self).__init__(*args, **kwargs)
	@ns.expect(answer_search_ar_inputs)
	def post(self):		
		start = time.time()
		try:			
			args = answer_search_ar_parser.parse_args()		

			output = {}

			## if not loaded the embedding then load it
			if not session.get("answer_embeddings_ar"):
				print(f'loading answer_embeddings_ar')
				session["answer_embeddings_ar"] = pd.read_json(
					answer_embeddings_ar_json,
					lines = True,
					orient = 'records',
					).to_dict('records')

			output['results'] = semantic_search(
				query_question = args['query'],
				embeddings = session.get("answer_embeddings_ar"),
				embedding_field = 'answer_embedding',
				returned_fields = ['question_ar', 'answer_ar', ],
				language = 'ar',
				k = 10,
				)
			output['status'] = 'success'
			output['running_time'] = float(time.time()- start)
			return output, 200
		except Exception as e:
			output = {}
			output['status'] = str(e)
			output['running_time'] = float(time.time()- start)
			return output


####################################################

extraction_parser = ns.parser()
extraction_parser.add_argument(
	'google_file_id', type=str, location='json')
extraction_inputs = ns.model(
	'redo_embedding', 
		{
			'google_file_id': fields.String(example = u"1SadGNSpLDt4ZuRD6N4xwCAPmJvlfTrm3")
		}
	)

@ns.route('/redo_embedding')
class extraction_api(Resource):
	def __init__(self, *args, **kwargs):
		super(extraction_api, self).__init__(*args, **kwargs)
	@ns.expect(extraction_inputs)
	def post(self):		
		start = time.time()
		try:
			session.clear()
			args = extraction_parser.parse_args()		
			if args['google_file_id'] is not None:

				## redo embeddings
				embedded_num = redo_embedding(
				file_id = args['google_file_id'],
				)

				## re-load to the session

				session["all_embeddings_en"] = pd.read_json(
					all_embeddings_en_json,
					lines = True,
					orient = 'records',
					).to_dict('records')

				session["all_embeddings_ar"] = pd.read_json(
					all_embeddings_ar_json,
					lines = True,
					orient = 'records',
					).to_dict('records')

				session["question_embeddings_en"] = pd.read_json(
					question_embeddings_en_json,
					lines = True,
					orient = 'records',
					).to_dict('records')

				session["answer_embeddings_en"] = pd.read_json(
					answer_embeddings_en_json,
					lines = True,
					orient = 'records',
					).to_dict('records')

				session["question_embeddings_ar"] = pd.read_json(
					question_embeddings_ar_json,
					lines = True,
					orient = 'records',
					).to_dict('records')

				session["answer_embeddings_ar"] = pd.read_json(
					answer_embeddings_ar_json,
					lines = True,
					orient = 'records',
					).to_dict('records')
				embedding_list = []
				for i in session["all_embeddings_en"]:
					embedding_list.append(i['question_embedding'])
				session["just_ques_embeddings_en"] = embedding_list
		
				embedding_list = []
				for i in session["all_embeddings_en"]:
					embedding_list.append(i['answer_embedding'])
				session["just_ans_embeddings_en"] = embedding_list

				embedding_list = []
				for i in session["all_embeddings_en"]:
					embedding_list.append(i['question_embedding'])
				session["just_ques_embeddings_ar"] = embedding_list

				embedding_list = []
				for i in session["all_embeddings_en"]:
					embedding_list.append(i['answer_embedding'])
				session["just_ans_embeddings_ar"] = embedding_list

			# print(f"*********  {session.get('just_ques_embeddings_en')[0]}")

			output = {}
			output['qa_pairs'] = embedded_num
			output['status'] = 'success'
			output['running_time'] = float(time.time()- start)
			return output, 200
		except Exception as e:
			output = {}
			output['status'] = str(e)
			output['running_time'] = float(time.time()- start)
			return output

##############server_path.py##############