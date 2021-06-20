from __future__ import print_function
import sys
import pandas as pd
from sklearn import metrics
#アルゴリズム用
from sklearn.ensemble import VotingClassifier
#from sklearn.ensemble import AdaBoostClassifier
#from sklearn.ensemble import BaggingClassifier
#from sklearn.ensemble import ExtraTreesClassifier
#from sklearn.ensemble import GradientBoostingClassifier
from sklearn.ensemble import RandomForestClassifier
#from sklearn.neighbors import KNeighborsClassifier
#from sklearn.linear_model import LogisticRegression
#from sklearn.naive_bayes import GaussianNB
#from sklearn.svm import SVC
#from sklearn.svm import LinearSVC
#from sklearn.tree import DecisionTreeClassifier

# python learn-judge.py learndata judgedata

if len(sys.argv) < 2:
    print("引数エラー\n引数の個数を確認してください。\npython learn-judge.py learndata judgedata")
    exit()

TRAIN_PATH = './data/' + sys.argv[1]
TEST_PATH = './data/' + sys.argv[2]

## サンプリングサイズ
N = 10000

LABEL_NORMAL = 1
LABEL_ATTACK = -1

# カテゴリ値の"サービス"を使ってみます
FEATURES = [
    'Duration',  
    'Source bytes',
    'Destination bytes',
    'Count',
    'Same_srv_rate',
    'Serror_rate',
    'Srv_serror_rate',
    'Dst_host_count',
    'Dst_host_srv_count',
    'Dst_host_same_src_port_rate',
    'Dst_host_serror_rate',
    'Dst_host_srv_serror_rate',
]


# CSV を読み込んでラベルとともに返す
def read_dataset(path, n=N):
    df = pd.read_csv(TRAIN_PATH)
    # データフレームのうちラベルが正常のもの
    normal = df[df.Label == LABEL_NORMAL]
    # 正常なものについて使用する特徴量のみを切り出してサンプリング
    normal = normal.loc[:, FEATURES].sample(n)

    # データフレームのうちラベルが攻撃のもの
    attack = df[df.Label == LABEL_ATTACK]
    # 攻撃について使用する特徴量のみを切り出してサンプリング
    # クラスごとのサンプル数が不均衡なのは望ましくないので同数にします
    attack = attack.loc[:, FEATURES].sample(n)

    label = [LABEL_NORMAL] * len(normal) + [LABEL_ATTACK] * len(attack)
    print('正常 : {}, 攻撃 : {}'.format(normal.shape, attack.shape))

    return pd.concat((normal, attack)), label


def main():

    estimators = [
            #('ada', AdaBoostClassifier()),
            #('bag', BaggingClassifier()),
            #('et', ExtraTreesClassifier()),
            #('gb', GradientBoostingClassifier()),
            ('rf', RandomForestClassifier(n_estimators=100)),
            #('knn', KNeighborsClassifier()),
            #('logit', LogisticRegression(solver='lbfgs', max_iter=10000)),
            #('nb', GaussianNB()),
            #('svm', SVC(gamma='scale', probability=True)),
            #('linearSVC',LinearSVC()),
            #('tree', DecisionTreeClassifier())
    ]

    print('学習用データ')
    train, label_train = read_dataset(TRAIN_PATH)
    print('評価用データ')
    test, label_test = read_dataset(TEST_PATH)

    clf = VotingClassifier(estimators)
    
    clf.fit(train, label_train)
    pred = clf.predict(test)

    print('正解率 : {:.2f} %'.format(
        metrics.accuracy_score(pred, label_test) * 100))


if __name__ == '__main__':
    main()
