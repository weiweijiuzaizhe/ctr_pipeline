 # 数据源介绍

 * kaggle 2014 criteo 点击率预估比赛,数据经过脱敏处理,官方页面: https://www.kaggle.com/c/criteo-display-ad-challenge/data  ,但是下载数据的页面已经失效了,通过迅雷离线下载到了,要想个方法分享出来,下载的文件是 dac.tar.gz,解压缩之后是45840617行的train.txt,以及6042135行的test.txt,
train.txt的前两行为例子:

0       1       1       5       0       1382    4       15      2       181     1       2               2       68fd1e64        80e26c9b        fb936136        7b4723c4        25c83c98        7e0ccccf        de7995b8        1f89b562        a73ee510a8cd5504        b2cb9c98        37c9c164        2824a5f6        1adce6ef        8ba8b39a        891b62e7        e5ba7672        f54016b9        21ddcdc9        b1252a9d        07b5194c                3a171ecb        c5c50484        e8b83407        9727dd16


0       2       0       44      1       102     8       2       2       4       1       1               4       68fd1e64        f0cf0024        6f67f7e5        41274cd7        25c83c98        fe6b92e5        922afcc0        0b153874        a73ee5102b53e5fb        4f1b46f3        623049e6        d7020589        b28479f6        e6c5b5cd        c92f3b61        07c540c4        b04e4670        21ddcdc9        5840adea        60f6221e                3a171ecb        43f13e8b        e8b83407        731c3655


 * Label - Target variable that indicates if an ad was clicked (1) or not (0). 第1列是label值,1或0表示点或者不点
 * I1-I13 - A total of 13 columns of integer features (mostly count features). 第2-14列是数值特征
 * C1-C26 - A total of 26 columns of categorical features. The values of these features have been hashed onto 32 bits for anonymization purposes.   第15-40列是类别特征,每个值都被hash成了32bit
 需要注意的是,有些行的值是空,既不是整数,也不是hash值,criteo_stat.py对于整个数据出现的维度和值的频次进行统计,输出cls_value_cnt_id.txt文件,提供给后面的one hot编码使用




 * Avito Context Ad Clicks  点击率预估比赛,数据没有经过脱敏处理,带有原始的信息 : https://www.kaggle.com/c/avito-context-ad-clicks/data 
