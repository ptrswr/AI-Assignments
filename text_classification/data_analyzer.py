import matplotlib.pyplot as plt
from sklearn.feature_extraction.text import CountVectorizer


def draw_bar_plot(x, y, filename, reduce_x_ticks=False):
    plt.bar(x, y)
    plt.xticks(rotation=45)
    if reduce_x_ticks:
        ax = plt.gca()
        ax.set_xticks(ax.get_xticks()[::6])
    plt.title(filename)
    plt.show()


def count_occurrences(feature_names, occurrences):
    temp_out = {}
    for i in range(occurrences.shape[0]):
        for (x, y) in zip(feature_names, occurrences[i]):
            if x in temp_out:
                temp_out[x] += y
            else:
                temp_out[x] = y

    temp_out = sorted(temp_out.items(), key=lambda x:x[1])
    words, occ = [], []
    for pair in temp_out:
        words.append(pair[0])
        occ.append(pair[1])

    return words, occ


def count_reviews_stats(reviews, filename):
    lens = [len(r) for r in reviews]
    max_l = max(lens)
    min_l = min(lens)
    avg_l = sum(lens) / len(lens)
    print(f'For file {filename}\nMax review length: {max_l}\nMin review length: {min_l}\nAvg review length: {avg_l}')


def count_label_occurrences(labels, filename):
    occ = {}
    for l in labels:
        l = l.strip()
        if l in occ:
            occ[l] += 1
        else:
            occ[l] = 1
    print(f'For file {filename}')
    draw_bar_plot(occ.keys(), occ.values(), filename)


def analyze_data():
    files = ['Dennis+Schwartz', 'James+Berardinelli', 'Scott+Renshaw', 'Steve+Rhodes']
    for f in files:
        with open(f'scale_data/scaledata/{f}/subj.{f}', 'r') as reader:
            lines = reader.readlines()
        with open(f'scale_data/scaledata/{f}/label.3class.{f}', 'r') as reader:
            class_3 = reader.readlines()
        with open(f'scale_data/scaledata/{f}/label.4class.{f}', 'r') as reader:
            class_4 = reader.readlines()
        with open(f'scale_data/scaledata/{f}/rating.{f}', 'r') as reader:
            ratings = reader.readlines()

        vectorizer = CountVectorizer(stop_words='english')
        x = vectorizer.fit_transform(lines)

        v_names = vectorizer.get_feature_names()
        v_matrix = x.toarray()
        words, occ = count_occurrences(v_names, v_matrix)
        # Najczesciej
        draw_bar_plot(words[-10:], occ[-10:], f + '-most')
        # Najrzadziej
        draw_bar_plot(words[:10], occ[:10], f + '-least')

        # Stats
        count_reviews_stats(lines, f)

        # Labels
        count_label_occurrences(class_3, f + '-class3')
        count_label_occurrences(class_4, f + '-class4')
        count_label_occurrences(ratings, f + '-ratings')