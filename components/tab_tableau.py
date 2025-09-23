# components/tableau.py

import streamlit as st
import pandas as pd
import streamlit.components.v1 as components
import uuid

def embed_tableau_auto(
    url: str,
    ratio: str = "16:9",      # W:H (가로:세로 비율)
    vh_portion: float = 0.85, # 화면 높이의 몇 %까지 사용할지 (0~1)
    min_height: int = 520,    # 너무 낮아지지 않게 하한
    max_height: int = 820,    # 과도하게 길어지지 않게 상한 (Streamlit 예약 높이도 이 값으로)
    toolbar: str = "yes",     # "yes" | "no" | "top" | "bottom"
):
    # 비율 계산 (H/W)
    w, h = map(float, ratio.split(":"))
    r = h / w

    sep = "&" if "?" in url else "?"
    final = f"{url}{sep}:showVizHome=no&:embed=y&:toolbar={toolbar}"
    box_id = f"tbl-{uuid.uuid4().hex}"

    html = f"""
    <div id="{box_id}" style="position:relative;width:100%;
         border:1px solid #e1e5e9;border-radius:8px;background:#fff;overflow:hidden;">
      <iframe id="{box_id}-iframe" src="{final}" style="width:100%;height:100%;border:0;" allowfullscreen></iframe>
    </div>
    <script>
      (function(){{
        const box = document.getElementById("{box_id}");
        const frame = document.getElementById("{box_id}-iframe");
        const RATIO = {r};                 // H/W
        const VH_PORTION = {vh_portion};   // 화면 높이 비율 (0~1)

        function resize() {{
          const w = box.clientWidth;                          // 현재 컬럼 실제 너비
          const hByWidth = Math.round(w * RATIO);             // 비율 기반 높이
          const hByViewport = Math.round(window.innerHeight * VH_PORTION); // 화면 높이 기반
          let target = Math.min(hByWidth, hByViewport);       // 둘 중 작은 값 사용
          target = Math.max({min_height}, Math.min({max_height}, target));  // 하한/상한
          box.style.height = target + "px";
          frame.style.height = target + "px";
        }}
        window.addEventListener("load", resize);
        window.addEventListener("resize", resize);
        setTimeout(resize, 200);  // 초기 렌더 지연 대응
      }})();
    </script>
    """
    # Streamlit이 예약하는 바깥 높이(너무 크면 빈 공간 생김) → max_height로 맞춰 최소화
    components.html(html, height=max_height, scrolling=False)

## tableau
def create_market_dashboard():
    """미국 시장 진출 대시보드 UI 생성"""
    # 설명 문구 추가
    st.info("""
    미국 식품 시장 동향을 시각화된 자료로 확인할 수 있습니다.\n
    모든 시각화 자료는 다운로드 기능을 제공합니다.""")
    
    # 2행: 두 개의 태블로 시각화 (미국 주별 식품 지출 시각화와 연도별 미국 식품 지출 추이)
    viz_col1, viz_col2= st.columns(2)
    
    with viz_col1:
        # 첫 번째 태블로 시각화: 미국 주별 식품 지출 시각화
        st.markdown("<h5 style='text-align: left;'># 미국 주별 식품 지출 시각화</h5>", unsafe_allow_html=True)
        
        embed_tableau_auto(
            url="https://public.tableau.com/views/state_food_exp2_17479635670940/State",
            ratio="4:3",          # 4:3 비율로 표시
            vh_portion=0.85,      # 화면 높이의 85%까지만 사용
            min_height=420,       # 최소 420픽셀
            max_height=600,       # 최대 600픽셀
            toolbar="bottom",     # 도구모음 하단 표시
        )
        st.caption("출처: [Statista Food](https://www.statista.com/outlook/cmo/food/united-states)")
    
    
    with viz_col2:
        st.markdown("<h5 style='text-align:left;'># 연도/리콜원인별 발생 건수 히트맵</h5>",
                    unsafe_allow_html=True)

        embed_tableau_auto(
            url="https://public.tableau.com/views/food_recall_year_01/1_1",
            ratio="4:3",          # 4:3 비율로 표시
            vh_portion=0.85,      # 화면 높이의 85%까지만 사용
            min_height=420,       # 최소 420픽셀
            max_height=600,       # 최대 600픽셀
            toolbar="yes",        # 도구모음 표시
        )
        st.caption("출처: [FDA Recall Database](https://www.fda.gov/safety/recalls-market-withdrawals-safety-alerts)")

    # 2행
    viz_col3, viz_col4= st.columns(2)

    with viz_col3:
        st.markdown("<h5 style='text-align:left;'># 연도/카테고리별 미국 식품 지출 추이</h5>",
                    unsafe_allow_html=True)

        embed_tableau_auto(
            url="https://public.tableau.com/views/main01/1_1",
            ratio="4:3",          # 4:3 비율로 표시
            vh_portion=0.85,      # 화면 높이의 85%까지만 사용
            min_height=540,       # 최소 540픽셀
            max_height=700,       # 최대 700픽셀
            toolbar="yes",        # 도구모음 표시
        )
        st.caption("출처: [USDA](https://www.ers.usda.gov/data-products/us-food-imports)")
    
    
    with viz_col4:
        st.markdown("<h5 style='text-align: left;'># 리콜 등급(Class)별 발생 건수</h5>", unsafe_allow_html=True)

        embed_tableau_auto(
            url="https://public.tableau.com/views/food_recall_class_01/1_1",
            ratio="4:3",          # 4:3 비율로 표시
            vh_portion=0.85,      # 화면 높이의 85%까지만 사용
            min_height=540,       # 최소 540픽셀
            max_height=700,       # 최대 700픽셀
            toolbar="yes",        # 도구모음 표시
        )
        st.caption("출처: [FDA Recall Database](https://www.fda.gov/safety/recalls-market-withdrawals-safety-alerts)")
