import tensorflow as tf
import re
import konlpy
import sentencepiece as spm
import pandas as pd
import random
from konlpy.tag import Mecab
from keras.models import load_model
import numpy as np
from tensorflow.keras.preprocessing.sequence import pad_sequences



mecab = Mecab(dicpath=r"C:/mecab/mecab-ko-dic")

#훈련된 서브워드 토크나이저 모델 불러오기
saved_path = r'C:/Users/RACS/MBTI_prj_backup/data/m.model'
sp = spm.SentencePieceProcessor()
sp.Load(saved_path)#m.model 불러오기

#훈련된 Bi-LSTM모델 불러오기
EI_model_save_path = r'C:/Users/RACS/MBTI_prj_backup/data/TrainedModel/EI_best_model.h5'
EI_loaded_model = tf.keras.models.load_model(EI_model_save_path)
NS_model_save_path = r'C:/Users/RACS/MBTI_prj_backup/data/TrainedModel/NS_best_model.h5'
NS_loaded_model = tf.keras.models.load_model(NS_model_save_path)
FT_model_save_path = r'C:/Users/RACS/MBTI_prj_backup/data/TrainedModel/FT_best_model.h5'
FT_loaded_model = tf.keras.models.load_model(FT_model_save_path)
JP_model_save_path = r'C:/Users/RACS/MBTI_prj_backup/data/TrainedModel/JP_best_model.h5'
JP_loaded_model = tf.keras.models.load_model(JP_model_save_path)


#사전에 입력된 질문 불러오기
question = pd.read_csv(r'C:/Users/RACS/MBTI_prj_backup/data/total_question.csv')


################################################################
# 질의 응답 로직 구현
def get_question(index):
    return qa_df.at[index,'Question']
def save_response(index,response):
    qa_df.at[index, 'Answer'] = response








################################################################
# 사용자 입력을 분석하는 로직 구현
check_mbti = False

#ectracted 단어 설정
def extract_words(pos_list): #pos_list는 'pos_tagged'에 들어있는 word와 tag를 추출한다.
  target_tags = ['NNG', 'NNP', 'VV', 'VA', 'MAG', 'VA+ETM']
  return [word    for word,tag in pos_list   if tag in target_tags]

#extract word 추출
def tokenize_tagged(text):
  tagged_text = mecab.pos(text)#품사 태깅
  extracted_words = extract_words(tagged_text)#특정단어만 추출하여 저장
  return extracted_words

#예측 메인 모델
def predict_sentence(model, sentence, max_len):
    # 문장 전처리
    new_sentence = re.sub("[^가-힣ㄱ-ㅎㅏ-ㅣ\\s]", "", sentence)
    new_sentence_morphs = tokenize_tagged(new_sentence)

    tokens_1 = sp.EncodeAsPieces(new_sentence)
    tokens_2 = sp.EncodeAsPieces(new_sentence_morphs)
    tokens_encode_1 = sp.EncodeAsIds(new_sentence)
    tokens_encode_2 = sp.EncodeAsIds(new_sentence_morphs)
    #중첩 리스트가 있을경우 평탄화
    if any(isinstance(i, list) for i in tokens_encode_2):
      tokens_encode_2 = [item for sublist in tokens_encode_2 for item in sublist]

    #패딩
    padded_sequences_1 = pad_sequences([tokens_encode_1], maxlen=max_len, padding='post')
    padded_sequences_2 = pad_sequences([tokens_encode_2], maxlen=max_len, padding='post')

    # 예측
    prediction_1 = model.predict(padded_sequences_1)
    prediction_2 = model.predict(padded_sequences_2)
    prediction_value_1 = prediction_1[0][0]
    prediction_value_2 = prediction_2[0][0]
    
    #예측값 계산
    result_mbti_value = (prediction_value_1 + prediction_value_2)/2.0

    return result_mbti_value


   
   

#최종 MBTI 판단 함수
def pred_mbti(what_type, pred_value):
    if what_type == 1:
        mbti_result = 'E' if pred_value >= 0.5 else 'I'
    elif what_type == 2:
        mbti_result = 'N' if pred_value >= 0.5 else 'S'
    elif what_type == 3:
        mbti_result = 'F' if pred_value >= 0.5 else 'T'
    else:
        mbti_result = 'J' if pred_value >= 0.5 else 'P'

    return mbti_result

      
   
#예측 확률 계산 함수
def cal(pred):
  if pred >=0.5: 
    pred = pred * 100
  elif pred < 0.5: 
    pred = 100 - pred * 100
  pred = round(pred, 2)
  return pred

#web.py에서 실행되는 실시간 응답분석
def analyze_response(index):
    model = None
    what_type = qa_df.loc[index, 'what_type']

    # what_type에 따라 적절한 모델 선택
    if what_type == 1:
        model = EI_loaded_model
        max_len=40
    elif what_type == 2:
        model = NS_loaded_model
        max_len=29
    elif what_type == 3:
        model = FT_loaded_model
        max_len=35
    elif what_type == 4:
        model = JP_loaded_model
        max_len=31

    if model:
      pred = predict_sentence(model, str(qa_df['Answer'][index]), max_len)
      qa_df.at[index, 'pred'] = pred #pred에 저장
    
    print(qa_df)

"""def analyze_type():
   pred = qa_df['pred'].sum() / 2 #예측값 계산
   percent = cal(pred)# 퍼센트 계산
   MBTI_type = pred_mbti(pred)#유형 계산
   #qa_df['type'] = MBTI_type
   return pred, MBTI_type, percent"""

def analyze_type():
    result = {}
    for what_type in range(1, 5):
         
        pred_sums = qa_df.groupby('what_type')['pred'].sum()
        pred_counts = qa_df.groupby('what_type')['pred'].count()

        total_pred = pred_sums[what_type] / pred_counts[what_type] #평균 계산

        percent = cal(total_pred)# 퍼센트 계산
        MBTI_type = pred_mbti(what_type, total_pred)#유형 계산
        

        result[what_type] = {'total_pred':total_pred, 'percent':percent, 'MBTI_type':MBTI_type}
        print(result)

    return result  # 이 부분은 필요에 따라 수정    

# 필요한 전처리 및 후처리 함수 구현



################################################################
#데이터 프레임 초기화
qa_df = pd.DataFrame(columns = ['Question', 'Answer', 'pred', 'what_type']) 

# what_type별로 질문 뽑기 및 각 질문의 what_type 저장
def get_random_questions_and_types(question, num_questions_per_type):
    random_questions = []
    what_type_list = []
    for what_type, num_questions in num_questions_per_type.items():
        questions_of_type = question[question['what_type'] == what_type]
        
        # 실제 질문 수보다 요청된 샘플 크기가 큰 경우 조정
        actual_num_questions = min(len(questions_of_type), num_questions)

        if actual_num_questions > 0:  # 질문이 존재하는 경우에만 처리
            random_rows = random.sample(questions_of_type.index.tolist(), actual_num_questions)
            for row in random_rows:
                random_questions.append(questions_of_type.loc[row]['Question'])
                what_type_list.append(what_type)
    return random_questions, what_type_list

def initialize_chat(index):
   global qa_df
   qa_df = pd.DataFrame(columns = ['Question', 'Answer', 'pred', 'what_type']) 

   # 랜덤하게 10개의 행을 선택
   num_questions_per_type = {1: 2, 2: 3, 3: 3, 4: 3}  # 예: what_type 1은 2개, what_type 2는 3개
   random_questions, what_type_list = get_random_questions_and_types(question, num_questions_per_type)
   #random_rows = random.sample(range(len(question)), 11)

   qa_df['Question'] = random_questions 
   qa_df['what_type'] = what_type_list 

   new_question = get_question(index)
   return new_question

def get_question(index):
    # qa_df의 크기를 확인하고 index가 유효한 범위 내에 있는지 확인
    return qa_df.iloc[index]['Question']
    
# qa_df 반환 함수
def get_qa_df():
    global qa_df
    return qa_df


"""#데이터 프레임 초기화 로직
def reset_dataframe():
   global qa_df
   #qa_df = pd.DataFrame(columns = ['Question', 'Answer', 'pred', 'type']) 
   random_question = random.sample(question['Question'].tolist(), 2)#3개 랜덤하게 뽑기
   qa_df['Question'] = random_question
   pass

def get_question(index):
    return qa_df.at[index,'Question']

def get_question(index):#단일질문 반환
    return qa_df.iloc[index]['Question']


def initialize_chat(index):
   reset_dataframe()
   new_question = get_question(index)
   return new_question
   
   
   # 질의 응답 로직 구현
    def get_question(index):
        return qa_df.at[index,'Question']
    def save_response(index,response):
        qa_df.at[index, 'Answer'] = response
    """




#질의응답 데이터 프레임
#qa_df = pd.DataFrame(columns = ['Question', 'Answer', 'pred', 'type'])
#random_question = random.sample(question['Question'].tolist(), 2)#3개 랜덤하게 뽑기
#qa_df['Question'] = random_question


