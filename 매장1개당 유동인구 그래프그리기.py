#!/usr/bin/env python
# coding: utf-8

# In[2]:


import pandas as pd

commercial = pd.read_csv('./commercial.csv')
commercial


commercial.groupby('상가업소번호')['상권업종소분류명'].count().sort_values(ascending=False)



commercial['도로명주소']


# 서울시 데이터만 가져오기
# 3덩어리로 쪼갠 후 새로운 칼럼 추가
commercial[['시','구','상세주소']] = commercial['도로명주소'].str.split(' ',n=2, expand=True)


# 서울특별시의 데이터만 추출
seoul_data = commercial[ commercial['시'] == '서울특별시']
seoul_data.tail(5)


# 서울만 있는지 확인하기(집합연산)
city_type = set(seoul_data['시'])
city_type


# 서울 치킨집만 추출
seoul_chicken_data = seoul_data[ seoul_data['상권업종소분류명'] == '후라이드/양념치킨' ]
seoul_chicken_data


chicken_count_by_gu = seoul_chicken_data.groupby('구')['상권업종소분류명'].count()
chicken_count_by_gu


# In[4]:


new_chicken_count_gu = pd.DataFrame(chicken_count_by_gu).reset_index()
new_chicken_count_gu


# In[5]:


population = pd.read_csv('./population07.csv')
sum_populationo_by_gu = population.groupby('군구')['유동인구수'].sum()


# In[6]:


new_sum_populationo_by_gu = pd.DataFrame(sum_populationo_by_gu).reset_index()
new_sum_populationo_by_gu


# In[7]:


# 두 데이터 합치기
gu_chicken = new_chicken_count_gu.join(new_sum_populationo_by_gu.set_index('군구'), on = '구')
gu_chicken


# In[8]:


gu_chicken['유동인구수/치킨집수'] = gu_chicken['유동인구수'] / gu_chicken['상권업종소분류명']
gu_chicken = gu_chicken.sort_values(by='유동인구수/치킨집수')
gu_chicken


# In[14]:


import matplotlib.pyplot as plt
plt.rcParams['font.family'] = 'Malgun Gothic'

plt.figure(figsize=(10,5))
plt.bar(gu_chicken['구'], gu_chicken['유동인구수/치킨집수'])
plt.title('치킨집당 유동인구수')
plt.xlabel('구')
plt.ylabel('유동인구수/치킨집수')
plt.xticks(rotation=90)
plt.show()


# In[ ]:




