# components/tab_recall.py
import streamlit as st
import time
from functools import lru_cache
from datetime import datetime

from utils.agent_recall import RecallAgent
from utils.chat_common_functions import (
    save_chat_history, get_session_keys, initialize_session_state,
    handle_project_change, display_chat_history,
    update_chat_history, handle_example_question, handle_user_input,
    reset_processing_state, quick_stream_response
)

# ── 무거운 객체는 캐싱해서 rerun 속도 개선 ─────────────────────────────────────
@st.cache_resource
def get_agent():
    return RecallAgent(add_hint=True)

agent = get_agent()

# 리콜 관련 예시 질문
@lru_cache(maxsize=1)
def get_recall_questions():
    return [
        "소스를 포함한 복합식품에서 리콜된 사례는 어떤 게 있나요?",
        "살모넬라균으로 리콜된 제품 목록을 보여줘.",
        "리콜이 가장 빈번하게 발생하는 식품 3개를 알려줘",
        "작년 대비 올해 리콜 트렌드에 변화가 있나요?"
    ]

def init_recall_session_state(session_keys):
    """리콜 특화 세션 상태 초기화"""
    initialize_session_state(session_keys)
    if "recall_processing_start_time" not in st.session_state:
        st.session_state.recall_processing_start_time = None

def render_sidebar_controls(project_name, chat_mode, session_keys):
    """사이드바 컨트롤 패널 렌더링"""
    project_changed = handle_project_change(project_name, chat_mode, session_keys)
    if project_changed:
        st.rerun()
    elif project_name:
        st.success(f"✅ '{project_name}' 진행 중")

    has_project_name = bool(project_name and project_name.strip())
    has_chat_history = bool(st.session_state.get(session_keys["chat_history"], []))
    is_processing = st.session_state.get(session_keys["is_processing"], False)

    # 저장 버튼
    save_disabled = not (has_project_name and has_chat_history) or is_processing
    if st.button("💾 대화 저장", disabled=save_disabled, use_container_width=True):
        if has_project_name and has_chat_history:
            with st.spinner("저장 중..."):
                success = save_chat_history(
                    project_name.strip(),
                    st.session_state.get(session_keys["chat_history"], []),
                    st.session_state.get(session_keys["langchain_history"], []),
                    chat_mode
                )
                if success:
                    st.success("✅ 저장 완료!")
                else:
                    st.error("❌ 저장 실패")

    return has_project_name, has_chat_history, is_processing

def clear_recall_conversation(session_keys):
    """리콜 탭 대화 초기화: 히스토리/메시지/챗 계열 리스트만 비우고 상태만 리셋"""
    # dict 크기 변경 오류 방지를 위해 keys()를 복사해서 순회
    for key in list(st.session_state.keys()):
        key_lower = key.lower()
        if any(k in key_lower for k in ['history', 'messages', 'chat']):
            if isinstance(st.session_state[key], list):
                st.session_state[key] = []

    # 선택 질문/처리 상태 초기화(루프에서 못비우는 단일 키들)
    if session_keys.get("selected_question"):
        st.session_state[session_keys["selected_question"]] = None
    if session_keys.get("is_processing"):
        st.session_state[session_keys["is_processing"]] = False
    st.session_state.recall_processing_start_time = None

def render_example_questions(session_keys, is_processing):
    """예시 질문 섹션 렌더링"""
    with st.expander("💡 예시 질문", expanded=True):
        recall_questions = get_recall_questions()
        cols = st.columns(2)
        for i, question in enumerate(recall_questions[:4]):
            with cols[i % 2]:
                if st.button(
                    question,
                    key=f"recall_example_{i}",
                    use_container_width=True,
                    disabled=is_processing
                ):
                    handle_example_question(question, session_keys)
                    st.rerun()

def render_chat_area(session_keys, is_processing):
    """메인 채팅 영역 렌더링 - 빠른 모드 전용"""

    # 예시 질문 & 기존 대화 표시
    render_example_questions(session_keys, is_processing)
    display_chat_history(session_keys)

    # 질문 처리 - 항상 빠른 모드로 스트리밍
    selected_key = session_keys["selected_question"]
    current_selected = st.session_state.get(selected_key)

    if current_selected:
        if not st.session_state.recall_processing_start_time:
            st.session_state.recall_processing_start_time = datetime.now()

        with st.chat_message("assistant"):
            response_placeholder = st.empty()
            with st.spinner("🔍 실시간 데이터 수집 및 분석 중..."):
                try:
                    response_placeholder.markdown("💭 리콜 데이터를 분석하고 있습니다...")
                    # Agent 실행
                    result = agent.run(
                        query=current_selected,
                        history=st.session_state.get(session_keys["langchain_history"], [])
                    )

                    # answer 추출 및 스트리밍
                    answer = result.get("answer", "답변을 생성할 수 없습니다.")
                    if answer:
                        quick_stream_response(
                            answer,
                            response_placeholder,
                            chunk_size=20,
                            delay=0.5
                        )
                    else:
                        response_placeholder.markdown("죄송합니다. 답변을 생성할 수 없습니다.")

                    # 처리 타입 표시
                    processing_type = result.get("processing_type", "unknown")
                    if processing_type == "agent":
                        st.info("🧠 Agent 컨트롤러로 처리됨")
                    elif processing_type == "function_calling":
                        st.info("⚡ Function Calling으로 처리됨")
                        function_calls = result.get('function_calls', [])
                        if function_calls:
                            with st.expander("🔧 실행된 함수들 보기"):
                                for i, call in enumerate(function_calls, 1):
                                    func_name = call.get('function', '알 수 없음')
                                    args = call.get('args', {})
                                    st.code(f"{i}. {func_name}({args})")
                    elif processing_type == "direct_answer":
                        st.info("💬 직접 답변")
                    else:
                        st.info("📄 처리 완료")

                    # 처리 시간 표시
                    if st.session_state.recall_processing_start_time:
                        processing_time = (datetime.now() - st.session_state.recall_processing_start_time).total_seconds()
                        st.caption(f"⏱️ 처리 시간: {processing_time:.1f}초")

                    # 히스토리 업데이트
                    update_chat_history(
                        current_selected,
                        answer,
                        session_keys,
                        result.get("chat_history", [])
                    )

                    # 다음 rerun에서 다시 돌지 않도록 선택 질문 해제
                    st.session_state[selected_key] = None

                    # 상태 초기화
                    reset_processing_state(session_keys)
                    st.session_state.recall_processing_start_time = None

                    time.sleep(0.3)
                    st.info("🔍 리콜 AI 답변 완료")

                except Exception as e:
                    response_placeholder.markdown(f"❌ 답변 생성 중 오류: {str(e)[:100]}...")
                    reset_processing_state(session_keys)
                    st.session_state.recall_processing_start_time = None
                    st.session_state[selected_key] = None

                st.rerun()

def show_recall_chat():
    """리콜 전용 챗봇 - 빠른 모드 전용 버전"""
    st.info("""
    🔎 **자동 실시간 리콜 분석 시스템** 
    - 질문 시, 최신 리콜 데이터를 실시간으로 자동 수집
    - 기존 DB와 통합하여 리콜 이슈를 분석 제공
    - 저장한 대화는 '기획안 요약 도우미' 탭에서 자동 요약 가능
    """)

    chat_mode = "리콜사례"
    session_keys = get_session_keys(chat_mode)

    # 세션 상태 초기화
    init_recall_session_state(session_keys)

    # 레이아웃
    col_left, col_center = st.columns([1, 4])

    with col_left:
        project_name = st.text_input("프로젝트 이름", placeholder="리콜 프로젝트명", key="recall_project_input")

        has_project_name, has_chat_history, is_processing = render_sidebar_controls(
            project_name, chat_mode, session_keys
        )

        # 규제 탭과 동일한 초기화 정책: 히스토리/메시지/챗 리스트만 비우고 상태 리셋
        if st.button("🗑️ 대화 초기화", type="secondary", use_container_width=True):
            clear_recall_conversation(session_keys)
            st.success("✅ 화면 초기화 완료!")
            st.rerun()

    with col_center:
        # 메인 채팅 영역
        render_chat_area(session_keys, is_processing)

        # 사용자 입력
        if not is_processing:
            user_input = st.chat_input("리콜 관련 질문을 입력하세요...", key="recall_chat_input")
            if user_input and user_input.strip():
                if len(user_input.strip()) < 3:
                    st.warning("⚠️ 질문이 너무 짧습니다.")
                else:
                    handle_user_input(user_input.strip(), session_keys)
                    st.rerun()
        else:

            st.info("🔄 실시간 데이터 수집 및 분석 중입니다...")
