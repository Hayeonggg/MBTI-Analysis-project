# 딥러닝 아키텍처를 활용한 자연어 응답기반 MBTI 분석
## Natural Language Response-Based MBTI Analysis
`졸업작품으로 2023년 제작된 1인 프로젝트입니다.`
- 프로젝트 기간 : 2023.08 ~ 2023.11 (약 4개월)</br>
~~- (추후, 예측방법 개선/트랜스포머 모델 사용/시스템 구성도 수정 예정)~~

</br>

<p align="center">
<img src="https://github.com/Ryuhamaa/MBTI-PRJ/assets/90309728/c8dc0bb6-4789-4b4a-a349-16acb55b89c2" width="600" height="280"/>
</p>

### OVERVIEW
본 프로젝트는 자연어 처리(NLP)를 기반으로 하여 인간의 심리적 특성을 16가지 성격 유형으로 분류하는 **MBTI 검사**의 **새로운 지표를 제시**합니다. </br>
기존의 MBTI 검사는 사용자가 객관식 질문에 응답하도록 설계되어 있어 인간의 복잡한 심리 상태를 파악하기에는 한계가 존재합니다.
이를 개선하기 위해 **주관식 응답을 기반으로 한 새로운 검사방식을 제안**하여, 보다 세밀하고 정교하게 피실험자의 성격 유형을 예측할 수 있습니다.</br>

### EXPECTANCY EFFECTS
- 전통적인 MBTI 검사와 달리, 텍스트로 표현된 사용자 응답을 활용하여 MBTI 성격 유형 분석 및 예측
- LSTM과 Bi-LSTM을 사용하여 5가지 Model 제안 및 비교
- Pre-trained Model(KoGPT-2, GPT-4)을 활용한 Data Augmentation
- 적은 양의 데이터 셋으로도 높은 예측 정확도를 보임

### PROJECT INTRODUCTION
Velog Link >> https://velog.io/@bluebarry3/%EC%A1%B8%EC%9E%91-%EC%A3%BC%EC%A0%9C%EB%B0%9C%ED%91%9C

</br>

___

### ▶ DEMO

<p align="center">
  <img src="https://github.com/Ryuhamaa/MBTI-Analysis-project/assets/90309728/075810f0-ec34-4990-8f20-a8eb2c9fa234" width="600" height="430"/>
</p>
</br>


### ▶ SYSTEM ARCHITECTURE
<p align="center">
  <img src="https://github.com/Ryuhamaa/MBTI-PRJ/assets/90309728/f8e94add-7095-432e-92a1-1e9e4a5bd849"/>
</p>
</br>

<p align="center">
  <img src="https://github.com/Hayeonggg/MBTI-Analysis-project/assets/90309728/f064acb4-c126-4908-b3cd-e1008fe829d2"width="550" height="320"/>
</p>

</br></br></br></br>
___

## ▶ DEVELOPMENT SEQUENCE
1. Data Collection (gpt4, kogpt-2.5 생성 이용)
2. Data Augmentation [(Github Link)](https://github.com/Hayeonggg/Easy-Data-Augmentation-Techniques) 
3. 5가지 모델 제안 및 최종선정 모델 - [Reference](https://github.com/Hayeonggg/LSTM-Personality-Analysis-2023/blob/main/2023%EB%85%84%20%EC%9C%B5%EB%B3%B5%ED%95%A9%EC%A7%80%EC%8B%9D%ED%95%99%ED%9A%8C%20%EC%B6%94%EA%B3%84%ED%95%99%EC%88%A0%EB%8C%80%ED%9A%8C%20%EB%85%BC%EB%AC%B8%EC%A7%91%20-%20%EC%9C%A0%ED%95%98%EC%98%81.pdf) / [Poster](https://github.com/Hayeonggg/LSTM-Personality-Analysis-2023/blob/main/2023%20%EC%B6%94%EA%B3%84%ED%95%99%EC%88%A0%EB%8C%80%ED%9A%8C%20%ED%8F%AC%EC%8A%A4%ED%84%B0%20-%20%EC%9C%A0%ED%95%98%EC%98%81.pdf)
4. MBTI 예측 방법 - [GitHub](https://github.com/Hayeonggg/MBTI-Analysis-project/tree/main/answer_prediction)
5. web 구현(로컬환경) - [GitHub](https://github.com/Hayeonggg/MBTI-Analysis-project/tree/main/web)

___




### 1. Data Collection / 2. Data Augmentation
<p align="center">
  <img src="https://github.com/Hayeonggg/MBTI-Analysis-project/assets/90309728/d5974d62-c119-4cb1-9c2d-fc36c29fa337"width="750" height="350"/>
</p>


<p align="center">
  <img src="https://github.com/Hayeonggg/MBTI-Analysis-project/assets/90309728/4bada387-cd2d-4f95-9c9d-ce49b4a84a47"width="400" height="250"/>
</p>
<p align="center">
  <img src="https://github.com/Hayeonggg/MBTI-Analysis-project/assets/90309728/723ac19d-00f6-4e31-b377-9f2f783970d6"/>
</p>

</br></br>

### 3. 5가지 모델 제안 및 최종선정 모델
### >> 실험방법
<p align="center">
  <img src="https://github.com/Hayeonggg/MBTI-Analysis-project/assets/90309728/9a13d761-38ef-4659-b7b2-abd871f31db3"width="680" height="300"/>
</p>
<p align="center">
  <img src="https://github.com/Hayeonggg/MBTI-Analysis-project/assets/90309728/614c8cdf-c690-42d0-ab65-4a80830c9569"width="680" height="320"/>
</p>
<p align="center">
  <img src="https://github.com/Hayeonggg/MBTI-Analysis-project/assets/90309728/870336b3-68f1-46fa-a7ca-6b53899c8c76"width="680" height="320"/>
</p>

</br>

### >> 실험결과
<p align="center">
  <img src="https://github.com/Hayeonggg/MBTI-Analysis-project/assets/90309728/0edc628e-c8cc-4dcb-a784-36e2f2276019"width="600" height="320"/>
</p>
<p align="center">
  <img src="https://github.com/Hayeonggg/MBTI-Analysis-project/assets/90309728/d6415699-afac-4ff7-ac3e-45d5df2d92b3"width="600" height="320"/>
</p>

</br></br>

### 4. MBTI 예측 방법 --> `(추후 개선 예정)`
### >> MBTI 예측 방법 구조화
<p align="center">
  <img src="https://github.com/Hayeonggg/MBTI-Analysis-project/assets/90309728/196767a1-5800-44d8-a5bb-cfabc587063d"width="650" height="400"/>
</p>
<p align="center">
  <img src="https://github.com/Hayeonggg/MBTI-Analysis-project/assets/90309728/9be1f1c0-c66f-4ae4-92c4-2477cb06cd1a"width="650" height="400"/>
</p>

### >> '사용자 응답 기반 MBTI 예측' 결과
  <p align="center">
  <img src="https://github.com/Hayeonggg/MBTI-Analysis-project/assets/90309728/ed2acc0b-c4ad-4843-b992-71e67a8f9341"width="500" height="460"/>
</p>
<p align="center">
  <img src="https://github.com/Hayeonggg/MBTI-Analysis-project/assets/90309728/23f22ab3-ad14-4dbb-933f-21c04266ecda"width="500" height="300"/>
</p>

</br></br>

### 5. web 구현(local)
- Flask 이용
<p align="center">
  <img src="https://github.com/Hayeonggg/MBTI-Analysis-project/assets/90309728/a8ea3b93-fda2-42f7-a5ad-3e8c6dc16641"/>
</p>

</br></br></br>
