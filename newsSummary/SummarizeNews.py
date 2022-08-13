######## 최종 ############################################
# page
def getSummaryList(text):
  title = getTitle(text)
  date = getDate(text)
  text = refineSentence(text)
  summary = summarizeNews(text) # 이 함수에 대한 내용입니다
  result = title + "\n" + date + "\n" + summary
  return result.split("\n")
##########################################################



def summarizeNews(text):
  # 가정 : 문장은 모두 \로 구분된다.
  sentences = re.split("\n", text)

  data = []
  for sentence in sentences:
      if(sentence == "" or len(sentence) == 0):
          continue
      temp_dict = dict()
      temp_dict['sentence'] = sentence
      temp_dict['token_list'] = komoran.nouns(sentence)
      data.append(temp_dict)
  df = pd.DataFrame(data)

  # 무효한 결과 제외
  index_list = []
  for index in range(len(df)):
    if df['token_list'][index] == []:
      index_list.append(index)
  # index_list
  df = df.drop(index_list)

  similarity_matrix = []
  for i, row_i in df.iterrows():
      i_row_vec = []
      for j, row_j in df.iterrows():
          if i == j:
              i_row_vec.append(0.0)
          else:
              intersection = len(set(row_i['token_list']) & set(row_j['token_list']))
              log_i = math.log(len(set(row_i['token_list'])))
              log_j = math.log(len(set(row_j['token_list'])))
              similarity = intersection / (log_i + log_j + 1e-10)
              i_row_vec.append(similarity)
      similarity_matrix.append(i_row_vec)
      
  weightedGraph = np.array(similarity_matrix)
  R = pagerank(weightedGraph)
  R = R.sum(axis=1)
  indexs = R.argsort()[-3:]

  summary_result = ""
  for index in sorted(indexs):
      summary_result += df['sentence'][index] + "\n"

  return summary_result.rstrip()






# 핵심 ML : pagerank
def pagerank(x, df=0.85, max_iter=30):
    assert 0 < df < 1
    # initialize
    A = preprocessing.normalize(x, axis=0, norm='l1')
    R = np.ones(A.shape[0]).reshape(-1,1)
    bias = (1 - df) * np.ones(A.shape[0]).reshape(-1,1)
    # iteration
    for _ in range(max_iter):
        R = df * (A * R) + bias
    return R
  
  
  
  
  # 단순히 getTitle, getDate
  # Title은 맨 위에 있다고 가정
  
def getDate(text):
  date_regex = "([0-9]{4}[\/. ((?!년).)*$]{1,3}[0-9]{1,2}[\/. ((?!월).)*$]{1,3}[0-9]{1,2}[\/. ((?!일).)*$]{0,2})"
  m = re.search(date_regex, text)
  if m == None:
    return "날짜 정보 없음"
  return m.group(0).strip()

def getTitle(text):
  enter = "\n"
  idx = text.find(enter)
  return text[:idx]


