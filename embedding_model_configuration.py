import logging

########embedding_model_configuration.py########

qa_pair_excel = './embeddings/QuestionAnsweringData.xlsx'
question_embeddings_en_json = './embeddings/question_embeddings_en.json'
answer_embeddings_en_json = './embeddings/answer_embeddings_en.json'
question_embeddings_ar_json = './embeddings/question_embeddings_ar.json'
answer_embeddings_ar_json = './embeddings/answer_embeddings_ar.json'

all_embeddings_en_json = './embeddings/all_embeddings_en.json'
all_embeddings_ar_json = './embeddings/all_embeddings_ar.json'


logger = logging.getLogger('root')
logger.setLevel(logging.INFO)

# 创建FileHandler对象
fh = logging.FileHandler('semantic_embedding.log')
fh.setLevel(logging.INFO)

#
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.INFO)

# 创建Formatter对象
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
fh.setFormatter(formatter)
console_handler.setFormatter(formatter)

# 将FileHandler对象添加到Logger对象中
logger.addHandler(fh)
logger.addHandler(console_handler)

########embedding_model_configuration.py########