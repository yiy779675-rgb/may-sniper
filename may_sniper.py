import streamlit as st
import requests
import yfinance as yf

# --- 页面基础设置 ---
st.set_page_config(page_title="May的全球狙击指挥部", page_icon="🔫", layout="wide")

st.title("🔫 May 的全球狙击指挥部")
st.caption("“日不落狙击手：从东京到孟买，从法兰克福到纽约。” —— 蓝蓝 V4.0")

# --- 顶部刷新按钮 ---
if st.button("🔄 点我刷新所有数据", type="primary"):
    st.rerun()

# --- 侧边栏：实时情报 ---
st.sidebar.header("🌍 实时期货情报")

def get_futures():
    # 新增日经期货(NIY=F)
    tickers = {
        '纳指期货': 'NQ=F', 
        '标普期货': 'ES=F', 
        '日经期货': 'NIY=F',
        '黄金期货': 'GC=F'
    }
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

# 侧边栏显示
futures = get_futures()
for name, info in futures.items():
    st.sidebar.metric(name, f"{info['price']:.0f}", f"{info['change']:.2f}%")
st.sidebar.info("提示：期货数据来自雅虎，可能有延迟。")


# --- 核心工具函数 ---
def get_sina_price(code):
    try:
        headers = {'Referer': 'http://finance.sina.com.cn'} 
        url = f"http://hq.sinajs.cn/list={code}"
        r = requests.get(url, headers=headers).text
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
    
    # 印度特别逻辑（印度经常高溢价，阈值放宽一点）
    if "印度" in name:
        if premium < 1.0: status, color = "🟢 极佳 (捡漏)", "success"
        elif premium < 3.0: status, color = "🟡 正常溢价", "warning"
        else: status, color = "🔴 太贵了 (小心)", "error"
    # A股逻辑
    elif "创业" in name or "中证" in name:
        if premium < 0: status, color = "🟢 折价", "success"
        else: status, color = "🟡 正常", "warning"
    # 黄金/发达市场逻辑
    else:
        if premium < 0.5: status, color = "🟢 极佳 (买入)", "success"
        elif premium < 1.0: status, color = "🟡 正常", "warning"
        elif premium < 3.0: status, color = "🟠 偏贵", "warning"
        else: status, color = "🔴 极度危险", "error"
        
    return premium, status, color

# --- 第一排：发达市场 F4 ---
st.header("🏙️ 发达市场 F4")
c1, c2, c3, c4 = st.columns(4)

with c1:
    st.subheader("🇺🇸 纳指 (513100)")
    p = get_sina_price("sh513100")
    st.metric("市价", f"¥ {p}")
    iopv = st.number_input("输入净值", value=p, format="%.4f", key="nq")
    prem, s, c = check_premium("纳指", p, iopv)
    st.metric("溢价率", f"{prem:.2f}%")
    if c == "success": st.success(s)
    elif c == "warning": st.warning(s)
    else: st.error(s)

with c2:
    st.subheader("🇺🇸 标普 (513500)")
    p = get_sina_price("sh513500")
    st.metric("市价", f"¥ {p}")
    iopv = st.number_input("输入净值", value=p, format="%.4f", key="sp")
    prem, s, c = check_premium("标普", p, iopv)
    st.metric("溢价率", f"{prem:.2f}%")
    if c == "success": st.success(s)
    else: st.warning(s)

with c3:
    st.subheader("🇩🇪 德国 (513030)")
    p = get_sina_price("sh513030")
    st.metric("市价", f"¥ {p}")
    iopv = st.number_input("输入净值", value=p, format="%.4f", key="dax")
    prem, s, c = check_premium("德国", p, iopv)
    st.metric("溢价率", f"{prem:.2f}%")
    if c == "success": st.success(s)
    elif c == "warning": st.warning(s)
    else: st.error(s)

with c4:
    # 新增：日经225
    st.subheader("🇯🇵 日经 (513520)")
    p = get_sina_price("sh513520")
    st.metric("市价", f"¥ {p}")
    iopv = st.number_input("输入净值", value=p, format="%.4f", key="nikkei")
    prem, s, c = check_premium("日经", p, iopv)
    st.metric("溢价率", f"{prem:.2f}%")
    if c == "success": st.success(s)
    elif c == "warning": st.warning(s)
    else: st.error(s)

st.divider()

# --- 第二排：新兴 & 资源 ---
st.header("🌶️ 新兴 & 资源")
c5, c6 = st.columns(2)

with c5:
    # 新增：印度LOF (最火的那个)
    st.subheader("🇮🇳 印度 (164824)")
    p = get_sina_price("sz164824")
    st.metric("市价", f"¥ {p}")
    iopv = st.number_input("输入净值", value=p, format="%.4f", key="india")
    prem, s, c = check_premium("印度", p, iopv)
    st.metric("溢价率", f"{prem:.2f}%")
    if c == "success": st.success(s)
    elif c == "warning": st.warning(s)
    else: st.error(s)

with c6:
    st.subheader("🏆 黄金 (518880)")
    p = get_sina_price("sh518880")
    st.metric("市价", f"¥ {p}")
    iopv = st.number_input("输入净值", value=p, format="%.4f", key="gold")
    prem, s, c = check_premium("黄金", p, iopv)
    st.metric("溢价率", f"{prem:.2f}%")
    if c == "success": st.success(s)
    else: st.warning(s)

st.divider()

# --- 第三排：A股内政 ---
st.header("🐼 A股内政")
c7, c8 = st.columns(2)

with c7:
    st.subheader("🚀 创业板 (159915)")
    p = get_sina_price("sz159915")
    st.metric("市价", f"¥ {p}")
    iopv = st.number_input("输入净值", value=p, format="%.4f", key="cyb")
    prem, s, c = check_premium("创业", p, iopv)
    st.metric("溢价率", f"{prem:.2f}%")
    
with c8:
    st.subheader("📊 中证500 (510500)")
    p = get_sina_price("sh510500") 
    st.metric("市价", f"¥ {p}")
    iopv = st.number_input("输入净值", value=p, format="%.4f", key="zz500")
    prem, s, c = check_premium("中证", p, iopv)
    st.metric("溢价率", f"{prem:.2f}%")
