import os
import json
from dotenv import load_dotenv
from openai import OpenAI

# === EKSİK OLAN VE ŞİMDİ EKLENEN SATIR BURADA ===
from .prompt_config import SYSTEM_PROMPT, SUMMARIZER_PROMPT
# =================================================

# .env dosyasındaki değişkenleri yüklemek için
load_dotenv()

# OpenAI İstemcisini Başlatma
client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY"),
    base_url="https://api.deepseek.com"
)

def call_ai_model(memory_json, chat_history, new_message):
    """
    Kullanıcı verileriyle birlikte DeepSeek modelini çağırır ve yapılandırılmış bir JSON cevabı bekler.
    """
    messages = [
        {
            "role": "system",
            "content": f"{SYSTEM_PROMPT}\\n\\n<hafiza>{json.dumps(memory_json, ensure_ascii=False)}</hafiza>"
        }
    ]
    for entry in chat_history:
        try:
            role_str, content_str = entry.split(":", 1)
            role = "user" if role_str.lower() == "kullanıcı" else "assistant"
            messages.append({"role": role, "content": content_str.strip()})
        except ValueError:
            continue
            
    messages.append({"role": "user", "content": new_message})

    try:
        response = client.chat.completions.create(
            model="deepseek-chat",
            messages=messages,
            stream=False,
            temperature=0.7,
            max_tokens=2048
        )
        
        ai_response_string = response.choices[0].message.content

        print("--- AI'DAN GELEN HAM CEVAP ---")
        print(ai_response_string)
        print("-----------------------------")
        
        return json.loads(ai_response_string)

    except json.JSONDecodeError:
        print(f"HATA: AI geçerli bir JSON formatında cevap vermedi. Gelen cevap: {ai_response_string}")
        return {"reply_text": ai_response_string, "suggested_action": None}
    except Exception as e:
        print(f"API çağrısı sırasında beklenmedik bir hata oluştu: {e}")
        return {"reply_text": "Sistemde beklenmedik bir sorun oluştu.", "suggested_action": None}


def get_updated_memory_json(current_memory_json, session_transcript):
    """
    Sohbet metnini ve mevcut hafızayı kullanarak AI'a özetletir ve güncellenmiş yeni JSON'ı döndürür.
    """
    messages = [
        {"role": "system", "content": f"{SUMMARIZER_PROMPT}\\n\\n[MEVCUT JSON]\\n<hafiza>{json.dumps(current_memory_json, ensure_ascii=False)}</hafiza>"},
        {"role": "user", "content": f"[SON KONUŞMA METNİ]\\n<konusma>{session_transcript}</konusma>\\n\\n[ÇIKTI]"}
    ]

    try:
        response = client.chat.completions.create(
            model="deepseek-chat",
            messages=messages,
            stream=False
        )
        response_content_string = response.choices[0].message.content
        return json.loads(response_content_string)
    except Exception as e:
        print(f"Özetleyici sırasında hata: {e}")
        return current_memory_json