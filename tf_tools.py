"""David Donahue 2016. This script deals primarily with tensorflow build operations. This script
separates functions that do import tensorflow from those that don't."""
import tensorflow as tf
import numpy as np
import cPickle as pickle
from tools import convert_words_to_indices
from tools import invert_dictionary
from tools import load_hashtag_data
from config import CHAR_2_PHONE_MODEL_DIR

GPU_OPTIONS = tf.GPUOptions(per_process_gpu_memory_fraction=0.7)

MAX_WORD_SIZE = 20
MAX_PRONUNCIATION_SIZE = 20
PHONE_CHAR_EMB_DIM = 30
PHONE_ENCODER_LSTM_EMB_DIM = 200


def build_chars_to_phonemes_model(char_vocab_size, phone_vocab_size):
    '''Here we build a model that takes in a series of characters and outputs a series of phonemes.
    The model, once trained, can pronounce words.'''
    print 'Building model'
    with tf.name_scope('CHAR_TO_PHONE_MODEL'):
        # PLACEHOLDERS. Model takes in a sequence of characters contained in tf_words.
        # The model also needs to know the batch size.
        tf_batch_size = tf.placeholder(tf.int32, name='batch_size')
        tf_words = tf.placeholder(tf.int32, [None, MAX_WORD_SIZE], 'words')
        # Lookup up embeddings for all characters in each word.
        tf_char_emb = tf.Variable(tf.random_normal([char_vocab_size, PHONE_CHAR_EMB_DIM]), name='character_emb')
        # Insert each character one by one into an LSTM.
        lstm = tf.nn.rnn_cell.LSTMCell(num_units=PHONE_ENCODER_LSTM_EMB_DIM, state_is_tuple=True)
        encoder_hidden_state = lstm.zero_state(tf_batch_size, tf.float32)
        for i in range(MAX_WORD_SIZE):
            tf_char_embedding = tf.nn.embedding_lookup(tf_char_emb, tf_words[:, i])

            with tf.variable_scope('LSTM_ENCODER') as lstm_scope:
                if i > 0:
                    lstm_scope.reuse_variables()
                encoder_output, encoder_hidden_state = lstm(tf_char_embedding, encoder_hidden_state)
        # Run encoder output through dense layer to process output
        tf_encoder_output_w = tf.Variable(tf.random_normal([PHONE_ENCODER_LSTM_EMB_DIM, PHONE_ENCODER_LSTM_EMB_DIM]), name='encoder_output_emb')
        tf_encoder_output_b = tf.Variable(tf.random_normal([PHONE_ENCODER_LSTM_EMB_DIM]), name='encoder_output_bias')
        encoder_output_emb = tf.matmul(encoder_output, tf_encoder_output_w) + tf_encoder_output_b

        decoder_hidden_state = lstm.zero_state(tf_batch_size, tf.float32)

        # Use hidden state of character encoding stage (this is the phoneme embedding) to predict phonemes.
        phonemes = []
        tf_phone_pred_w = tf.Variable(tf.random_normal([lstm.output_size, phone_vocab_size]),
                                      name='phoneme_prediction_emb')
        tf_phone_pred_b = tf.Variable(tf.random_normal([phone_vocab_size]), name='phoneme_prediction_bias')
        for j in range(MAX_PRONUNCIATION_SIZE):
            with tf.variable_scope('LSTM_DECODER') as lstm_scope:
                if j == 0:
                    decoder_output, decoder_hidden_state = lstm(encoder_output_emb, decoder_hidden_state)
                else:
                    lstm_scope.reuse_variables()
                    # decoder_output, decoder_hidden_state = lstm(tf.zeros([tf_batch_size, LSTM_EMB_DIM]), decoder_hidden_state)
                    decoder_output, decoder_hidden_state = lstm(encoder_output_emb, decoder_hidden_state)
                phoneme = tf.matmul(decoder_output, tf_phone_pred_w) + tf_phone_pred_b
                phonemes.append(phoneme)
        tf_phonemes = tf.pack(phonemes, axis=1)
    # Print model variables.
    model_variables = tf.trainable_variables()
    print 'Model variables:'
    # for model_variable in model_variables:
    #     print ' - ', model_variable.name

    return [tf_words, tf_batch_size], [tf_phonemes, encoder_output_emb]


def create_dense_layer(input_layer, input_size, output_size, activation=None):
    tf_w = tf.Variable(tf.random_normal([input_size, output_size], stddev=.1))
    tf_b = tf.Variable(tf.random_normal([output_size]))
    output_layer = tf.matmul(input_layer, tf_w) + tf_b
    if activation == 'relu':
        output_layer = tf.nn.relu(output_layer)
    elif activation == 'sigmoid':
        output_layer = tf.nn.sigmoid(output_layer)
    elif activation is None:
        pass
    else:
        print 'Did not specify layer activation'

    return output_layer, tf_w, tf_b


def generate_phonetic_embs_from_words(words, char_to_index_path, phone_to_index_path):
    '''Generates a phonetic embedding for each word using the pretrained char2phone model.'''
    print 'Generating phonetic embeddings for GloVe words'
    char_to_index = pickle.load(open(char_to_index_path, 'rb'))
    phone_to_index = pickle.load(open(phone_to_index_path, 'rb'))
    character_vocab_size = len(char_to_index)
    phoneme_vocab_size = len(phone_to_index)
    model_inputs, model_outputs = build_chars_to_phonemes_model(character_vocab_size, phoneme_vocab_size)
    [tf_words, tf_batch_size] = model_inputs
    [tf_phonemes, lstm_hidden_state] = model_outputs
    tf_phonetic_emb = tf.concat(1, lstm_hidden_state)

    np_word_indices = convert_words_to_indices(words, char_to_index)
    print np_word_indices
    # Prove words converted to indices correctly by reversing the process and printing.
    index_to_char = invert_dictionary(char_to_index)
    print 'Example GloVe words recreated from indices:'
    for i in range(130, 140):
        np_word = np_word_indices[i, :]
        char_list = []
        for j in np_word:
            if j in index_to_char:
                char_list.append(index_to_char[j])
        word = ''.join(char_list)
        print word,
    print

    sess = tf.InteractiveSession(config=tf.ConfigProto(gpu_options=GPU_OPTIONS))
    saver = tf.train.Saver(max_to_keep=10)
    # Restore model from previous save.
    ckpt = tf.train.get_checkpoint_state(CHAR_2_PHONE_MODEL_DIR)
    if ckpt and ckpt.model_checkpoint_path:
        saver.restore(sess, ckpt.model_checkpoint_path)
    else:
        print("No checkpoint found!")
        return -1

    np_phonetic_emb = sess.run(tf_phonetic_emb, feed_dict={tf_words: np_word_indices,
                                                           tf_batch_size: len(words),})

    print np_phonetic_emb.shape
    print np.mean(np.abs(np_phonetic_emb))

    return np_phonetic_emb


def predict_on_hashtag(sess, model_vars, hashtag_name, hashtag_dir):
    """Predicts on a hashtag. Returns the accuracy of predictions on all tweet pairs and returns
    a list. The list contains the predictions on all tweet pairs, and tweet ids for the first and second tweets in
    each pair."""
    print 'Predicting on hashtag %s' % hashtag_name
    [tf_first_input_tweets, tf_second_input_tweets, tf_predictions, tf_tweet_humor_ratings, tf_batch_size] = model_vars
    np_first_tweets, np_second_tweets, np_labels, first_tweet_ids, second_tweet_ids = load_hashtag_data(hashtag_dir, hashtag_name)
    np_predictions = sess.run(tf_predictions, feed_dict={tf_first_input_tweets: np_first_tweets,
                                                         tf_second_input_tweets: np_second_tweets,
                                                         tf_batch_size: np_first_tweets.shape[0]})
    accuracy = np.mean(np_predictions == np_labels)
    return accuracy, [np_predictions, first_tweet_ids, second_tweet_ids]
