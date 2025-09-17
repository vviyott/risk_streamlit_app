## Risk Killer: 중소 식품기업의 미국 진출을 지원하는 AI 서비스



<p align="left">
  <a href="./Risk_killer.pdf">
    <img src="./Risk_Killer.png" width="900" alt="Risk Killer 발표 썸네일 (클릭하면 PDF)">
  </a>
</p>

> Risk Killer는 일반 LLM에 법규/리콜 전문 데이터를 결합해 근거 링크와 수치 집계가 포함된 답변을 제공합니다.
[![Watch on YouTube](https://img.shields.io/badge/YouTube-FF0000?logo=youtube&logoColor=white)](https://youtu.be/fcc8h7o8pXs)
[![Streamlit App](https://img.shields.io/badge/Streamlit-App-green)](https://riskstremlaitapp.streamlit.app/)
[![PDF](https://img.shields.io/badge/Slides-PDF-blue)](./Risk_killer.pdf)


### 📋 프로젝트 개요

- **목적**: FDA 규제·리콜 데이터를 RAG로 연결해 국내 식품기업의 미국 진출 리스크를 빠르게 점검하고, 근거 기반 리포트를 생성하는 AI 서비스
- **기간**: 2025.04–2025.09
- **팀 구성**: 4인
- **수행 역할(황세영)**: eCFR/FDA 크롤링, ChromaDB 파이프라인 구축, UI설계, Streamlit 및 클라우드 배포




### 🏗️ 시스템 아키텍처

<p align="left"><img src="architecture.png" width="700" alt="Risk Killer Architecture"></p>


주요 수행 과정
1) 문제 정의

중소 식품기업이 미국 진출 시 규제 적합성(성분·표시·첨가물·알레르겐)과 리콜 리스크를 사전에 점검하기 어려움.

요구사항: 제품 정보 기반 규제 적합성 힌트, 유사 리콜 사례 탐색, 수치 질의(예: “최근 1년 알레르겐 리콜 Top5”), 근거 링크·원문 인용.

2) 데이터 수집 및 전처리

크롤링: eCFR Title 21 최근 변경(Chapter 1 / Subchapter A·B·L)과 FDA 리콜 페이지.

정규화: document_type(guidance/regulation/recall), category(additives/allergen/labeling/ecfr/usc 등), title/url/chunks와 도메인별 온톨로지(ont_allergen, ont_contaminant, ont_recall_reason 등) 스키마 통합.

벡터화: 한글 번역·요약 텍스트를 문단 단위로 분할하여 ChromaDB에 임베딩 저장, 메타데이터 필터로 조건 검색.

요약·통계 저장: 리콜 핵심 메타와 집계에 적합한 필드를 SQLite에 별도 보관.

3) 기대효과

규정·가이던스·리콜 근거 인용형 답변으로 의사결정 신뢰성 향상.

키워드가 아닌 시멘틱 검색과 조건 필터링으로 탐색 효율화.

Function Calling을 통해 개수/순위/기간별 집계 요청에 즉시 응답.

Streamlit UI로 분석–증거–요약 보고까지 단일 화면에서 수행.

4) 한계점

법률 자문이 아닌 보조 도구로, 최종 준수 판단은 전문가 검토 필요.

크롤링/번역 품질과 원문 개정에 따른 시의성 의존.

RAG로 할루시네이션을 줄였으나 모델 한계에 따른 오답 가능.

현재 식품 분야 중심(확장 설계는 가능).
## 프로젝트 구조

```bash
risk_streamlit_app/
├── main.py                  # streamlit 엔트리
├── components/              # 탭 기반 UI모듈
│   ├── __init__.py    
│   ├── tab_tableau.py       #
│   ├── tab_news.py
│   ├── tab_regulation.py
│   ├── tab_recall.py
│   └── tab_export.py
├── utils/
│   ├── data_loader.py
│   ├── chat_regulation.py
│   ├── c.py
│   ├── chat_common_functions.py
│   ├── agent_recall.py
│   ├── function_calling_system.py
│   ├── recall_prompts.py
│   └── chart_downloader.py
├── data/
│   ├── chroma_db/         # 규제 벡터DB
│   ├── chroma_db_recall/  # 리콜 벡터DB
│   └── fda_recalls.db
├── requirements.txt
├── packages.txt
└── guide.png
