#coding=utf-8
import cPickle
import sys

import numpy as np
import theano
import theano.tensor as T

sys.path.append('.')

from LoadData import load_data_x
from LoadData import load_data_y
from MLP_GRU import MLP

import uniout

def build_model_for_predication(
        data_set='data/RNNinput.txt',
        out_file='data/gru_test/test_4/output.txt',
        n_hidden=400):
    print '...loading data'

    path = '../data/gru_test/gaokao2016/quanguo3/'

    out_file = path + 'output.txt'

    x_set, w_set = load_data_x(path + 'words.txt', path + 'dict.txt')
    y_set = load_data_y(path + 'labels.txt')

    for i in range(5, 10, 5):
    # for i in range(0, 1, 1):
        print '...loading parameters'
        # f = open('../data/6000params/gru_params/epoch_' + str(i) + '.txt', 'rb')
        f = open('../data/6000params/gru_params/epoch_5.txt', 'rb')
        # f = open('../data/20000params/gru_params/epoch_25.txt', 'rb')

        best_params = cPickle.load(f)
        f.close()

        print 'result of epoch' + str(i)
        # print '...rebuilding model'

        x = T.matrix('x', dtype=theano.config.floatX)
        rng = np.random.RandomState(1234)

        classifier = MLP(rng = rng,
                         input=x,
                         n_in=100,
                         n_hidden=n_hidden,
                         n_out=2)
        #predictor = theano.function(inputs=[x],  outputs=classifier.output_layer.y_pred)
        predictor = theano.function(inputs=[x], outputs=classifier.output_layer.p_y_given_x)

        classifier.hidden_layer.U.set_value(best_params[0])
        classifier.hidden_layer.V.set_value(best_params[1])
        classifier.hidden_layer.W.set_value(best_params[2])
        classifier.output_layer.W.set_value(best_params[3])
        classifier.output_layer.b.set_value(best_params[4])

        # print '...printing calculate results to %s' % out_file

        f = open(out_file, 'w')
        for index in xrange(len(x_set)):
            print >> f, predictor(x_set[index])[0][1], y_set[index]
        f.close()

        ######################################################################################
        f = open(path + 'output.txt', mode='r')

        propabilities = []
        right_one = []

        for line in f:
            propabilities.append(float(line.split(" ")[0]))
            right_one.append(int(line.split(" ")[1]))

        f.close()

        size = len(propabilities) / 4

        right_num = 0
        wrong_num = 0

        for index in xrange(size):
            print w_set[4 * index]
            right_index = -1
            max_index = -1
            max_p = -1

            for i in xrange(4):
                if propabilities[index * 4 + i] > max_p:
                    max_index = i
                    max_p = propabilities[index * 4 + i]
                if right_one[index * 4 + i] == 1:
                    right_index = i

            print index+1, ": ", max_index,

            if (right_index == max_index):
                right_num += 1
                print "1"
            else:
                wrong_num += 1
                print ' '

        print "    ", right_num, wrong_num
        print "    ", float(right_num) / float(right_num + wrong_num)

if __name__ == '__main__':
    build_model_for_predication()

