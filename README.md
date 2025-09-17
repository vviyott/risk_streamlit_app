## Risk Killer: 중소 식품기업의 미국 진출을 지원하는 AI 서비스

[![Watch on YouTube](https://img.shields.io/badge/YouTube-FF0000?logo=youtube&logoColor=white)](https://youtu.be/fcc8h7o8pXs)
[![Streamlit App](https://img.shields.io/badge/Streamlit-App-green)](https://riskstremlaitapp.streamlit.app/)
[![PDF](https://img.shields.io/badge/Slides-PDF-blue)](./Risk_killer.pdf)

<p align="center">
  <a href="./Risk_killer.pdf">
    <img src="./Risk_Killer.png" width="900" alt="Risk Killer 발표 썸네일 (클릭하면 PDF)">
  </a>
</p>

### 📄 프로젝트 개요

- **목적**: 미국 식품·의약 규제(FDA)와 리콜 데이터를 기반으로 국내 식품기업의 미국 진출 가능성/리스크를 빠르게 점검하고, 근거가 포함된 답변과 리포트를 제공.
- **주제**: LLM+LangGraph 오케스트레이션, eCFR/FDA 크롤링→번역·요약→정규화→ChromaDB·SQLite 적재, Function Calling 기반 통계 질의 + RAG.
- **기간**: 2025.04–2025.09 (진행)
- **팀 구성**: 4인
- **담당 역할(황세영)**: LangGraph 설계, eCFR/FDA 크롤러·번역/요약 파이프라인, ChromaDB/SQLite 스키마, Function Calling 도구, Streamlit UI.


---

## Quickstart

```bash
# 1) 클론 및 진입
git clone https://github.com/vviyott/risk_streamlit_app.git
cd risk_streamlit_app

# 2) 가상환경 & 설치 (Windows 예시)
python -m venv .venv && .\.venv\Scripts\activate
pip install -r requirements.txt

# 3) 환경변수(예: OpenAI 키) 설정 후 실행
# macOS/Linux: export OPENAI_API_KEY=...
# Windows(PowerShell): $env:OPENAI_API_KEY="..."
streamlit run main.py
