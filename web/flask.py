from flask import Flask, request, render_template, redirect, url_for
from flask import jsonify
import chat
import os
import csv
import pandas as pd
import numpy as np

app = Flask(__name__)

# 템플릿 디렉토리 설정
app.template_folder = 'templates'

# 전역변수로 현재 질문 인덱스 관리
question_index = 0 


# 사용자의 이름, 질문, 응답 등을 저장할 데이터 프레임 초기화
save_user_answer = pd.DataFrame(columns=['name'])


#인트로 
@app.route('/', methods=['GET'])
def home():
    if request.method == 'POST':
        if 'yes' in request.form:
            return redirect(url_for('name_input'))
        elif 'no' in request.form:
            # 시작 메시지 출력
            return render_template('index.html')
            
    return render_template('index.html')
    
#이름 저장
@app.route('/user', methods=['POST'])
def name_input():
    # POST 요청으로 받은 사용자의 이름을 처리합니다.
    if request.method == 'POST':
        user_name = request.form['name']
        
        # DataFrame에 이름을 추가합니다.
        new_index = len(save_user_answer)
        save_user_answer.loc[new_index] = {'name': user_name}
        print(save_user_answer)

        # 제출된 이름을 JSON 형식으로 반환합니다.
        return jsonify({"name": user_name})


main_index = 0 #사람 세기
count = 1#한사람당 질문-응답 개수


#질문 random 맨처음. 초기화
@app.route('/start', methods=['GET'])
def start_chat():
    global question_index
    global main_index
    global count
    global save_user_answer
    count = 1# 질의응답 개수는 초기화

    question_index = 0  # question_index 초기화
    new_question = chat.initialize_chat(question_index)

    return jsonify({'question': new_question})

def return_results():
    # 결과를 담을 딕셔너리 초기화
    json_results = {'result': True}

    # 각 what_type에 대한 결과를 딕셔너리에 추가
    for what_type in range(1, 5):
        pred_column_name = f'pred_{what_type}'
        per_column_name = f'percent_{what_type}'
        type_column_name = f'MBTI_type_{what_type}'

        json_results[pred_column_name] = save_user_answer[pred_column_name].iloc[0]
        json_results[per_column_name] = save_user_answer[per_column_name].iloc[0]
        json_results[type_column_name] = save_user_answer[type_column_name].iloc[0]

    return jsonify(json_results)


#응답
@app.route('/submit', methods=['POST'])
def submit():
    global question_index
    global count
    global main_index
    global save_user_answer
    response = request.form['response']
    chat.save_response(question_index, response)
    chat.analyze_response(question_index)#실시간 응답 분석

    qa_df = chat.get_qa_df()
    what_type = qa_df.loc[question_index, 'what_type']  # 현재 질문의 what_type
    q_column_name = f'q{what_type}_{count}'  # 질문 열 이름 생성
    a_column_name = f'a{what_type}_{count}'  # 응답 열 이름 생성

    #save_user_answer에 질문 저장
    cu_question = qa_df.loc[question_index, 'Question']  # 현재 질문의 what_type
    save_user_answer.loc[main_index, q_column_name] = cu_question

    #save_user_answer에 응답 저장
    save_user_answer.loc[main_index, a_column_name] = response


    #질문 인덱스 증가
    question_index += 1
    count+=1
    
    print(save_user_answer)

    if question_index == 11:
        #mbti 분석
        result = chat.analyze_type()

        for what_type, data in result.items():
            pred_column_name = f'pred_{what_type}'
            per_column_name = f'per_{what_type}'
            type_column_name = f'type_{what_type}'

            save_user_answer[pred_column_name] = data['total_pred']
            save_user_answer[per_column_name] = data['percent']
            save_user_answer[type_column_name] = data['MBTI_type']


        # 열의 값을 결합하여 새 열에 저장
        save_user_answer['user_mbti'] = (
            save_user_answer['type_1'].astype(str) + 
            save_user_answer['type_2'].astype(str) +
            save_user_answer['type_3'].astype(str) +
            save_user_answer['type_4'].astype(str)
        )

        print(save_user_answer)#확인용
        main_index+=1 #두번째 사람.. 세번째 사람..
        
        print(save_user_answer.columns)
        
        #return jsonify({'result':True, 'MBTI_data':result_data})
        #save_user_answer_dict = save_user_answer.to_dict(orient='records')
        """return jsonify({'result': True, 'MBTI_type': user_mbti, 'per_type_1':per_type_1, 
                        'per_type_2':per_type_2, 'per_type_3':per_type_3, 'per_type_4':per_type_4})"""
        return jsonify({
            'result': True,
            'user_mbti': save_user_answer['user_mbti'].to_dict(),
            'per_1': save_user_answer['per_1'].to_dict(),
            'per_2': save_user_answer['per_2'].to_dict(),
            'per_3': save_user_answer['per_3'].to_dict(),  
            'per_4': save_user_answer['per_4'].to_dict(),
        })
    else:
        next_question = chat.get_question(question_index)
        
        return jsonify({'result': False, 'question': next_question})
    
@app.route('/submit_real_mbti', methods=['POST'])
def submit_real_mbti():
    real_mbti = request.form['real_mbti']
    save_user_answer['real_mbti'] = real_mbti
    return jsonify({'status': 'success'})
    
if __name__ == '__main__':
    try:
        app.run(host='localhost', port=5000)
    except KeyboardInterrupt:
        # KeyboardInterrupt 예외가 발생하면 (예: Ctrl+C 입력)
        print("Flask application is stopping...")
    finally:
        # 애플리케이션이 종료될 때 실행되는 코드
        file_path = '/Users/RACS/web/saved_data/test_result.csv'  # CSV 파일을 저장할 경로
        # 파일이 이미 존재하는지 체크
        file_exists = os.path.isfile(file_path)

        
        
        # save_user_answer 데이터프레임을 CSV 파일에 저장
        # 파일이 존재하면, 헤더를 제외하고 데이터만 추가
        # 파일이 존재하지 않으면, 헤더를 포함하여 새로운 파일을 생성
        #save_user_answer.to_csv(file_path, index=False, encoding='utf-8-sig')
        save_user_answer.to_csv(file_path, mode='a', index=False, header=not file_exists, encoding='utf-8-sig')
        print("Data saved to CSV.")

