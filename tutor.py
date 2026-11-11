"""
tutor.py
AI Tutor chat powered by Groq. Maintains conversation history per session.
"""
from groq import Groq

GROQ_API_KEY = "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"

SYSTEM_PROMPT = """You are LearnCraft Tutor — a friendly, encouraging, and highly knowledgeable AI tutor.
Your role is to help students understand topics deeply, answer their questions clearly, and guide them
step-by-step when they are confused.

Guidelines:
- Be concise but thorough. Use examples and analogies generously.
- If a student seems confused, break things down into smaller steps.
- Celebrate correct answers and effort warmly.
- Never just give answers to homework — guide the student to figure it out.
- Format responses with clear structure (use short paragraphs, numbered steps where helpful).
- Keep responses under 200 words unless a complex explanation is needed.
- Always end with a follow-up question or encouragement to keep the student engaged.
"""


def get_tutor_reply(messages: list, topic: str = "") -> str:
    """
    Send conversation history to Groq and return the tutor's reply.
    messages: list of {"role": "user"/"assistant", "content": str}
    """
    system = SYSTEM_PROMPT
    if topic:
        system += f"\n\nThe student is currently studying: {topic}. Focus your answers around this topic when relevant."

    try:
        client = Groq(api_key=GROQ_API_KEY)
        response = client.chat.completions.create(
            model=
def generate_flashcards(topic: str, level: str, num_cards: int = 10) -> list:
    """Generate flashcards for all difficulty levels."""

    difficulty_instructions = {
        "beginner": """
        Use simple language.
        Focus on basic definitions and fundamental concepts.
        Avoid complicated terminology.
        """,

        "intermediate": """
        Assume the learner understands the fundamentals.
        Focus on practical applications, comparisons,
        working principles and conceptual understanding.
        Include moderate technical terminology.
        """,

        "advanced": """
        Assume strong knowledge of the fundamentals.
        Focus on complex concepts, deeper technical details,
        problem-solving, limitations and real-world scenarios.
        Use precise technical terminology.
        Avoid basic or repetitive questions.
        """
    }

    difficulty = difficulty_instructions.get(
        level.strip().lower(),
        difficulty_instructions["beginner"]
    )

    prompt = f"""
    Generate exactly {num_cards} educational flashcards.

    Topic: {topic}
    Difficulty: {level}

    DIFFICULTY GUIDELINES:
    {difficulty}

    REQUIREMENTS:
    1. Every question must be relevant to the topic.
    2. Questions must match the selected difficulty.
    3. Front must contain a question or term (maximum 15 words).
    4. Back must contain a clear answer (maximum 40 words).
    5. Avoid duplicate questions.
    6. Answers must be factually accurate.

    OUTPUT FORMAT:
    Return ONLY valid JSON in this structure:

    {{
        "cards": [
            {{
                "front": "Question here",
                "back": "Answer here"
            }}
        ]
    }}

    Do not include markdown or explanations outside JSON.
    """

    try:
        client = Groq(api_key=GROQ_API_KEY)

        response = client.chat.completions.create(
            model="openai/gpt-oss-120b",
            messages=[
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            response_format={"type": "json_object"},
            max_tokens=3000
        )

        raw = response.choices[0].message.content

        if not raw:
            raise ValueError("Empty response from Groq.")

        data = json.loads(raw.strip())
        cards = data.get("cards", [])

        if not isinstance(cards, list) or len(cards) == 0:
            raise ValueError("No flashcards returned.")

        return cards[:num_cards]

    except Exception as e:
        print("Flashcard Error:", repr(e))
        return [{
            "front": "Generation failed",
            "back": str(e)
        }]
,
            messages=[{"role": "system", "content": system}] + messages,
            max_tokens=400,
            temperature=0.7,
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        return f"Sorry, I couldn't connect right now. Please try again! (Error: {str(e)})"
