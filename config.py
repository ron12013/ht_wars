import os

DATA_DIR = '../data/'

try:
    from config_local import *
except ImportError:
    pass

# Random seed to synchronize tweet pair creation between models
TWEET_PAIR_LABEL_RANDOM_SEED = 'hello world'

# GloVe embedding dataset path
WORD_VECTORS_FILE_PATH = os.path.join(DATA_DIR, 'glove.twitter.27B/glove.twitter.27B.200d.txt')

# Main #HashtagWars dataset paths
SEMEVAL_HUMOR_TRAIN_DIR = os.path.join(DATA_DIR, 'train_dir/train_data/')
SEMEVAL_HUMOR_TRIAL_DIR = os.path.join(DATA_DIR, 'trial_dir/trial_data/')
SEMEVAL_HUMOR_EVAL_DIR = os.path.join(DATA_DIR, 'evaluation_dir/evaluation_data/')

SEMEVAL_EVAL_PREDICTIONS = os.path.join(DATA_DIR, 'evaluation_dir/evaluation_predict/')

# Character-to-phoneme model paths
CMU_SYMBOLS_FILE_PATH = os.path.join(DATA_DIR, 'cmudict-0.7b.symbols.txt')
CMU_DICTIONARY_FILE_PATH = os.path.join(DATA_DIR, 'cmudict-0.7b.txt')

CMU_CHAR_TO_INDEX_FILE_PATH = os.path.join(DATA_DIR, 'cmu_char_to_index.cpkl')
CMU_PHONE_TO_INDEX_FILE_PATH = os.path.join(DATA_DIR, 'cmu_phone_to_index.cpkl')
CMU_NP_WORDS_FILE_PATH = os.path.join(DATA_DIR, 'cmu_words.npy')
CMU_NP_PRONUNCIATIONS_FILE_PATH = os.path.join(DATA_DIR, 'cmu_pronunciations.npy')

CHAR_2_PHONE_MODEL_DIR = os.path.join(DATA_DIR, 'char_2_phone_models/')

# Embedding humor model paths for both models, embedding model only, and character model only.
EMB_CHAR_HUMOR_MODEL_DIR = os.path.join(DATA_DIR, 'humor_models/')
EMB_HUMOR_MODEL_DIR = os.path.join(DATA_DIR, 'emb-only_humor_models/')
CHAR_HUMOR_MODEL_DIR = os.path.join(DATA_DIR, 'char-only_humor_models/')

# Prediction input for ensemble model (training)
HUMOR_TRAIN_TWEET_PAIR_PREDICTIONS = os.path.join(DATA_DIR, 'train_tweet_pair_predictions.cpkl')
HUMOR_TRAIN_PREDICTION_HASHTAGS = os.path.join(DATA_DIR, 'train_prediction_hashtags')
HUMOR_TRAIN_PREDICTION_LABELS = os.path.join(DATA_DIR, 'train_prediction_labels')

# Prediction input for ensemble model (trial)
HUMOR_TRIAL_TWEET_PAIR_PREDICTIONS = os.path.join(DATA_DIR, 'trial_tweet_pair_predictions.cpkl')
HUMOR_TRIAL_PREDICTION_HASHTAGS = os.path.join(DATA_DIR, 'trial_prediction_hashtags.cpkl')
HUMOR_TRIAL_PREDICTION_LABELS = os.path.join(DATA_DIR, 'trial_prediction_labels.cpkl')
HUMOR_TRIAL_PREDICTION_FIRST_TWEET_IDS = os.path.join(DATA_DIR, 'trial_prediction_first_tweet_ids.cpkl')
HUMOR_TRIAL_PREDICTION_SECOND_TWEET_IDS = os.path.join(DATA_DIR, 'trial_prediction_second_tweet_ids.cpkl')

# Prediction input for ensemble model (evaluation)
HUMOR_EVAL_TWEET_PAIR_PREDICTIONS = os.path.join(DATA_DIR, 'eval_tweet_pair_predictions.cpkl')
HUMOR_EVAL_PREDICTION_HASHTAGS = os.path.join(DATA_DIR, 'eval_prediction_hashtags.cpkl')
HUMOR_EVAL_PREDICTION_LABELS = os.path.join(DATA_DIR, 'eval_prediction_labels.cpkl')
HUMOR_EVAL_PREDICTION_FIRST_TWEET_IDS = os.path.join(DATA_DIR, 'eval_prediction_first_tweet_ids.cpkl')
HUMOR_EVAL_PREDICTION_SECOND_TWEET_IDS = os.path.join(DATA_DIR, 'eval_prediction_second_tweet_ids.cpkl')

HUMOR_TRAIN_TWEET_PAIR_CHAR_DIR = os.path.join(DATA_DIR, 'train_numpy_tweet_pairs/')
HUMOR_TRIAL_TWEET_PAIR_CHAR_DIR = os.path.join(DATA_DIR, 'trial_numpy_tweet_pairs/')
HUMOR_CHAR_TO_INDEX_FILE_PATH = os.path.join(DATA_DIR, 'humor_char_to_index.cpkl')
HUMOR_INDEX_TO_WORD_FILE_PATH = os.path.join(DATA_DIR, 'humor_index_to_word.cpkl')
HUMOR_WORD_TO_GLOVE_FILE_PATH = os.path.join(DATA_DIR, 'humor_word_to_glove.cpkl')
HUMOR_WORD_TO_PHONETIC_FILE_PATH = os.path.join(DATA_DIR, 'humor_word_to_phonetic.cpkl')

HUMOR_TRAIN_TWEET_PAIR_EMBEDDING_DIR = os.path.join(DATA_DIR, 'training_tweet_pair_embeddings/')
HUMOR_TRIAL_TWEET_PAIR_EMBEDDING_DIR = os.path.join(DATA_DIR, 'trial_tweet_pair_embeddings/')

# Boost tree humor model paths
# BOOST_TREE_TWEET_PAIR_TRAINING_DIR = os.path.join(DATA_DIR, 'training_tweet_pair_tree_data/')
# BOOST_TREE_TWEET_PAIR_TESTING_DIR = os.path.join(DATA_DIR, 'testing_tweet_pair_tree_data/')

# Boost tree model data
BOOST_TREE_TWEET_PAIR_TRAIN_DIR = os.path.join(DATA_DIR, 'tree_train_data/')
BOOST_TREE_TWEET_PAIR_TRIAL_DIR = os.path.join(DATA_DIR, 'tree_trial/')
BOOST_TREE_TWEET_PAIR_EVAL_DIR = os.path.join(DATA_DIR, 'tree_eval_data/')

BOOST_TREE_TRAIN_TWEET_PAIR_PREDICTIONS = os.path.join(DATA_DIR, 'boost_tree_train_tweet_pair_predictions.cpkl')
BOOST_TREE_TRIAL_TWEET_PAIR_PREDICTIONS = os.path.join(DATA_DIR, 'boost_tree_trial_tweet_pair_predictions.cpkl')
BOOST_TREE_EVAL_TWEET_PAIR_PREDICTIONS = os.path.join(DATA_DIR, 'boost_tree_eval_tweet_pair_predictions.cpkl')

BOOST_TREE_MODEL_FILE_PATH = os.path.join(DATA_DIR, 'boost_tree_model.bin')


# PARAMETERS
HUMOR_MAX_WORDS_IN_TWEET = 20  # All winning tweets are under 30 words long
HUMOR_MAX_WORDS_IN_HASHTAG = 8
GLOVE_EMB_SIZE = 200
TWEET_SIZE = 140
PHONETIC_EMB_SIZE = 200

# Mongo for Sacred's observer
MONGO_ADDRESS = '127.0.0.1:27018'

ENSEMBLE_DIR = os.path.join(DATA_DIR, 'ensemble/')
ENSEMBLE_EVAL_PREDICTIONS_DIR = os.path.join(DATA_DIR, 'ensemble_predictions/')
