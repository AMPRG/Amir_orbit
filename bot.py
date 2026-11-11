def call_ai_api(prompt_text):
    headers = {
        "Authorization": f"Bearer {DAHL_API_KEY}",
        "Content-Type": "application/json"
    }
    payload = {
        "model": "MiniMaxAI/MiniMax-M2.7",
        "messages": [
            {
                "role": "system",
                "content": "تو یک دستیار آموزشی و درسی هوشمند هستی. به سوالات درسی به زبان فارسی و به صورت دقیق و مفهومی پاسخ بده."
            },
            {
                "role": "user",
                "content": prompt_text
            }
        ]
    }
    try:
        response = requests.post(DAHL_URL, json=payload, headers=headers)
        
        # چاپ وضعیت و متن خام پاسخ برای عیب‌یابی در لاگ‌های رایلوِی
        print(f"Status Code: {response.status_code}")
        print(f"Response Text: {response.text}")
        
        res_data = response.json()
        
        if response.status_code != 200:
            return f"خطای سرور ({response.status_code}): {res_data}"
            
        return res_data["choices"][0]["message"]["content"]
    except Exception as e:
        print(f"API Error: {e}")
        return f"خطای فنی: {e}"
