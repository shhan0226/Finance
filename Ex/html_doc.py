#!/usr/bin/env python
# coding: utf-8

# In[2]:


from bs4 import BeautifulSoup

html_doc = """
<html><head><title>The Office</title></head>
<body>
<p class="title"><b>The Office</b></p>
<p class="story">In my office, there are four officers,
<a href="http://example.com/YW" class="member">YW</a>,
<a href="http://example.com/JK" class="member">JK</a>,
<a href="http://example.com/YJ" class="member">YJ</a> and
<a href="http://example.com/KS" class="member">KS</a>
.</p>
<p class="story">...</p>
"""

soup = BeautifulSoup(html_doc, 'html.parser')

print(soup.prettify())


# In[3]:


soup.title #타이틀 태그 통째로 가져옴


# In[5]:


soup.title.text #타이틀 태그 내용을 추출


# In[6]:


soup.a #a 태그를 통째로 가져옴


# In[7]:


soup.find_all('a') #a 태그 모든 리스트를 모두 가져옴


# In[8]:


soup.find_all('a').text


# In[9]:


soup.find_all('a')[2] #3번째 멤버를 가져옴 


# In[10]:


member = soup.find_all('a')
for m in member:
    print(m.text)


# In[ ]:




