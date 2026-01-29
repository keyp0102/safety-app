import streamlit as st
from streamlit_drawable_canvas import st_canvas
import datetime
 
# 設定網頁標題與排版
st.set_page_config(page_title="安全衛生檢查表", layout="centered")
 
st.title("🛡️ 安全衛生指導檢查紀錄表")
 
# 1. 檢查日期 (自動抓取台灣時間)
today = datetime.date.today()
check_date = st.date_input("檢查日期", today)
 
# 2. 定義循環勾選邏輯
def toggle_status(key):
    # 在 session_state 中儲存每個項目的狀態
    if key not in st.session_state:
        st.session_state[key] = ""
   
    status_list = ["", "V", "X", "!"]
    current_idx = status_list.index(st.session_state[key])
    next_idx = (current_idx + 1) % len(status_list)
    st.session_state[key] = status_list[next_idx]
 
# 3. 查核大項資料
items = {
    "A04.缺失改善": ["控制室高架地板增設火警偵測", "手持設備充電應放於金屬箱內", "消防系統開關標示常關或常開", "消防軟管轉軸保養"],
    "A06.文件管理": ["變更案申請是否符合MOC程序書", "是否如期推動否則應提出展延", "抽查最新一件完成的MOC辦理情形"],
    "A08.風險管理": ["風險評估AB表填寫是否完整", "承攬商是否依據實際工作內容提出JSA", "承攬商工作屬A級或B級作業是否提出SOP"],
    "B03.管線標示": ["管線直段每100m標示及流向", "排放或取樣開關標示及管填塞", "手輪標示開關方向"],
    "B04.5S安全": ["控制室/電氣室不可擺置非必要物品", "工作場所走道或通道應暢通", "鋼樓梯及護蓋漆黃漆警示"]
}
 
# 4. 渲染表格
for category, sub_items in items.items():
    st.subheader(f"📍 {category}")
    for idx, sub_item in enumerate(sub_items):
        col1, col2, col3 = st.columns([1, 4, 3])
        key = f"{category}_{idx}"
       
        # 顯示目前的狀態顏色
        current_val = st.session_state.get(key, "")
        btn_label = f"狀態: {current_val}" if current_val else "點擊勾選"
       
        with col1:
            st.button(btn_label, key=f"btn_{key}", on_click=toggle_status, args=(key,))
        with col2:
           st.write(sub_item)
        with col3:
            st.text_input("備註", key=f"note_{key}", placeholder="鍵入結果...")
    st.divider()
 
# 5. 手寫簽名區 (iPhone 友善)
st.subheader("✍️ 指導人與部門經理簽名")
canvas_result = st_canvas(
    fill_color="rgba(255, 165, 0, 0.3)", 
    stroke_width=3,
    stroke_color="#000000",
    background_color="#eeeeee",
    height=150,
    key="canvas",
    display_toolbar=True,
    update_streamlit=True,
)
 
if st.button("✅ 完成檢查並生成報告"):
    st.success("報告已產出！(此處可連結 PDF 生成功能)")
    st.balloons()
