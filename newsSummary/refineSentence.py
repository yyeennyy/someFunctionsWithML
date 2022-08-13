######## 종합 : refineSentence ######
def refineSentence(text):
  new_text = dropSentence(text)
  new_text = dropWords(new_text)
  new_text = insertDot(new_text)
  return new_text
#####################################




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
  
  
# 제외대상 문장 드롭
def dropSentence(text):
  def getTitle(text):
    enter = "\n"
    idx = text.find(enter)
    return text[:idx]
  title = getTitle(text)
  except_words = ["제공:"]
  except_regex = "[((?!입력|수정).)*$ ]{2,3}([0-9]{4}[\/. ((?!년).)*$]{1,3}[0-9]{1,2}[\/. ((?!월).)*$]{1,3}[0-9]{1,2}[\/. ((?!일).)*$]{0,2})"
  lines = text.split("\n")
  lines = list(set(lines))
  new_text = ""
  for line in lines:
    if bool(re.search(except_regex, line)):
      continue
    if len(line) == 1 or len(line) == 2 or len(line) == 0:
      continue
    for word in except_words:
      if word in line:
        continue
    if line == title:
      continue
    new_text = new_text + line + "\n"
  return new_text.rstrip()


# 제외 문구 삭제 후 삽입
def dropWords(text):
  clean_regex1 = "[\(\[][|\s -=+,#/\?:^.@*※~ㆍ!』‘|`…》·가-힣]{3,15}[\)\]]"
  return re.sub(clean_regex1, "", text)

# 점 삽입
def insertDot(text):
  new_text = ""
  divided = text.split("\n")
  for line in divided:
    line = line.strip()
    if line.strip()[-1:] != "." :
      new_text = new_text + line + ".\n"
    else:
      new_text = new_text + line + "\n"
  return new_text

