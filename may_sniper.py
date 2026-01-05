import streamlit as st
import requests
import yfinance as yf

# --- 页面基础设置 ---
st.set_page_config(page_title="May的全球狙击指挥部", page_icon="🔫", layout="wide")

st.title("🔫 May 的全球狙击指挥部")
st.caption("“点击下方按钮，获取最新战场快照。” —— 蓝蓝 V3.0")

# --- 顶部刷新按钮 (解决你的痛点) ---
if st.button("🔄 点我刷新所有数据", type="primary"):
    st.rerun()

# --- 侧边栏：实时情报 ---
st.sidebar.header("🌍 实时期货情报 (侦察兵)")

def get_futures():
    tickers = {'纳指期货': 'NQ=F', '标普期货': 'ES=F', '黄金期货': 'GC=F'}
    data = {}
    for name, code in tickers.items():
        try:
            ticker = yf.Ticker(code)
            info = ticker.history(period='1d')
            if not info.empty:
                current = info['Close'].iloc[-1]
                open_p = info['Open'].iloc[-1]
                change = (current - open_p) / open_p * 100
                data[name] = {"price": current, "change": change}
            else:
                data[name] = {"price": 0, "change": 0}
        except:
            data[name] = {"price": 0, "change": 0}
    return data

# 侧边栏逻辑
futures = get_futures()
for name, info in futures.items():
    # 颜色逻辑：涨红跌绿
    delta_color = "normal" 
    st.sidebar.metric(name, f"{info['price']:.2f}", f"{info['change']:.2f}%")
st.sidebar.info("提示：期货数据来自雅虎，可能有延迟。")


# --- 核心工具函数 ---
def get_sina_price(code):
    try:
        headers = {'Referer': 'http://finance.sina.com.cn'} 
        url = f"http://hq.sinajs.cn/list={code}"
        r = requests.get(url, headers=headers).text
        # 数据格式: var hq_str_sh513100="名字,开盘,昨收,现价..."
        price = float(r.split(',')[3])
        return price
    except:
        return 0.0

def check_premium(name, market_price, iopv):
    if iopv == 0 or market_price == 0: 
        return 0.0, "等待数据...", "gray"
    
    premium = (market_price - iopv) / iopv * 100
    status = ""
    color = ""
    
    # A股逻辑
    if "创业" in name or "中证" in name:
        if premium < 0: status, color = "🟢 折价 (划算)", "success"
        elif premium < 0.2: status, color = "🟡 正常", "warning"
        else: status, color = "🔴 溢价 (略贵)", "error"
    # 黄金逻辑
    elif "黄金" in name:
        if premium <= 0: status, color = "🟢 极佳 (折价)", "success"
        elif premium < 0.2: status, color = "🟡 正常", "warning"
        else: status, color = "🔴 太贵", "error"
    # 跨境ETF逻辑
    else:
        if premium < 0.5: status, color = "🟢 极佳 (买入)", "success"
        elif premium < 1.0: status, color = "🟡 正常 (可买)", "warning"
        elif premium < 3.0: status, color = "🟠 偏贵 (慎重)", "warning"
        else: status, color = "🔴 极度危险 (停手)", "error"
        
    return premium, status, color

# --- 第一排：全球战场 (跨境ETF) ---
st.header("✈️ 全球战场 (4大金刚)")
col1, col2, col3, col4 = st.columns(4)

# 1. 纳指
with col1:
    st.subheader("🇺🇸 纳指 (513100)")
    p1 = get_sina_price("sh513100")
    st.metric("当前市价", f"¥ {p1}")
    iopv1 = st.number_input("输入净值(IOPV)", value=p1, step=0.001, format="%.4f", key="nasdaq")
    prem1, s1, c1 = check_premium("纳指", p1, iopv1)
    st.metric("溢价率", f"{prem1:.2f}%")
    if c1 == "success": st.success(s1)
    elif c1 == "warning": st.warning(s1)
    else: st.error(s1)

# 2. 标普500 (新增!)
with col2:
    st.subheader("🇺🇸 标普 (513500)")
    p_sp = get_sina_price("sh513500")
    st.metric("当前市价", f"¥ {p_sp}")
    iopv_sp = st.number_input("输入净值(IOPV)", value=p_sp, step=0.001, format="%.4f", key="sp500")
    prem_sp, s_sp, c_sp = check_premium("标普", p_sp, iopv_sp)
    st.metric("溢价率", f"{prem_sp:.2f}%")
    if c_sp == "success": st.success(s_sp)
    elif c_sp == "warning": st.warning(s_sp)
    else: st.error(s_sp)

# 3. 德国
with col3:
    st.subheader("🇩🇪 德国 (513030)")
    p2 = get_sina_price("sh513030")
    st.metric("当前市价", f"¥ {p2}")
    iopv2 = st.number_input("输入净值(IOPV)", value=p2, step=0.001, format="%.4f", key="dax")
    prem2, s2, c2 = check_premium("德国", p2, iopv2)
    st.metric("溢价率", f"{prem2:.2f}%")
    if c2 == "success": st.success(s2)
    elif c2 == "warning": st.warning(s2)
    else: st.error(s2)

# 4. 黄金
with col4:
    st.subheader("🏆 黄金 (518880)")
    p3 = get_sina_price("sh518880")
    st.metric("当前市价", f"¥ {p3}")
    iopv3 = st.number_input("输入净值(IOPV)", value=p3, step=0.001, format="%.4f", key="gold")
    prem3, s3, c3 = check_premium("黄金", p3, iopv3)
    st.metric("溢价率", f"{prem3:.2f}%")
    if c3 == "success": st.success(s3)
    elif c3 == "warning": st.warning(s3)
    else: st.error(s3)

st.divider()

# --- 第二排：A股战场 (内政) ---
st.header("🐼 A股战场 (内政)")
col5, col6 = st.columns(2)

# 5. 创业板
with col5:
    st.subheader("🚀 创业板 (159915)")
    p4 = get_sina_price("sz159915")
    st.metric("当前市价", f"¥ {p4}")
    iopv4 = st.number_input("输入净值(IOPV)", value=p4, step=0.001, format="%.4f", key="cyb")
    prem4, s4, c4 = check_premium("创业板", p4, iopv4)
    st.metric("溢价率", f"{prem4:.2f}%")
    if c4 == "success": st.success(s4)
    elif c4 == "warning": st.warning(s4)
    else: st.error(s4)

# 6. 中证500
with col6:
    st.subheader("📊 中证500 (510500)")
    p5 = get_sina_price("sh510500") 
    st.metric("当前市价", f"¥ {p5}")
    iopv5 = st.number_input("输入净值(IOPV)", value=p5, step=0.001, format="%.4f", key="zz500")
    prem5, s5, c5 = check_premium("中证500", p5, iopv5)
    st.metric("溢价率", f"{prem5:.2f}%")
    if c5 == "success": st.success(s5)
    elif c5 == "warning": st.warning(s5)
    else: st.error(s5)
