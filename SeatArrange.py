#!/usr/bin/env python
# coding: utf-8

# ・mtgの場所（最大グループ数・一班の最大人数）・最上期・最小期・ファシリをする期・等を冒頭に宣言（できるだけマジックナンバーを作らない）
# 
# 
# ・他の人が勝手に生成してしまわないようにパスワードをかけても良い
# 
# 
# ・対面班をアルファベット、オンライン班をアラビア数字で割り振れば処理が楽になりそう
# 
# 
# ・リーダーは各班にいなくて良い？
# 
# 
# 
# ・希望の出席形態と過去の席配置を読み込み
# 
# 
# ・ファシリ・議事録・司会を優先的に配置（議事録が新スタッフのみにならないように）
# 
# 
# ・残りを、期と前回の班がばらけるように配置（期で並び替えた後に前回の班・前々回の班で並び替えるとバラバラになる？）
# 
# ・全員に通し番号を振って処理する
# 
# ・スプシはプルダウンを使ってもらって入力を制限

# In[1]:


# 動作化環境を確認
import sys

print("Python version")
print(sys.version)
print("Version info.")
print(sys.version_info)


# ### 以下の環境で作成
# 
# Python version
# 
# 3.12.7 | packaged by Anaconda, Inc. | (main, Oct  4 2024, 13:17:27) [MSC v.1929 64 bit (AMD64)
# ]
# Version inf
# o.
# sys.version_info(major=3, minor=12, micro=7, releaselevel='final', serial=0)

# In[2]:


# CSVデータをDL
import numpy as np
import pandas as pd
df = pd.read_csv('source.csv')

# print(df)
print(df.head())
print(df.info())


# In[12]:


# 最初に変数を設定

# 全体mtg実施場所
# 一方を使って他方はコメントアウト
                                            #←ここもユーザーからの入力で選べるようにした方が良いかも
Venue = 'a' # ANNEX
# Venue = 'j' # 情報統括センター

# ファシリテーションを担当する期
Faci=20

# 最上期と最下期
OldestCohort =17 # 最上期
YoungestCohort = 21 # 最下期

# 実施場所に応じて班員の最大値と、班数の最大値を設定
# オンライン班については上限無しとする
if(Venue == 'a'):
  # ANNEXの場合
  MNmembers = 8 # 一班あたりの最大人数：Maximum Numbers of members per group
  MNgroups = 6 # 班の数の最大：Maximum Numbers of groups
elif(Venue == 'j'):
  # 情報統括センターの場合
  MNmembers = 8
  MNgroups = 8

PhyGroups = ['A','B','C','D','E','F','G','H','I','J'] # 対面グループ参照用テーブル。対面参加：physically present

# 対面とオンラインのそれぞれの出席者をカウント　←　必要無いかも？
# T：対面　O：オンライン
# print(len(df.query('attendanceFormat == "対面" ')))
sumT=len(df.query('attendanceFormat == "対面" '))
sumO=len(df.query('attendanceFormat == "Zoom" '))
# print(sumT,sumO)
# 36 16


# In[ ]:


df


# In[41]:


# code from Gemini
# サンプルデータフレーム
data = {'column1': [1, 2, 3, 4, 5], 'column2': ['A', 'B', 'A', 'C', 'B']}
df = pd.DataFrame(data)
# print(df)

# 条件を満たす行を抽出
condition = df['column2'] == 'A' # bool
df_filtered = df[condition]
# print(df_filtered)

# 乱数を生成し、インデックスに設定
random_indices = np.arange(1, len(df_filtered) + 1)  # 1から始まる連番を生成
np.random.shuffle(random_indices)  # ランダムにシャッフル
df_filtered.index = random_indices

# 元のデータフレームに反映
df.loc[condition, 'random_number'] = df_filtered.index

# print(df)


# In[22]:


# 所属している期のリストを作成。ファシリをする期優先的に配置するので先頭に移動させる。
CohortList = list(range(OldestCohort,YoungestCohort+1))
CohortList.insert(0,CohortList.pop(CohortList.index(Faci)))


# In[26]:


cnt = 0
df['seat'] = None # 結果を格納用の列を追加

# ファシリの期の人をランダムにシャッフルして、班の数以内で通し番号を振る。番号を振った後でmodで最大班数以下にする。
for Cohort in CohortList:
 condition = (df['cohort'] == Cohort) & (df['attendanceFormat'] == "対面")
 # print(condition)
 df_filtered = df[condition]
 # print(df_filtered)
 random_indices = np.arange(cnt, cnt + len(df_filtered))  # 1から始まる連番を生成
 cnt = max(random_indices) % MNgroups
 # print(random_indices)
 # print(cnt)
 # modを入れる
 np.random.shuffle(random_indices)  # ランダムにシャッフル
 df_filtered.index = random_indices

 # 元のデータフレームに反映
 df.loc[condition, 'seat'] = df_filtered.index
 # print(df)
df['seat'] = df['seat'] % MNgroups

df.sort_values('seat')


# In[27]:


# ファシリの期の人をランダムにシャッフルして、班の数以内で通し番号を振る。番号を振った後でmodで最大班数以下にする。
# df.loc[(df['cohort'] == Faci) & (df['attendanceFormat'] == "対面"), 'seat'] = range(1, len(df.loc[(df['cohort'] == Faci) & (df['attendanceFormat'] == "対面")]) + 1)
# df

# 継続は、ファシリ+1期から順に、期ごとにシャッフルして通し番号を振る。（前の期の番号をグローバル変数で管理しておくと偏りが出ないかも）


# ### 議事録担当の配置は後で実装

# In[ ]:


# 議事録担当を優先的に配置
# print(df.query(('cohort == @Faci & attendanceFormat == "対面" ')))
df_T = df.query(('attendanceFormat == "対面" '))
min_MTTimes = df_T['minuteTakerTimes'].min()
num_min_MTTimes =len(df_T.query('minuteTakerTimes == @min_MTTimes '))
print(min_MTTimes,num_min_MTTimes)

# num_min_MTTimes が1人の場合
# num_min_MTTimes のcohortを重複無しで取り出す。個数が1で且つ youngestCohort と同じ場合は、 num_min_MTTimes をインクリメント
unq = df_T.query(('minuteTakerTimes == @min_MTTimes '))['cohort'].unique()
n_unq = len(unq)
if (n_unq == 1 & unq[0] == YoungestCohort ):

elif()
# num_min_MTTimes が全員 youngestCohort の場合

# 議事録担当者の議事録担当回数をインクリメント

