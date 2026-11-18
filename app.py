import streamlit as st

from core.config import DEFAULT_STYLE, GENRES, TONES, load_settings
from core.export import to_markdown, to_srt
from core.generator import GenerationError, Generator
from core.schema import Request, Script

st.set_page_config(page_title="숏폼 스크립트 생성기", page_icon="🎬", layout="wide")
st.title("🎬 숏폼 애니메이션 & 웹툰 스크립트 생성기")

settings = load_settings()
if not settings.api_key:
    st.error(
        "GEMINI_API_KEY가 없습니다. Streamlit Cloud는 Secrets에, "
        "Codespaces는 .streamlit/secrets.toml에 추가해주세요."
    )
    st.stop()


@st.cache_resource
def get_generator(api_key: str, model: str) -> Generator:
    return Generator(api_key, model)


def render_script(s: Script) -> None:
    st.subheader(s.title)
    st.info(f"🎣 훅: {s.hook}")
    with st.expander("캐릭터 설정 (이미지 일관성용)"):
        for c in s.characters:
            st.write(f"- {c}")
    for sc in s.scenes:
        with st.container(border=True):
            st.markdown(f"**장면 {sc.number}** · {sc.seconds}초 — {sc.summary}")
            for ln in sc.lines:
                sfx = f"  _({ln.sfx})_" if ln.sfx else ""
                st.markdown(f"**{ln.speaker}:** {ln.text}{sfx}")
            st.caption("이미지 프롬프트")
            st.code(sc.image_prompt, language=None)
    st.markdown(f"**CTA:** {s.cta}")
    st.write(" ".join(s.hashtags))


with st.sidebar:
    st.header("설정")
    total = st.slider("총 길이 (초)", 15, 90, 60, step=5)
    n_scenes = st.slider("장면 수", 3, 12, 6)
    tone = st.selectbox("톤", TONES)
    style = st.text_input("이미지 스타일", DEFAULT_STYLE)
    st.caption(f"모델: {settings.model}")

genre = st.selectbox("장르 선택", GENRES)
topic = st.text_input("오늘의 에피소드 주제 (예: 지하철에서 아는 사람 만났을 때)")

if st.button("대본 및 이미지 프롬프트 생성", type="primary"):
    if not topic.strip():
        st.warning("주제를 입력해주세요.")
    else:
        req = Request(
            genre=genre, tone=tone, topic=topic.strip(),
            total_seconds=total, n_scenes=n_scenes, style=style,
        )
        with st.spinner("Gemini가 대본을 쓰는 중..."):
            try:
                st.session_state["script"] = get_generator(
                    settings.api_key, settings.model
                ).generate(req)
            except GenerationError as e:
                st.error(f"생성 실패: {e}")

script: Script | None = st.session_state.get("script")
if script:
    st.success("생성 완료!")
    render_script(script)
    c1, c2, c3 = st.columns(3)
    c1.download_button("Markdown", to_markdown(script), file_name="script.md")
    c2.download_button("JSON", script.model_dump_json(indent=2), file_name="script.json")
    c3.download_button("자막 SRT", to_srt(script), file_name="script.srt")
