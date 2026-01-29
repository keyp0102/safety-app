import streamlit as st
from streamlit_drawable_canvas import st_canvas
import datetime
 
# 設定網頁標題
st.set_page_config(page_title="安全衛生檢查表", layout="centered")
 
# 使用 CSS 讓按鈕在手機上更好按，並讓表格更緊湊
st.markdown("""
    <style>
    .stButton>button { width: 100%; font-weight: bold; height: 3em; border-radius: 10px; }
    .stSubheader { background-color: #f0f2f6; padding: 5px 10px; border-left: 5px solid #007aff; }
    </style>
    """, unsafe_allow_html=True)
 
st.title("🛡️ 安衛指導檢查紀錄表")
 
# 1. 基本資訊區
c1, c2 = st.columns(2)
with c1:
    check_date = st.date_input("檢查日期", datetime.date.today())
with c2:
    dept = st.text_input("受指導部門", placeholder="請輸入部門名稱")
 
# 2. 定義狀態切換
def toggle(key):
    status_list = [" ", "V", "X", "!"]
    if key not in st.session_state:
        st.session_state[key] = " "
    current_idx = status_list.index(st.session_state[key])
    st.session_state[key] = status_list[(current_idx + 1) % len(status_list)]
 
# 3. 完整的查核項目資料庫
all_items = {
    "A.組織管理 - A04/06/08": [
        ("A04-1", "控制室高架地板增設火警偵測"),
        ("A04-2", "手持設備充電應放於金屬箱內"),
        ("A04-3", "消防系統開關標示常關或常開"),
        ("A06-1", "變更案申請是否符合MOC程序書"),
        ("A08-1", "風險評估AB表填寫是否完整"),
        ("A08-2", "承攬商是否依據內容提出JSA")
    ],
    "B.責任轄區 - B01/03/04": [
        ("B01-1", "各單位年度計畫及執行紀錄"),
        ("B01-2", "表單內是否確實填寫實測紀錄"),
        ("B03-1", "管線標示流體名稱與方向"),
        ("B03-2", "手輪標示開關方向"),
        ("B04-1", "機房不可擺置非必要物品"),
        ("B04-2", "工作場所走道保持暢通"),
        ("B04-3", "鋼樓梯及護蓋漆黃漆警示")
    ]
}
 
# 4. 生成檢查表介面
for category, tasks in all_items.items():
    st.subheader(category)
    for code, task in tasks:
        col_btn, col_text = st.columns([1, 4])
        with col_btn:
            # 顯示當前狀態
            val = st.session_state.get(code, " ")
            st.button(val, key=f"btn_{code}", on_click=toggle, args=(code,))
        with col_text:
            st.write(f"**{code}** {task}")
        # 備註欄位放在下方增加手機操作空間
        st.text_input("說明/改善措施", key=f"note_{code}", placeholder="異常請註明...")
    st.divider()
 
# 5. 簽名區域
st.subheader("✍️ 相關人員簽名")
st.info("請於下方灰色區域手寫簽名")
canvas_result = st_canvas(
    stroke_width=3, stroke_color="#000", background_color="#eee",
    height=150, update_streamlit=True, key="sig_canvas"
)
 
if st.button("✅ 檢查完成 (點擊慶祝)"):
    st.balloons()
    st.success("檢查已完成！請利用 iPhone 截圖或使用分享功能儲存結果。")
