import streamlit as st
import requests

st.set_page_config(page_title="プロパンガス切替NG判定", layout="centered")

st.title("🔥 プロパンガス切替NG判定システム")
st.write("エリア・ガス会社・ボンベ会社を入力して、切替可能かをAIが判定します。")

# 入力フォーム
area = st.text_input("【エリア】例：愛知県弥富市")
company = st.text_input("【ガス会社】例：名古屋プロパン")
bottle = st.text_input("【ボンベ会社】不明でもOK", value="不明")

# ボタン押下で判定
if st.button("🔍 判定する"):
    if not area or not company:
        st.warning("エリアとガス会社は必須ですモー🐮")
    else:
        prompt = f"""以下の情報から、切替NGかどうか判定してください。

【エリア】{area}
【現在のガス会社】{company}
【ボンベ会社】{bottle}

出力形式：
---
ガス会社名
◯◯◯◯

切替可能提携拠点名
◯◯◯◯
---"""

        # Fireworks API呼び出し
        FIREWORKS_API_KEY = st.secrets["FIREWORKS_API_KEY"]
        url = "https://api.fireworks.ai/inference/v1/chat/completions"

        headers = {
            "Authorization": f"Bearer {FIREWORKS_API_KEY}",
            "Content-Type": "application/json"
        }

        data = {
            "model": "accounts/fireworks/models/claude-3-sonnet:20240229",
            "messages": [
                {"role": "system", "content": "あなたはプロパンガスの切替NG判定を行う専門AIです。"},
                {"role": "user", "content": prompt}
            ],
            "temperature": 0.3,
            "max_tokens": 1024
        }

        with st.spinner("判定中モー🐮..."):
            response = requests.post(url, headers=headers, json=data)

        if response.ok:
            result = response.json()["choices"][0]["message"]["content"]
            st.success("✅ 判定結果")
            st.text(result)
        else:
            st.error("❌ Fireworks APIエラー")
            st.code(response.text)
