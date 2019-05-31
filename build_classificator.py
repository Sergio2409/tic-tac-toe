#!/usr/bin/env python
# -*- coding: utf-8 -*-
# -----------------------------------------------
# Copyright (c) ░s░e░r░g░i░o░v░a░l░d░e░s░2░4░0░9░
# Mail: sergiovaldes2409@gmail.com
#
# All rights reserved.
#
#
"""
Module description goes here

"""
import os
import pickle
import numpy as np
import pandas as pd
from sklearn.base import clone
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.svm import SVC
from sklearn.ensemble import RandomForestClassifier, ExtraTreesClassifier, VotingClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.neighbors import KNeighborsClassifier


class BuiltClassificators(object):

    def __init__(self, d_set_filename = 'tictac_single.txt', pickle_name = "dict.pickle"):
        self.data_set_name = d_set_filename
        self.pickle_file = pickle_name
        self.load_data()
        self.initialize_classificators()

    def load_data(self):
        Data_Interm = np.loadtxt(self.data_set_name)
        Interm_X = Data_Interm[:,:9]           # Input features
        Interm_y = Data_Interm[:,9:]
        features_train, features_test, labels_train, labels_test = train_test_split(
            Interm_X, Interm_y, test_size=0.2, random_state=24)

        self.X_train = features_train
        self.labels_train = labels_train
        self.X_test = features_test
        self.labels_test = labels_test

    def produce_data_for_Xvalues(self, Interm_X, Interm_y):
        targets = Interm_y.tolist()
        import ipdb;ipdb.set_trace();
        f = open("tictac_single_for_X_icon.txt","w+")
        for pos, _array in enumerate(Interm_X):
            line = self._replace(Interm_X[pos].tolist(), 1.0, -1.0)
            line += targets[pos]
            line = ' '.join([str(int(el)) for el in line])
            f.write(line + '\n')
        f.close()

    def _replace(self, elements, replace, by):
        _list = elements
        for pos in range(len(_list)):
            if _list[pos] == replace:
                _list[pos] = by
            elif _list[pos] == by:
                _list[pos] = replace
        return _list



    def remove_pickle_data(self):
        os.remove(self.pickle_file)
        self.__init__()

    def add_line_to_dataset(self, line_data):
        with open(self.data_set_name, "a") as myfile:
            # Write the line more than one in ordert increase the probability
            myfile.write(line_data)
            myfile.write(line_data)
            myfile.write(line_data)

    def get_score(self, classifier):
        return classifier.score(self.X_test, self.labels_test)

    def fit_model(self, classifier):
        self.max_score = 0
        self.best_classifier = None
        classifier.fit(self.X_train, self.labels_train)
        _score = self.get_score(classifier)
        if _score > self.max_score:
            self.max_score = _score
            self.best_classifier = classifier
        return classifier

    def fit_model_multiple_times(self, classifier):
        self.max_score = 0
        self.best_classifier = None
        _copy = None
        classifier.fit(self.X_train, self.labels_train)
        for i in range(10):
            _score = self.get_score(classifier)
            _copy = clone(classifier)
            _copy.fit(self.X_train, self.labels_train)
            copy_score = self.get_score(_copy)
            if _score < copy_score:
                classifier = _copy
                max_score = copy_score
                if copy_score > self.max_score:
                    self.max_score = copy_score
                    self.best_classifier = classifier
                print('Score step: ', copy_score, '\n')
            else:
                if _score > self.max_score:
                    self.max_score = _score
                    self.best_classifier = classifier
        return classifier


    def save_best_classifier(self):
        if self.best_classifier is None:
            self.best_classifier = self.ensemble
        pickle_out = open(self.pickle_file, "wb")
        pickle.dump(self, pickle_out)
        pickle_out.close()

    @staticmethod
    def load_classifiers(d_set_filename, pickle_name="dict.pickle"):
        try:
            pickle_in = open(pickle_name, "rb")
            loaded = pickle.load(pickle_in)
            pickle_in.close()
        except FileNotFoundError as error:
            loaded = BuiltClassificators(d_set_filename=d_set_filename, pickle_name=pickle_name)
        return loaded

    def plot_data(self, classifier=None):
        import matplotlib.pyplot as plt
        if not classifier:
            classifier = self.best_classifier
        predictions = classifier.predict(self.X_test)
        # Showing graphs
        plt.plot(range(len(predictions)), predictions, c='green')
        plt.plot(range(len(predictions)), np.transpose(self.labels_test)[0], c='blue')
        plt.show()

    def initialize_classificators(self):
        self.decision_tree = DecisionTreeClassifier(max_depth=18, criterion="entropy")
        self.decision_tree = self.fit_model(self.decision_tree)

        #self.svm = SVC(gamma='auto') # Clearly the data is non linear.
        #self.svm  = self.fit_model(self.svm )


        self.knn = clf3 = KNeighborsClassifier(n_neighbors=1)
        self.knn = self.fit_model(self.knn)

        self.ext_tree = ExtraTreesClassifier(n_estimators=200, n_jobs=-1)
        self.fit_model(self.ext_tree)

        self.ensemble = VotingClassifier(estimators=[('DecisionTree', self.decision_tree),
                                                ('KNN', self.knn),
                                                ('ExtraTrees', self.ext_tree)],
                                         voting='soft')
        self.ensemble = self.fit_model(self.ensemble)
        self.save_best_classifier()


