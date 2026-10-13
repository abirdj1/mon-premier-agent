import os
import json
import subprocess
from datetime import datetime
from dotenv import load_dotenv

# Charger la clé API depuis le fichier .env
load_dotenv()
API_KEY = os.getenv("OPENROUTER_API_KEY")
API_URL = "https://openrouter.ai/api/v1/chat/completions"

print(f"🔍 DEBUG : Ta clé commence par '{API_KEY[:8]}' (Doit être 'sk-or-v1')\n")

# ========== LES OUTILS (TOOLS) ==========

def calculer(expression: str) -> str:
    try:
        resultat = eval(expression)
        return f"Le résultat de {expression} est {resultat}"
    except Exception as e:
        return f"Erreur : je ne peux pas calculer cette expression ({e})"

def heure_actuelle() -> str:
    maintenant = datetime.now()
    return f"Il est actuellement {maintenant.strftime('%H:%M:%S')}, le {maintenant.strftime('%A %d %B %Y')}"

tools = [
    {
        "type": "function",
        "function": {
            "name": "calculer",
            "description": "Utile pour faire des calculs mathématiques",
            "parameters": {
                "type": "object",
                "properties": {
                    "expression": {
                        "type": "string",
                        "description": "L'expression mathématique à calculer, exemple: '25 * 4 + 10'"
                    }
                },
                "required": ["expression"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "heure_actuelle",
            "description": "Utile pour savoir l'heure et la date actuelles",
            "parameters": {
                "type": "object",
                "properties": {}
            }
        }
    }
]

# ========== FONCTION POUR APPELER OPENROUTER VIA CURL.EXE ==========

def appeler_ia(messages):
    data = {
        "model": "openrouter/free",  # Modèle infaillible et 100% gratuit
        "messages": messages,
        "tools": tools,
        "tool_choice": "auto"
    }
    
    with open("temp_request.json", "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False)
    
    curl_command = [
        "curl.exe", "-s", "-k", "-X", "POST", API_URL,
        "-H", f"Authorization: Bearer {API_KEY}",
        "-H", "Content-Type: application/json",
        "-H", "HTTP-Referer: http://localhost",
        "-H", "X-Title: Mon Agent IA",
        "-d", "@temp_request.json"
    ]
    
    try:
        result = subprocess.run(curl_command, capture_output=True, text=True, encoding="utf-8", timeout=90)
        if result.returncode != 0:
            raise Exception(f"curl a échoué: {result.stderr}")
        
        response = json.loads(result.stdout)
        if "error" in response:
            raise Exception(f"Erreur API : {response['error']}")
        return response
    except subprocess.TimeoutExpired:
        raise Exception("La requête a expiré (30s).")
    except Exception as e:
        raise Exception(f"Erreur : {e}")
    finally:
        if os.path.exists("temp_request.json"):
            os.remove("temp_request.json")

# ========== FONCTION PRINCIPALE DE L'AGENT ==========

def run_agent(question_utilisateur: str):
    messages = [
        {"role": "system", "content": "Tu es un assistant intelligent. Utilise des outils si nécessaire. Réponds toujours en français de manière naturelle."},
        {"role": "user", "content": question_utilisateur}
    ]

    response = appeler_ia(messages)
    response_message = response["choices"][0]["message"]
    tool_calls = response_message.get("tool_calls")

    if tool_calls:
        messages.append(response_message)

        for tool_call in tool_calls:
            function_name = tool_call["function"]["name"]
            function_args = json.loads(tool_call["function"]["arguments"])

            print(f"→ L'agent utilise l'outil : {function_name}")

            if function_name == "calculer":
                result = calculer(function_args.get("expression"))
            elif function_name == "heure_actuelle":
                result = heure_actuelle()
            else:
                result = "Outil inconnu"

            messages.append({
                "role": "tool",
                "tool_call_id": tool_call["id"],
                "name": function_name,
                "content": str(result)
            })

        final_response = appeler_ia(messages)
        final_message = final_response["choices"][0]["message"]
        
        # 🛡️ SÉCURITÉ : Si le modèle gratuit renvoie None, on affiche le résultat de l'outil
        reponse_texte = final_message.get("content")
        if not reponse_texte:
            resultats_outils = [msg["content"] for msg in messages if msg["role"] == "tool"]
            return "📊 Résultat : " + " | ".join(resultats_outils)
            
        return reponse_texte
    else:
        return response_message.get("content", "Je n'ai pas de réponse.")

# ========== TESTER L'AGENT ==========

if __name__ == "__main__":
    print("=== Mon Premier Agent IA (OpenRouter 100% Gratuit & Blindé) ===")
    print("Tape 'quit' pour quitter\n")

    while True:
        question = input("Toi : ")
        if question.lower() in ["quit", "exit", "q"]:
            print("Au revoir !")
            break

        reponse = run_agent(question)
        print(f"\nAgent : {reponse}\n")