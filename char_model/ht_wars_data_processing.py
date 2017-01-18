'''David Donahue 2016. This script is intended to process the #HashtagWars dataset into an appropriate format
for training a model. This script extracts tweets for all hashtags in the training data located in the current
directory (training_dir located in ./) and generates tweet pairs from them. Tweets are categorized as 2 (winning tweet),
1 (one of top-ten tweets) or 0 (did not make it into top ten). Pairs are generated as follows:

    1.) Matching winning tweet with each other tweet in the top ten
    2.) Matching each tweet in the top ten with each non-winning tweet
    
Output of this script is saved to output_dir, in the form of hashtag files. Each file is a numpy array (.npy) that holds
all the tweet pairs for that hashtag. The array is of the dimension tweet_pairs by (2 * max tweet length). Each row is
then a tweet pair, with the first max_tweet_length elements being the first tweet, and the second max_tweet_length elements
being the second tweet. Each element is an index to a character that appears in the dataset. The conversion from a character
to its corresponding index is dictionary that can be found in char_to_index.cpkl, a file found in the ./ directory.
'''
from os import walk
import csv
import cPickle as pickle
import os
import random
import numpy as np
import sys

sys.path.append('../')
from config import SEMEVAL_HUMOR_TRAIN_DIR
from config import SEMEVAL_HUMOR_TRIAL_DIR
from config import HUMOR_TRAIN_TWEET_PAIR_CHAR_DIR
from config import HUMOR_TRIAL_TWEET_PAIR_CHAR_DIR
from config import HUMOR_CHAR_TO_INDEX_FILE_PATH
from config import TWEET_PAIR_LABEL_RANDOM_SEED
from tools import get_hashtag_file_names
from tools import extract_tweet_pairs_from_file

def main():
    # Find hashtags, create character vocabulary, print dataset statistics, extract/format tweet pairs and save everything.
    # Repeat this for both training and trial sets.
    print "Processing #HashtagWars training data..."
    process_hashtag_data(SEMEVAL_HUMOR_TRAIN_DIR, HUMOR_CHAR_TO_INDEX_FILE_PATH, HUMOR_TRAIN_TWEET_PAIR_CHAR_DIR)
    print "Processing #HashtagWars trial data..."
    process_hashtag_data(SEMEVAL_HUMOR_TRIAL_DIR, None, HUMOR_TRIAL_TWEET_PAIR_CHAR_DIR)
     

def process_hashtag_data(hashtag_dir, char_to_index_path, tweet_pair_path):
    hashtags = get_hashtag_file_names(hashtag_dir)
    char_to_index = build_character_vocabulary(hashtags, directory=hashtag_dir)
    print('Size of character vocabulary: %s' % len(char_to_index))
    output_tweet_statistics(hashtags, directory=hashtag_dir)
    print 'Extracting tweet pairs...'
    for i in range(len(hashtags)):
        hashtag = hashtags[i]
        random.seed(TWEET_PAIR_LABEL_RANDOM_SEED + hashtag)
        data = extract_tweet_pairs_from_file(hashtag_dir + hashtag + '.tsv')
        np_tweet_pairs, np_tweet_pair_labels = format_tweet_pairs(data, char_to_index)
        save_hashtag_data(np_tweet_pairs, np_tweet_pair_labels, hashtag, directory=tweet_pair_path)
    print 'Saving char_to_index.cpkl containing character vocabulary'
    if char_to_index_path is not None:
        pickle.dump(char_to_index, open(char_to_index_path, 'wb'))
    print "Done!"


def format_tweet_pairs(data, char_to_index, max_tweet_size=140):
    '''This script converts every character in all tweets into an index.
    It stores each tweet side by side, each tweet constrained to 150 characters long.
    The total matrix is m x 300, for m tweet pairs, two 150 word tweets per row.'''
    # Create numpy matrices to hold tweet pairs and their labels.
    np_tweet_pairs = np.zeros(shape=[len(data), max_tweet_size * 2], dtype=int)
    np_tweet_pair_labels = np.zeros(shape=[len(data)], dtype=int)
    for pair_index in range(len(data)):
        first_tweet = data[pair_index][0]
        second_tweet = data[pair_index][2]
        # Insert label for tweet pair into numpy array.
        np_tweet_pair_labels[pair_index] = data[pair_index][4]
        # Insert first tweet of pair into numpy array.
        for i in range(len(first_tweet)):
            if i < max_tweet_size:
                character = first_tweet[i]
                if character in char_to_index:
                    np_tweet_pairs[pair_index][i] = char_to_index[character]
        # Insert second tweet of pair into numpy array.
        for i in range(len(second_tweet)):
            if i < max_tweet_size:
                character = second_tweet[i]
                if character in char_to_index:
                    np_tweet_pairs[pair_index][i + max_tweet_size] = char_to_index[character]
            
    return np_tweet_pairs, np_tweet_pair_labels


def output_tweet_statistics(hashtags, directory=SEMEVAL_HUMOR_TRAIN_DIR):
    '''This function analyzes the dataset and prints statistics for it.
    These statistics have to do with the number of tweets, the largest and average
    length of tweets - for all tweets, top-ten tweets, and winning tweets.'''
    largest_tweet_length = 0
    largest_winning_tweet_length = 0
    number_of_tweets = 0
    number_of_top_ten_tweets = 0
    number_of_winning_tweets = 0
    tweet_length_sum = 0
    winning_tweet_length_sum = 0
    
    # Find tweet length statistics (max, average, std dev) and number of tweets.
    for hashtag in hashtags:
        with open(directory + hashtag + '.tsv') as tsv:
            for line in csv.reader(tsv, dialect='excel-tab'):
                # Count number of tweets, find longest tweet, find average tweet length
                # for all tweets, top ten, and winning.
                tweet_length = len(line[1])
                tweet_rank = int(line[2])
                number_of_tweets += 1
                tweet_length_sum += tweet_length
                if tweet_length > largest_tweet_length:
                    largest_tweet_length = tweet_length
                if tweet_rank == 2:
                    if tweet_length > largest_winning_tweet_length:
                        largest_winning_tweet_length = tweet_length
                    winning_tweet_length_sum += tweet_length
                    number_of_winning_tweets += 1
                if tweet_rank == 1:
                    number_of_top_ten_tweets += 1
    average_tweet_length = (float(tweet_length_sum) / number_of_tweets)
    average_winning_tweet_length = (float(winning_tweet_length_sum) / number_of_winning_tweets)
    
    # Find standard deviation.
    tweet_std_dev_sum = 0
    winning_tweet_std_dev_sum = 0
    for hashtag in hashtags:
        with open(directory + hashtag + '.tsv') as tsv:
            for line in csv.reader(tsv, dialect='excel-tab'):
                tweet_length = len(line[1])
                tweet_rank = int(line[2])
                tweet_std_dev_sum += abs(tweet_length - average_tweet_length)
                if tweet_rank == 2:
                    winning_tweet_std_dev_sum += abs(tweet_length - average_winning_tweet_length)
    tweet_std_dev = float(tweet_std_dev_sum) / number_of_tweets
    winning_tweet_std_dev = float(winning_tweet_std_dev_sum) / number_of_winning_tweets
    
    # Print statistics found above.
    print 'The largest tweet length is %s characters' % largest_tweet_length
    print 'The largest winning tweet length is %s characters' % largest_winning_tweet_length
    print 'Number of tweets: %s' % number_of_tweets
    print 'Number of top-ten tweets: %s' % number_of_top_ten_tweets
    print 'Number of winning tweets: %s' % number_of_winning_tweets
    print 'Average tweet length: %s' % average_tweet_length
    print 'Average winning tweet length: %s' % average_winning_tweet_length
    print 'Tweet length standard deviation: %s' % tweet_std_dev
    print 'Winning tweet length standard deviation: %s' % winning_tweet_std_dev


def build_character_vocabulary(hashtags, directory=SEMEVAL_HUMOR_TRAIN_DIR):
    '''Find all characters special or alphabetical that appear in the dataset.
    Construct a vocabulary that assigns a unique index to each character and
    return that vocabulary. Vocabulary does not include anything with a backslash.'''
    characters = []
    characters.append('')
    #Create list of all characters that appear in dataset.
    for hashtag in hashtags:
        with open(directory + hashtag + '.tsv') as tsv:
            for line in csv.reader(tsv, dialect='excel-tab'):
                for char in line[1]:
                    # If character hasn't been seen before, add it to the vocabulary.
                    if char not in characters:
                        characters.append(char)
    # Create dictionary from list to map from characters to their indices.
    vocabulary = {}
    for i in range(len(characters)):
        vocabulary[characters[i]] = i
    return vocabulary


def save_hashtag_data(np_tweet_pairs, np_tweet_pair_labels, hashtag, directory=HUMOR_TRAIN_TWEET_PAIR_CHAR_DIR):
    print 'Saving data for hashtag %s' % hashtag
    # Create directories if they don't exist
    if not os.path.exists(directory):
        os.makedirs(directory)
    # Save hashtag tweet pair data into training or testing folders depending on training_hashtag
    np.save(directory + hashtag + '_pairs.npy', np_tweet_pairs)
    np.save(directory + hashtag + '_labels.npy', np_tweet_pair_labels)


def test_reconstruct_tweets_from_file():
    max_tweet_size = 140
    hashtags = get_hashtag_file_names()
    char_to_index = pickle.load(open('char_to_index.cpkl', 'rb'))
    index_to_char = {v: k for k, v in char_to_index.items()}
    for (dirpath, dirnames, filenames) in walk('.'):
        for filename in filenames:
            if '_pairs.npy' in filename:
                tweets = []
                np_tweet_pairs = np.load(os.path.join(dirpath, filename))
                for i in range(np_tweet_pairs.shape[0]):
                    tweet_1_indices = np_tweet_pairs[i][:max_tweet_size]
                    tweet_2_indices = np_tweet_pairs[i][max_tweet_size:]
                    tweet1 = ''.join([index_to_char[tweet_1_indices[i]] for i in range(tweet_1_indices.size)])
                    tweet2 = ''.join([index_to_char[tweet_2_indices[i]] for i in range(tweet_2_indices.size)])
                    tweets.append(tweet1)
                    tweets.append(tweet2)
                tweets = list(set(tweets))
                with open(SEMEVAL_HUMOR_TRAIN_DIR + filename.replace('_pairs.npy', '.tsv')) as tsv:
                    for line in csv.reader(tsv, dialect='excel-tab'):
                        tweet = line[1]
                        if tweet <= max_tweet_size:
                            assert tweet in tweets

    
if __name__ == '__main__':
    main()