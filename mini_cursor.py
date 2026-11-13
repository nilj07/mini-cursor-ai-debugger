import os 
import sys 
import subprocess

from groq import Groq


# adding colors in terminal 

RED = "\033[91m"
GREEN = "\033[92m"
YELLOW = "\033[93m"
CYAN = "\033[96m"
RESET = "\033[0m"

# building AI main Brain

SYSTEM_PROMPT = """You are a friendly senior developer helping a beginner student.
You will receive Python code and the error it produced.
Reply in EXACTLY this format, in simple English, with no markdown and no backticks:
WHY: (1-2 simple sentences, why this error happened)
FIX: (the corrected line or code)
TIP: (one short tip to avoid this mistake next time)"""

# now we define our AI Model 

MODEL = "openai/gpt-oss-120b"
    
client = Groq(api_key="ADD_YOUR_API")

# writing a if block that check file name is exist or not 

if len(sys.argv) < 2:
    print(YELLOW + "Use this:  python mini_cursor.py <file_name.py>" + RESET)
    sys.exit()


filename = sys.argv[1]


# IMP step where we run our code file 

result = subprocess.run([sys.executable, filename], capture_output=True, text=True)


# now we are checking that actually code file have error or not cause it waste API calls if no error

if result.returncode == 0:
    print(GREEN + "No error! Code working properly." + RESET)
    print(result.stdout)
    sys.exit()

# now we are sending the error to AI model for fixing it

with open(filename, encoding="utf-8") as f:
    code = f.read()

error = result.stderr[-2000:]

print(RED + "Error found:\n" + RESET + error)

user_message = f"CODE:\n{code}\n\nERROR:\n{error}"


response = client.chat.completions.create(
    model=MODEL,
    messages=[
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": user_message},
    ],
    temperature=0.2, 
)

answer = response.choices[0].message.content


color = CYAN

for line in answer.splitlines():
    if line.startswith("WHY"):
        color = YELLOW
    elif line.startswith("FIX"):
        color = GREEN
    elif line.startswith("TIP"):
        color = CYAN
    print(color + line + RESET)












