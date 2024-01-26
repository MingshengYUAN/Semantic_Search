import time
import re 
import os
import requests
import logging
import argparse
import configparser
import numpy as np
from datetime import timedelta
from flask import Flask, request
from flasgger import Swagger
from flasgger.utils import swag_from
from swagger_template import template
from log_info import *
import xlrd
from share_args import ShareArgs

parser = argparse.ArgumentParser()
parser.add_argument('--port', default=3010)
parser.add_argument('--log_path', default='./log/semantic_search_dev.log')
parser.add_argument('--config_path', default='./config/semantic_search_dev.ini')
args = parser.parse_args()
args_default = vars(args)
ShareArgs.update(args_default)

from embedding_util import process_excel, embedding_store, qa_pairs_search, empty_collection, download_file_from_google_drive, read_qa_pairs

config_path = args.config_path
conf = configparser.ConfigParser()
conf.read(config_path, encoding='utf-8')

app = Flask(__name__)
swagger = Swagger(app, template=template)

fh = logging.FileHandler(args.log_path)
fh.setLevel(logging.INFO)

formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
fh.setFormatter(formatter)
console_handler.setFormatter(formatter)

logger.addHandler(console_handler)
logger.addHandler(fh)

try:
    os.system(f"mkdir uploaded/")
    os.system(f"mkdir uploaded/{conf['application']['name']}")
    os.system(f"mkdir uploaded/{conf['application']['name']}/google_docs")
    os.system(f"mkdir uploaded/{conf['application']['name']}/excel")
except:
	pass

#####################

@app.route('/get_qa_pairs', methods=['POST'])
def get_qa_pairs():
    start = time.time()
    token_name = request.form.get('token_name')
    logger.info(f"Load {token_name} existed qa_pairs!")

    response = read_qa_pairs(token_name)
    return {"en_qa_list": response['en_list'], "ar_qa_list": response['ar_list'], "status": "success", "running_time": float(time.time() - start)}

#####################

@app.route('/upload_qa_pairs', methods=['POST'])
def upload_qa_pairs():
    start = time.time()
    uploaded_file = request.files['file']
    token_name = request.form.get('token_name')
    logger.info(f"Upload file: {uploaded_file.filename} | Token name: {token_name}")
    uploaded_file.save(f"./uploaded/{conf['application']['name']}/excel/{uploaded_file.filename}")
    try:
        file_type = uploaded_file.filename.split('.')[1]
    except:
        return "Check file type ERROR!"
    if file_type != 'xlsx':

        return "Please upload EXCEL file!"

    all_data = process_excel(files=uploaded_file)
    embedding_store(all_data, token_name)

    return {"response": "Success", "status":"success", "running_time": float(time.time() - start)}

@app.route('/qa_search', methods=['POST'])
def qa_search():
    start = time.time()
    question = request.form.get('question')
    token_name = request.form.get('token_name')

    logger.info(f"Question: {question}")
    logger.info(f"Select DB: {token_name}")

    result = qa_pairs_search(question, token_name)
    try:
        if result == "Get Collection ERROR!":
            return {"response": "Get Collection ERROR!", "reference":'', "status":'FAIL', "running_time": float(time.time() - start)}
    except:
        pass
    try:
        threshold_score = request.form.get("threshold_score")
        if result['Score'] >= threshold_score:
            logger.info(f"Meet Threshold! Response: {result['Answer']} | Score: {result['Score']}")
            return {"response": result['Answer'], "reference":result['reference_res'], "status":'success', "running_time": float(time.time() - start)}
        else:
            logger.info(f"NOT Meet Threshold! Original Response: {result['Answer']} | Score: {result['Score']}")
            return {"response": "Score not meet the threshold", "reference":'', "status":'success', "running_time": float(time.time() - start)}
    except:
        pass

    logger.info(f"No Threshold! Response: {result['Answer']} | Score: {result['Score']}")
    return {"response": result['Answer'], "reference":result['reference_res'], "score": result['Score'], "status":'success', "running_time": float(time.time() - start)}

@app.route('/empty_collection', methods=['POST'])
def do_empty_collection():
    start = time.time()
    data = request.get_json()
    collection_name = data['collection_name']
    logger.info(f"Request Delete collection : {collection_name}")
    logger.info(f"Succeed Delete collection : {name_list}")
    
    name_list = empty_collection(collection_name)
    return {"response": f"Success delete following collection : {name_list}", "status":'success', "running_time": float(time.time() - start)}

@app.route('/upload_google_qa_pairs')
def upload_google_qa_pairs():
    start = time.time()
    file_id = request.form.get('file_id', default='1SadGNSpLDt4ZuRD6N4xwCAPmJvlfTrm3', type=str)
    token_name = request.form.get('token_name')
    question_answer_pair_path = f"./uploaded/{conf['application']['name']}/google_docs/{file_id}.xlsx",
    logger.info(f"Download from Google: ./uploaded/{conf['application']['name']}/google_docs/{file_id}.xlsx")
    download_file_from_google_drive(file_id, question_answer_pair_path)
    
    all_data = process_excel(file_path=question_answer_pair_path)
    embedding_store(all_data, file_id)

    return {"response": "Success", "status":"success", "running_time": float(time.time() - start)}
#######################
if __name__=="__main__":
    app.run(port=args.port, host="0.0.0.0", debug=False)