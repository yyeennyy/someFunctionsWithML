######################################################################
def txtFileUpdate(raw_url, done_url):
  if getRawNews(raw_url) == "추가사항 없음":
    return "추가사항 없음"
  
  makeSummaryFile(raw_url, done_url)
  reloadRawNews(raw_url)
  return "완료"
######################################################################
# 사용예시
raw_url = "/content/drive/MyDrive/대회준비/txt/raw.txt"
done_url = "/content/drive/MyDrive/대회준비/txt/done.txt"
txtFileUpdate(raw_url, done_url)
######################################################################




## 추가 대상 raw news 가져오기
def getRawNews(url):
  news_bundle = []
  one = ""
  end_idx = 0
  with open(url, "r") as raw:
    try:
      raw_news_list = raw.readlines()
      file_length = len(raw_news_list)
      added_idx = raw_news_list.index("(added)\n")
      for i, line in enumerate(list(reversed(raw_news_list[:added_idx]))):
        if line == "(end)\n":
          end_idx = added_idx - i - 1
          break
    except:
      return "추가사항 없음"

    while end_idx < added_idx:
      # 각 뉴스 하나를 하나의 String으로 새 리스트에 저장
      news_line_list = raw_news_list[end_idx+1:added_idx-1]
      for line in news_line_list:
        one += line
      news_bundle.append(one.strip('\n'))
      one = ""

      # 첫 서치 이후
      # end index 갱신
      end_idx = added_idx + 1
      try:
        plus = raw_news_list[end_idx:].index("(added)\n")
        added_idx += plus + 1
      except:
        break;
        
    return news_bundle


# 요약 뉴스 만들어서 추가하기 - done.txt :
def makeSummaryFile(raw_url, done_url):
  raw_bundle = getRawNews(raw_url)
  for text in raw_bundle:
    summary_list = getSummaryList(text)
    with open(done_url, "a") as done:
      for line in summary_list:
        done.write(line + "\n")
      done.write("(end)\n")
  return True

## 추가한 raw news 처리하기 - "(added)\n" 표시 없애기
def reloadRawNews(raw_url):
  with open(raw_url, "r") as raw:
    raw_news_list = raw.readlines()
  with open(raw_url, "w") as raw:
    while "(added)\n" in raw_news_list:    
      print("success")
      raw_news_list.remove("(added)\n")
    for line in raw_news_list:
      if line != "\n":
        raw.write(line + "\n")
  return True
