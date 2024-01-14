# 딥러닝 아키텍처를 활용한 자연어 응답기반 MBTI 분석
## Natural Language Response-Based MBTI Analysis
</br>

`2023년 11월 졸업작품으로 제작된 프로젝트입니다.`
</br>

#### OVERVIEW
본 작품은 자연어 처리(NLP)를 기반으로 하여 인간의 심리적 특성을 16가지 성격 유형으로 분류하는 MBTI 검사의 새로운 지표를 제시한다. </br>
기존의 MBTI 검사는 사용자가 객관식 질문에 응답하도록 설계되어 있어 인간의 복잡한 심리 상태를 파악하기에는 한계가 존재한다.
이를 개선하기 위해 **주관식 응답을 기반으로 한 새로운 검사방식을 제안**하여, 보다 세밀하고 정교하게 피실험자의 성격 유형을 예측할 수 있다.</br>

#### EXPECTANCY EFFECTS
- 전통적인 MBTI 검사와 달리, 텍스트로 표현된 사용자 응답을 활용하여 MBTI 성격 유형 분석 및 예측
- LSTM과 Bi-LSTM을 사용하여 5가지의 모델 제안 및 비교
- Pre-trained Model(KoGPT-2, GPT-4)을 활용한   데이터 증강 기법 사용
- 적은 양의 데이터 셋으로도 높은 예측 정확도를 보임

___

<img src="https://github.com/Ryuhamaa/MBTI-PRJ/assets/90309728/c8dc0bb6-4789-4b4a-a349-16acb55b89c2" width="600" height="280"/>
</br></br>

1. 데이터 수집 - 데이터 증강</br>
2. 모델학습(5가지 모델 제안, 택 1)
3. web 구현
