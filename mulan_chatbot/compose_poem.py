import tensorflow as tf
from poems.model import rnn_model
from poems.poems import process_poems
import numpy as np

start_token = 'B'
end_token = 'E'
model_dir = './model/'
corpus_file = './data/poems.txt'

lr = 0.0002


def to_word(predict, vocabs):
    t = np.cumsum(predict)
    s = np.sum(predict)
    sample = int(np.searchsorted(t, np.random.rand(1) * s))
    if sample > len(vocabs):
        sample = len(vocabs) - 1
    return vocabs[sample]


def gen_poem(begin_word, poem_flag):
    batch_size = 1
    poems_vector, word_int_map, vocabularies = process_poems(corpus_file)
    input_data = tf.placeholder(tf.int32, [batch_size, None])
    end_points = rnn_model(model='lstm', input_data=input_data, output_data=None, vocab_size=len(
        vocabularies), rnn_size=128, num_layers=2, batch_size=64, learning_rate=lr)

    saver = tf.train.Saver(tf.global_variables())
    init_op = tf.group(tf.global_variables_initializer(), tf.local_variables_initializer())
    with tf.Session() as sess:
        sess.run(init_op)
        saver.restore(sess, "./model/"+"poems-"+str(poem_flag))
        x = np.array([list(map(word_int_map.get, start_token))])
        [predict, last_state] = sess.run([end_points['prediction'], end_points['last_state']],
                                         feed_dict={input_data: x})
        if begin_word:
            word = begin_word
        else:
            word = to_word(predict, vocabularies)
        poem_ = ''

        i = 0
        while word != end_token:
            poem_ += word
            i += 1
            if i >= 24:
                break
            x = np.zeros((1, 1))
            x[0, 0] = word_int_map[word]
            [predict, last_state] = sess.run([end_points['prediction'], end_points['last_state']],
                                             feed_dict={input_data: x, end_points['initial_state']: last_state})
            word = to_word(predict, vocabularies)
        return poem_


def pretty_print_poem(poem_):
    replyTxt=''
    poem_sentences = poem_.split('。')
    for s in poem_sentences:
        if s != '' and len(s) > 8:
            replyTxt+=s
            # print(s + '。')
    return replyTxt


def is_chinese(begin_char):
    if '\u4e00' <= begin_char <='\u9fff':
        return True
    else:
        return False

def is_number(letter):
    if '\u0030' <= letter <='\u0039':
        return True
    else:
        return False

def run():
    b = True
    while b == True:
        begin_char = input('## please input the first character in chinese:')
        while '啊' in begin_char:
            begin_char = input('## please input another first character in chinese:')
        c = len(begin_char)
        while c != 1:
            begin_char = input('## please input the correct number of first character in chinese:')
            c = len(begin_char)
        a = is_chinese(begin_char)
        while a == False:
            begin_char = input('## please input the correct first character in chinese:')
            a = is_chinese(begin_char)
            while '啊' in begin_char:
                begin_char = input('## please input another first character in chinese:')
        poem_flag = 24
        poem = gen_poem(begin_char, poem_flag)
        pretty_print_poem(poem_=poem)
        tf.reset_default_graph()
        letter = input('## input any number to continue:')
        b = is_number(letter)
    print("See you again! Bye bye!")

if __name__ == '__main__':
    run()










