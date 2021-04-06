from __future__ import print_function
import pandas as pd
from sklearn import metrics
from sklearn.tree import DecisionTreeClassifier

TRAIN_PATH = '.\\data\\default.csv'
TEST_PATH = '.\\data\\test.csv'

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
    print('学習用データ')
    train, label_train = read_dataset(TRAIN_PATH)
    print('評価用データ')
    test, label_test = read_dataset(TEST_PATH)

    clf = DecisionTreeClassifier()
    
    clf.fit(train, label_train)
    pred = clf.predict(test)

    print('正解率 : {:.2f} %'.format(
        metrics.accuracy_score(pred, label_test) * 100))


if __name__ == '__main__':
    main()
