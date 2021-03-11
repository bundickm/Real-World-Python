import nltk
from nltk.corpus import stopwords
import matplotlib.pyplot as plt

LINES = ['-', ':', '--']  # Line style for plots

def main():
    strings_by_author = dict()
    strings_by_author['doyle'] = text_to_string('hound.txt')
    strings_by_author['wells'] = text_to_string('war.txt')
    strings_by_author['unknown'] = text_to_string('lost.txt')

    print(strings_by_author['doyle'][:300])

    words_by_author = make_word_dict(strings_by_author)
    len_shortest_corpus = find_shortest_corpus(words_by_author)
    word_length_test(words_by_author, len_shortest_corpus)
    stopwords_test(words_by_author, len_shortest_corpus)
    parts_of_speech_test(words_by_author, len_shortest_corpus)
    vocab_test(words_by_author)
    jacard_test(words_by_author, len_shortest_corpus)


def text_to_string(filename):
    '''Read a text file and return a string'''
    with open(filename) as infile:
        return infile.read()


def make_word_dict(strings_by_author):
    '''Return dictionary of tokenized words by corpus by author'''
    words_by_author = dict()
    for author in strings_by_author:
        tokens = nltk.word_tokenize(strings_by_author[author])
        words_by_author[author] = ([token.lower() for token in tokens
                                    if token.isalpha()])
    return words_by_author


def find_shortest_corpus(words_by_author):
    '''Return length of shortest corpus'''
    word_count = []

    for author in words_by_author:
        word_count.append(len(words_by_author[author]))
        print('\nNumber of words for {} = {}\n'.
                format(author, len(words_by_author[author])))

    len_shortest_corpus = min(word_count)
    print('Length of shortest corpus = {}\n'.format(len_shortest_corpus))

    return len_shortest_corpus


def word_length_test(words_by_author, len_shortest_corpus):
    '''Plot word length freq by author, truncated to shortest corpus length.'''
    by_author_length_freq_dist = dict()
    plt.figure(1)
    plt.ion()

    for i, author in enumerate(words_by_author):
        word_lengths = [len(word) for word in words_by_author[author]
                        [:len_shortest_corpus]]
        by_author_length_freq_dist[author] = nltk.FreqDist(word_lengths)
        by_author_length_freq_dist[author].plot(15, linestyle=LINES[i],
                                                label=author,
                                                title='Word Length')

    plt.legend()
    # plt.show()


def stopwords_test(words_by_author, len_shortest_corpus):
    '''Plot stopwords freq by author, truncated to shortest corpus length'''
    stopwords_by_author_freq_dist = dict()
    plt.figure(2)
    stop_words = set(stopwords.words('english'))
    # print('Number of stopwords = {}\n'.format(len(stop_words)))
    # print('Stopwords = {}\n'.format(stop_words))

    for i, author in enumerate(words_by_author):
        stopwords_by_author = [word for word in words_by_author[author]
                                [:len_shortest_corpus] if word in stop_words]
        stopwords_by_author_freq_dist[author] = nltk.FreqDist(stopwords_by_author)
        stopwords_by_author_freq_dist[author].plot(50, label=author,
                                                    linestyle=LINES[i],
                                                    title='50 Most Common Stopwords')

    plt.legend()
    # plt.show()


def parts_of_speech_test(words_by_author, len_shortest_corpus):
    '''Plot author use of parts-of-speech such as nouns, verbs, etc.'''
    by_author_pos_freq_dist = dict()
    plt.figure(3)
    for i, author in enumerate(words_by_author):
        pos_by_author = [pos[1] for pos in nltk.pos_tag(words_by_author[author]
                            [:len_shortest_corpus])]
        by_author_pos_freq_dist[author] = nltk.FreqDist(pos_by_author)
        by_author_pos_freq_dist[author].plot(35, label=author,
                                                linestyle=LINES[i],
                                                title='Parts of Speech')
    plt.legend()
    plt.show()


def vocab_test(words_by_author):
    '''Compare author vocabularies using the chi-squared test'''
    chisquared_by_author = dict()
    for author in words_by_author:
        if author != 'unknown':
            combined_corpus = (words_by_author[author] +
                                words_by_author['unknown'])
            author_proportion = (len(words_by_author[author])
                                    / len(combined_corpus))
            combined_freq_dist = nltk.FreqDist(combined_corpus)
            most_common_words = list(combined_freq_dist.most_common(100))
            chisquared = 0
            for word, combined_count in most_common_words:
                observed_count_author = words_by_author[author].count(word)
                expected_count_author = combined_count * author_proportion
                chisquared += ((observed_count_author - expected_count_author)**2
                                / expected_count_author)
                chisquared_by_author[author] = chisquared
            print('Chi-Squared for {} = {:.1f}'.format(author, chisquared))
    most_likely_author = min(chisquared_by_author, key=chisquared_by_author.get)
    print('Most likely author by vocabulary is {}\n'.format(most_likely_author))


def jacard_test(words_by_author, len_shortest_corpus):
    '''Calculate Jacard Similarity of each known corpus to unknown corpus'''
    jacard_by_author = dict()
    unique_words_unknown = set(words_by_author['unknown'][:len_shortest_corpus])
    authors = (author for author in words_by_author if author != 'unknown')
    for author in authors:
        unique_words_author = set(words_by_author[author][:len_shortest_corpus])
        shared_words = unique_words_author.intersection(unique_words_unknown)
        jacard_sim = (float(len(shared_words)) / (len(unique_words_author)
                                                    + len(unique_words_unknown)
                                                    - len(shared_words)))
        jacard_by_author[author] = jacard_sim
        print('Jacard Similarity for {} = {}'.format(author, jacard_sim))
    most_likely_author = max(jacard_by_author, key=jacard_by_author.get)
    print('Most likely author by similarity is {}'.format(most_likely_author))


if __name__ == '__main__':
    main()
    input()