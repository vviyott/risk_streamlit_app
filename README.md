# Risk Killer: 중소 식품기업의 미국 진출을 지원하는 AI 서비스

![썸네일](./Risk_Killer.png)
[[프로젝트 발표자료]](./Risk_killer.pdf)


🔗 Live Demo: https://riskstremlaitapp.streamlit.app/


# Risk Killer — K-Food의 미국 진출을 돕는 FDA 규제·리콜 분석 AI (Streamlit)

[![Watch on YouTube](https://img.shields.io/badge/YouTube-FF0000?logo=youtube&logoColor=white)](https://youtu.be/VIDEO_ID)
[![Streamlit App](https://img.shields.io/badge/Streamlit-App-green)](https://YOUR-APP-URL)
[![PDF](https://img.shields.io/badge/Slides-PDF-blue)](./Risk_killer.pdf)

<p align="center">
  <a href="./Risk_killer.pdf">
    <img src="./Risk_Killer.png" width="900" alt="Risk Killer 발표 썸네일 (클릭하면 PDF)">
  </a>
</p>

## TL;DR
- 🇺🇸 **FDA 규제/리콜** 문서를 수집·임베딩해 **질의응답/검색** 제공
- 🧠 **LangChain/LangGraph + ChromaDB** 기반 RAG 파이프라인
- 🖥️ **Streamlit** UI로 누구나 바로 사용 가능
- 🔍 실전 시나리오: 성분/알레르겐/표시기준/리콜사유 빠른 확인

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
