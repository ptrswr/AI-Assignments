from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn import preprocessing


# files = ['Dennis+Schwartz']
# files = ['Dennis+Schwartz', 'James+Berardinelli']
# files = ['Dennis+Schwartz', 'James+Berardinelli', 'Scott+Renshaw']
files = ['Dennis+Schwartz', 'James+Berardinelli', 'Scott+Renshaw', 'Steve+Rhodes']


def load_data():
    print('[1/3] Loading datasets')
    reviews = []
    labels = []
    for f in files:
        with open(f'scale_data/scaledata/{f}/subj.{f}', 'r') as reader:
            for line in reader:
                reviews.append(line.strip())

        with open(f'scale_data/scaledata/{f}/label.3class.{f}', 'r') as reader:
            for line in reader:
                labels.append(line.strip())

    return reviews, labels


def prepare_training_set(reviews):
    print('[2/3] Extracting features')
    vectorizer = TfidfVectorizer(analyzer='word',
                                 stop_words='english',
                                 norm='l2',
                                 min_df=0.01,
                                 max_df=1.0)
    return vectorizer.fit_transform(reviews).toarray()
