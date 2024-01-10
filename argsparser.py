###########
import argparse
from envdefault import EnvDefault

def prepare_args():
	parser = argparse.ArgumentParser(description="")
	parser.add_argument('--activate_detection', action=EnvDefault, envvar='ACTIVATE_DETECTION', type=bool, default=True)
	parser.add_argument('--host', action=EnvDefault, envvar='HOST', type=str, default='0.0.0.0')
	parser.add_argument('--port', action=EnvDefault, envvar='PORT', type=int, default=9000)
	parser.add_argument('--embeddings', action=EnvDefault, envvar='EMBEDDINGS', type=str, default='question_embedding')
	parser.add_argument('--threshold', action=EnvDefault, envvar='THRESHOLD', type=float, default=0.9)
	args = parser.parse_args()
	return args
###########
