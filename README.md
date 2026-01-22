<h1 align="left">Risk Killer: 중소 식품기업의 미국 진출을 지원하는 AI 서비스</h1>

<p align="left">
  <a href="./Risk_killer.pdf">
    <img src="./Risk_Killer.png" width="900" alt="Risk Killer 발표 썸네일 (클릭하면 PDF)">
  </a>
</p>

<p align="left">
  <em>Risk Killer는 일반 LLM에 FDA 법규/리콜 데이터를 결합해 근거 링크와 수치 집계가 포함된 답변을 제공합니다.</em>
</p>

<div align="left">
  
[![Watch on YouTube](https://img.shields.io/badge/YouTube-FF0000?logo=youtube&logoColor=white)](https://youtu.be/fcc8h7o8pXs)
[![Streamlit App](https://img.shields.io/badge/Streamlit-App-green)](https://riskstremlaitapp.streamlit.app/)
[![PDF](https://img.shields.io/badge/Slides-PDF-blue)](./Risk_killer.pdf)

</div>


## 📋 프로젝트 개요

- **목적**: FDA 규제·리콜 데이터를 RAG로 연결해 국내 식품기업의 미국 진출 리스크를 빠르게 점검하고, 근거 기반 리포트를 생성하는 AI 서비스  
- **기간**: 2025.06–2025.08
- **팀 구성**: 4인  
- **수행 역할(황세영)**: eCFR/FDA 크롤링, ChromaDB 파이프라인 구축, UI설계, Streamlit 및 클라우드 배포


## 🏗️ 시스템 아키텍처
<p align="left"><img src="architecture.png" width="700" alt="Risk Killer Architecture"></p>


## 📌 주요 수행 과정

<details>
<summary><b>문제 정의</b></summary>

- 중소 식품기업의 미국 진출 시 **규제 적합성(성분·표시·첨가물·알레르겐)** 및 **리콜 리스크**를 선제 점검하기 어려움.
- 요구사항: 
  - 제품 정보 기반 규제 적합성 힌트 제공
  - 유사 리콜 사례 탐색
  - **집계 질의**(예: “최근 1년 알레르겐 리콜 Top5”) 응답
  - **근거 링크/원문 인용** 포함한 신뢰 가능한 답변

</details>

<details>
<summary><b>데이터 수집 및 전처리</b></summary>

- **크롤링 대상**
  - eCFR Title 21 최근 변경(Chapter 1 / Subchapter A·B·L)
  - FDA 리콜 페이지(발표일, 리콜 사유, 회수 범위 등 핵심 메타)
- **수집 방식**
  - Playwright 기반 비동기 크롤러로 목록/상세 크롤링
  - 필요 시 Selenium을 이용해 외부 차트/페이지 캡처 자동화
- **정규화 스키마**
  - `document_type`(guidance/regulation/recall)
  - `category`(additives/allergen/labeling/ecfr/usc 등)
  - `title`, `url`, `chunks` + 온톨로지(`ont_allergen`, `ont_contaminant`, `ont_recall_reason` 등)
- **텍스트 가공**
  - 한글 번역·요약 → 문단 단위 **chunking**
  - 불필요 태그/공백/표 제거, 날짜·수치 표준화
- **저장**
  - **ChromaDB**: chunk 임베딩 + 메타데이터 인덱싱
  - **SQLite**: 리콜 핵심 메타/집계 친화 필드 분리 저장(카운트·랭킹 질의용)

</details>

<details>
<summary><b>검색/생성 아키텍처</b></summary>

- **임베딩**: OpenAI `text-embedding-3-small`로 문단 임베딩
- **검색**: 시맨틱 검색 + 메타필터(문서유형/카테고리/기간)로 후보 문서 추출
- **응답 생성**: OpenAI API 기반 생성, **근거 인용(링크/인용문)** 포함
- **Function Calling**
  - 집계형 질문(개수/순위/기간)에 대해 SQLite/VectorStore 결과를 함수로 호출 → 표/요약 생성
- **오케스트레이션(LangGraph)**
  1) 질의 분류(집계형/설명형/혼합)  
  2) 라우팅(규제 vs 리콜)  
  3) 벡터 검색 + 필터  
  4) 필요 시 함수 호출(집계/랭킹)  
  5) 출처 인용 정리 → 최종 응답

</details>

<details>
<summary><b>한계 및 개선 계획</b></summary>

- 법률 자문이 아닌 **보조 도구**이므로 최종 판단은 전문가 검토 필요
- 원문 개정/번역 품질에 따른 시의성 이슈 → **변경 감지·재임베딩 파이프라인** 보강 예정
- 모델 한계로 인한 오답 가능 → **쿼리 재작성/반박-검증 체인** 도입 검토
- 식품 분야 중심 → 의약/화장품 등 **스키마 확장** 및 멀티도메인 테스트 계획

</details>



## 🗂️ 모듈 구조

```bash
risk_streamlit_app/
├── main.py                  # streamlit 엔트리
├── components/              # 탭 기반 UI모듈
│   ├── __init__.py    
│   ├── tab_tableau.py       # 시장 동향
│   ├── tab_news.py          # 식품 뉴스
│   ├── tab_regulation.py    # FDA 규제 관련 챗봇
│   ├── tab_recall.py        # FDA 리콜사례 챗
│   └── tab_export.py        # 기획안 요약 도우미
├── utils/
│   ├── data_loader.py              # 구글 드라이브와의 연동
│   ├── chat_regulation.py          # 규제 QA 파이프라인
│   ├── c.py                        # eCFR Title 21의 최근 변경 사항 수집·정제·번역·요약
│   ├── chat_common_functions.py    # 챗봇의 공통 기능 모듈
│   ├── agent_recall.py             # 리콜 Q\&A용 에이전트 컨트롤러
│   ├── function_calling_system.py  # Function Calling 엔진
│   ├── recall_prompts.py           # 프롬프트 템플릿 묶음
│   └── chart_downloader.py
├── data/
│   ├── chroma_db/         # 규제 벡터DB
│   ├── chroma_db_recall/  # 리콜 벡터DB
│   └── fda_recalls.db
├── requirements.txt
├── packages.txt
└── guide.png
```


## 🧰 주요 기술
<div align="left">

<img src="https://img.shields.io/badge/Streamlit-App-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white"/>
<img src="https://img.shields.io/badge/ChromaDB-Vector%20Store-3E77FF?style=for-the-badge"/>
<img src="https://img.shields.io/badge/OpenAI-API-5E5E5E?style=for-the-badge&logo=openai&logoColor=white"/>
<img src="https://img.shields.io/badge/LangGraph-Orchestration-4B5563?style=for-the-badge"/>
<img src="https://img.shields.io/badge/SQLite-DB-003B57?style=for-the-badge&logo=sqlite&logoColor=white"/>
<img src="https://img.shields.io/badge/pandas-Dataframe-150458?style=for-the-badge&logo=pandas&logoColor=white"/>
<img src="https://img.shields.io/badge/Plotly-Interactive%20Charts-3F4F75?style=for-the-badge&logo=plotly&logoColor=white"/>
<img src="https://img.shields.io/badge/Selenium-Web%20Chart%20Capture-43B02A?style=for-the-badge&logo=selenium&logoColor=white"/>
<img src="https://img.shields.io/badge/Google%20Drive-Integration-4285F4?style=for-the-badge&logo=googledrive&logoColor=white"/>

</div>


## 🖥️ 개발 환경
<div align="left">

<img src="https://img.shields.io/badge/Windows-11-0078D6?style=for-the-badge&logo=windows&logoColor=white"/>
<img src="https://img.shields.io/badge/VS%20Code-Editor-007ACC?style=for-the-badge&logo=visualstudiocode&logoColor=white"/>
<img src="https://img.shields.io/badge/Python-3.11-3776AB?style=for-the-badge&logo=python&logoColor=white"/>
<img src="https://img.shields.io/badge/Streamlit-Cloud%20(Deploy)-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white"/>
<img src="https://img.shields.io/badge/ChromeDriver-Automation-4285F4?style=for-the-badge&logo=googlechrome&logoColor=white"/>
<img src="https://img.shields.io/badge/Tableau-Public-005571?style=for-the-badge&logo=tableau&logoColor=white"/>

</div>
