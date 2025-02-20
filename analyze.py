import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from colorcet import palette

data = pd.read_csv("tiktok_dataset.csv")

data.head(10)
data.info
data.describe()
data.columns

data['claim_status'].value_counts()

claims=data[data['claim_status']=='claim']
print('Mean view count claims:', claims['video_view_count'].mean())
print('Median view count claims:', claims['video_view_count'].median())

opinions = data[data['claim_status'] == 'opinion']
print('Mean view count opinions:', opinions['video_view_count'].mean())
print('Median view count opinions:', opinions['video_view_count'].median())

data.groupby(['claim_status', 'author_ban_status']).count()[['#']]

data.groupby(['author_ban_status']).agg(
    {'video_view_count': ['mean', 'median'],
     'video_like_count': ['mean', 'median'],
     'video_share_count': ['mean', 'median']})

data.groupby(['author_ban_status']).median(numeric_only=True)[['video_share_count']]

data.groupby(['author_ban_status']).agg(
    {'video_view_count': ['count', 'mean', 'median'],
     'video_like_count': ['count', 'mean', 'median'],
     'video_share_count': ['count', 'mean', 'median']
     })

data['likes_per_view'] = data['video_like_count'] / data['video_view_count']
data['comments_per_view'] = data['video_comment_count'] / data['video_view_count']
data['shares_per_view'] = data['video_share_count'] / data['video_view_count']

data.groupby(['claim_status', 'author_ban_status']).agg(
    {'likes_per_view': ['count', 'mean', 'median'],
     'comments_per_view': ['count', 'mean', 'median'],
     'shares_per_view': ['count', 'mean', 'median']})

# a boxplot to visualize distribution of `video_duration_sec'
plt.figure(figsize=(5,1))
plt.title('Video duration secV')
sns.boxplot(x=data['video_duration_sec'])

# Create a histogram of'Video duration sec'
plt.figure(figsize=(6,3))
plt.title('Video duration sec')
plt.hist(data['video_duration_sec'], bins=range(0,61,5), edgecolor='black')

## Create a boxplot to visualize distribution of `video_view_count`
plt.figure(figsize=(5,1))
plt.title('video view count')
sns.boxplot(x=data['video_view_count'])

# Create a histogram of 'video view count'
plt.figure(figsize=(5,3))
plt.title('video view count histogram')
sns.histplot(x=data['video_view_count'],bins=range(0,10**6+1,10**5),edgecolor='black')

#Create a boxplot of 'video_like_count'
plt.figure(figsize=(10,1))
plt.title('Video like count')
sns.boxplot(x=data['video_like_count'])

#Create a histogram of 'video_like_count'
ax = sns.histplot(data['video_like_count'], bins=range(0,(7*10**5+1),10**5))
labels = [0] + [str(i) + 'k' for i in range(100, 701, 100)]
ax.set_xticks(range(0,7*10**5+1,10**5), labels=labels)
plt.title('Video like count histogram')

# Create a boxplot to visualize distribution of `video_comment_count`
plt.figure(figsize=(5,1))
plt.title('video comment count boxplot')
sns.boxplot(x=data['video_comment_count'])

#Create a histogram of 'video_comment_count'
plt.figure(figsize=(5,3))
plt.title('video comment count')
sns.histplot(x=data['video_comment_count'],bins=range(0,(3001),100))

# Create a boxplot to visualize distribution of `video_share_count`
plt.figure(figsize=(5,1))
plt.title('video_share_count')
sns.boxplot(x=data['video_share_count'])

#Create a histogram of 'video_share_count'
plt.figure(figsize=(5,3))
sns.histplot(data['video_share_count'], bins=range(0,(270001),10000))
plt.title('Video share count histogram')

# Create a boxplot to visualize distribution of `video_download_count`
plt.figure(figsize=(5,1))
plt.title('video_download_count')
sns.boxplot(x=data['video_download_count'])

#create a histogram of 'video_download_count'
plt.figure(figsize=(5,3))
sns.histplot(data['video_download_count'], bins=range(0,(15001),500))
plt.title('Video download count histogram')

plt.figure(figsize=(7,4))
sns.histplot(data=data,
             x='claim_status',
             hue='verified_status',
             multiple='dodge',
             shrink=0.9)
plt.title('Claims by verification status histogram')

plt.figure(figsize=(7,4))
sns.histplot(data=data , x='claim_status' , hue='author_ban_status',
             multiple='dodge',
             hue_order= [ 'active', 'under review', 'banned'],
             shrink=0.9,
             palette={'active':'green','under review':'orange','banned':'red'},
             alpha=0.5)
plt.title('Claim status by author ban status - counts')


ban_status_counts=data.groupby(['author_ban_status']).median(
    numeric_only=True).reset_index()
plt.figure(figsize=(7,4))
sns.barplot(data=ban_status_counts,
            x='author_ban_status',
            y='video_view_count',
            order=['active','under review','banned'],
            palette={'active':'green','under review':'orange','banned':'red'},
            alpha=0.5)
plt.title('Median view count by ban status')

data.groupby('claim_status')['video_view_count'].median()


plt.figure(figsize=(7,4))
plt.pie(data.groupby('claim_status')['video_view_count'].sum(), labels=['claim','opinion'])
plt.title('Total views by video claim status')

count_cols = ['video_view_count',
              'video_like_count',
              'video_share_count',
              'video_download_count',
              'video_comment_count',
              ]
for column in count_cols:
    q1 = data[column].quantile(0.25)
    q3 = data[column].quantile(0.75)
    iqr = q3 - q1
    median = data[column].median()
    outlier_threshold = median + 1.5*iqr

    # Count the number of values that exceed the outlier threshold
    outlier_count = (data[column] > outlier_threshold).sum()
    print(f'Number of outliers, {column}:', outlier_count)

# Create a scatterplot of `video_view_count` versus `video_like_count` according to 'claim_status'
sns.scatterplot(x=data["video_view_count"], y=data["video_like_count"],
                hue=data["claim_status"], s=10, alpha=.3)
plt.show()

# Create a scatterplot of `video_view_count` versus `video_like_count` for opinions only
opinion = data[data['claim_status']=='opinion']
sns.scatterplot(x=opinion["video_view_count"], y=opinion["video_like_count"],
                 s=10, alpha=.3)
plt.show()