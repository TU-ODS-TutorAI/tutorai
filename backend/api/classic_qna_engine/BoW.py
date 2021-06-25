#!/usr/bin/python3

import nltk
import numpy as np
from compound_split import doc_split
from nltk.stem.snowball import SnowballStemmer
from HanTa import HanoverTagger as ht


class BagWords:

    def __init__(self, language):
        self.language = language
        self.vocabulary = []
        self.matrix = []
        self.texts = []
        self.tokens = []
        

    def str_2_vec(self, input_string):
        """
        remove stopwords
        split compound words
        stem the sentence
        return a vector (list) of tokens

        eg. "Hallo mein Name ist XY" -> ["name", "ist", "XY"]
        """

        # extract single words
        cleaned = []
        stemmed = []
        
        words = nltk.word_tokenize(input_string, self.language)
        
        if(self.language == "german"):
            tagger = ht.HanoverTagger('morphmodel_ger.pgz')
            lemmata = tagger.tag_sent(words, taglevel=1)

            for lemma in lemmata:
                if(lemma[2] == "NN" or lemma[2] == "NE" or lemma[2].startswith("ADJ") or lemma[2].startswith("VV")):
                    if((lemma[2] == "NN" or lemma[2] == "NE") and self.language == "de"):
                        compounds = doc_split.maximal_split(lemma[0])
                        for compound in compounds:
                            compound = compound.replace("-", "")
                            cleaned.append(compound.lower())
                    else:
                        cleaned.append(lemma[0].lower())
        else:
            tagger = nltk.pos_tag(words)
            
            for tag in tagger:
                if(tag[1].startswith("NN") or tag[1].startswith("VB")):
                    word = tag[0].lower()
                    word = word.replace("-", "")
                    cleaned.append(word)
        
        # stem
        stemmer = SnowballStemmer(self.language)
        for element in cleaned:
            stemmed.append(stemmer.stem(element))

        return stemmed
        
    
    # create matrix term list
    def create_vocabulary(self, sentence):
        """
        takes as input a sentence in form of a stemmed vector
        adds new tokens to the vocabulary
        """
        for term in sentence:
            if term not in self.vocabulary:
                self.vocabulary = np.append(self.vocabulary, term)

    
    def calculate_vec(self, sentence_vector, voc=None):
        """
        given a sentence in the form of a list of stemmed tokens
        this method calculates a term frequency vector based on
        the vocabulary.

        Input: vector of tokens
        Output: term frequency vector
        """
        if not voc:
            vocabulary = np.array(self.vocabulary)
        else:
            vocabulary = np.array(voc)

        sentence_vector = np.array(sentence_vector)

        indexes = [np.where(x == vocabulary)[0][0] for x in sentence_vector]
        result = np.zeros(vocabulary.shape)

        for i in indexes:
            result[i] += 1

        return result

    # PUBLIC METHODS--------------------------------------------------------

    def compute_matrix(self):
        """
        given all the sentences added, the bag of words will compute
        the term frequency matrix
        """
        self.matrix = []
        # add all sentences to vocabulary

        for i in range(len(self.texts)):
            if not isinstance(self.texts[i], list):
                self.texts[i] = self.str_2_vec(self.texts[i])
                self.create_vocabulary(self.texts[i])

        # calculate matrix
        j = 1
        for text in self.texts:
            vec = self.calculate_vec(text)
            self.matrix.append(vec)

        self.matrix = np.array(self.matrix)

    def add_sentence(self, sentence):
        """
        adds a sentence to the texts.
        After adding all sentences it is necessary to
        call the method compute_matrix()
        """
        self.texts.append(sentence)

    def tf_idf(self):
        """
        calculate inverse term frequency
        IDF = 1 + log(N/nj)

        N = number of total vectors
        nj = number of vectors containing the word
        """

        x = np.array(self.matrix)

        # number of vectors
        N = x.shape[0]
        nj = (x > 0).sum(axis=0) * np.ones(x.shape)

        tfidf = x * (1 + np.log(N/nj))

        self.matrix = tfidf

    def similarity(self, new_sentence):
        """
        given a new string calculates the similarity
        between it and every other vector and returns
        the index of the text.

        For performance reasons, the matrix in not calculated again.
        Instead, the number of new tokens in the input sentence
        is calculated and for each token a new column of 0s is added
        (since the word is new there is no old sentence with this word)
        and given the new vocabulary (old + new tokens), the vector of the
        new sentence is calculated and used to compute similarity with
        the sentences in the matrix

        Input: string
        Output: comparison matrix
        """
        tokens = self.str_2_vec(new_sentence)
        self.tokens = tokens

        if not set(tokens).intersection(set(self.vocabulary)):
            return None


        else:
            difference = set(tokens) - set(self.vocabulary)
            to_append = np.zeros((self.matrix.shape[0], len(difference)))
            matrix = np.append(self.matrix, to_append, axis=1)
            new_voc = list(self.vocabulary) + list(difference)
            question_vector = self.calculate_vec(tokens, new_voc)
            result = np.matmul(matrix, question_vector)

            return result

