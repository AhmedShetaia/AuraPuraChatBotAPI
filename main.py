from fastapi import FastAPI, Form, Request
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from langchain.prompts import PromptTemplate
from langchain.chains import ConversationChain
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.memory import ConversationSummaryMemory

# Define calming prompts for each state
calm_prompts = {
    "depression": """
        You are a calming and empathetic chatbot. If a user is feeling depressed, respond with gentle, positive, and encouraging messages.
        Example:
        - "I'm here to listen. You are stronger than you think."
        - "Sometimes, small steps lead to big changes. Let's start by finding something good in your day."
    """,
    "anxiety": """
        You are a calming and supportive chatbot. If a user is anxious, respond with messages that help them feel grounded and safe.
        Example:
        - "Take a deep breath with me. Inhale... exhale... You are safe."
        - "Let’s try grounding exercises together. Look around and name 3 things you see."
    """,
    "stress": """
        You are a soothing chatbot. If a user is stressed, respond with relaxing and reassuring messages.
        Example:
        - "Let’s pause and take a moment to relax. What helps you feel calm?"
        - "Stress is tough, but you can handle it. Let’s find one thing to ease your mind."
    """
}

# Function to generate a dynamic prompt based on user's state
def generate_prompt(state_scores):
    prompt = "You will respond empathetically based on the user's emotional states:\n\n"
    for state, score in state_scores.items():
        if score > 0:  # Include only states with a non-zero score
            prompt += calm_prompts[state] + f"\n(Current state: {state} at {score}%)\n\n"
    prompt += "Respond thoughtfully to help the user calm down."
    return prompt

# Initialize FastAPI app
app = FastAPI()

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Route for chatbot interaction
@app.post("/chat/")
async def chat(
    google_api_key: str = Form(...),
    user_input: str = Form(...),
    depression: int = Form(0),
    anxiety: int = Form(0),
    bipolar: int = Form(0),
    stress: int = Form(0)
):
    try:
        # Initialize memory and chatbot
        memory = ConversationSummaryMemory(
            llm=ChatGoogleGenerativeAI(api_key=google_api_key, model="gemini-1.5-pro"),
            max_token_limit=1000
        )
        chatbot = ConversationChain(
            llm=ChatGoogleGenerativeAI(api_key=google_api_key, model="gemini-1.5-pro"),
            memory=memory
        )

        # Generate dynamic prompt
        state_scores = {
            "depression": depression,
            "anxiety": anxiety,
            "bipolar": bipolar,
            "stress": stress
        }
        dynamic_prompt = generate_prompt(state_scores)

        # Generate response
        response = chatbot.run(dynamic_prompt + f"\n\nUser: {user_input}\nBot:")
        return JSONResponse({"response": response})

    except Exception as e:
        return JSONResponse({"error": str(e)}, status_code=500)
