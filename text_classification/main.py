from model import load_data, prepare_training_set
from sklearn.naive_bayes import MultinomialNB
from sklearn.model_selection import cross_val_score, GridSearchCV
from sklearn.linear_model import LogisticRegression
from sklearn.svm import SVC
from sklearn.neighbors import KNeighborsClassifier


def train_clf(clf, x_train, y_train, cv=10):
    score = cross_val_score(clf, x_train, y_train, cv=cv, scoring='accuracy', verbose=1)
    print(f'Scores for {cv}-cross validation: {score}\nMean: {score.mean()}')


def search_best_params(clf, data, target, parameters):
    print('[3/3] Starting GridSearch')
    gs = GridSearchCV(
        clf,
        parameters,
        cv=10,
        verbose=3
    )
    gs.fit(data, target)
    print(f'Best score: {gs.best_score_}')
    print(f'Best params: {gs.best_params_}')
    print(f'Best scores from each fold: {gs.cv_results_["mean_test_score"]}')


def main():
    reviews, labels = load_data()
    x_train = prepare_training_set(reviews)
    svc = SVC()
    train_clf(svc, x_train, labels)

    nb = MultinomialNB()
    train_clf(nb, x_train, labels)


if __name__ == '__main__':
    main()
