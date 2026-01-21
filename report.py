import os
import datetime
import requests
import FinanceDataReader as fdr

DISCORD_WEBHOOK_URL = os.environ.get("DISCORD_WEBHOOK_URL")

TICKERS = ["TQQQ", "QQQ"]

def send_message(msg):
    now = datetime.datetime.now()
    payload = {
        "content": f"[{now.strftime('%Y-%m-%d %H:%M:%S')}] {msg}"
    }
    requests.post(DISCORD_WEBHOOK_URL, json=payload, timeout=10)

def analyze_ticker(ticker):
    df = fdr.DataReader(ticker)

    if len(df) < 200:
        return f"{ticker} ❌ 데이터 부족"

    df_200 = df.tail(200)

    max_close = df_200['Close'].max()
    last_close = df_200['Close'].iloc[-1]
    prev_close = df_200['Close'].iloc[-2]

    drop_rate = (last_close - max_close) / max_close * 100

    return (
        f"{ticker}(최고가: {max_close:.2f}$, "
        f"전일종가: {prev_close:.2f}$, "
        f"최고가대비 하락: {drop_rate:.2f}%)"
    )

def main():
    send_message("📊 200거래일 기준 하락률 리포트")

    for ticker in TICKERS:
        try:
            result = analyze_ticker(ticker)
            send_message(result)
        except Exception as e:
            send_message(f"{ticker} ❌ 오류: {e}")

if __name__ == "__main__":
    main()
