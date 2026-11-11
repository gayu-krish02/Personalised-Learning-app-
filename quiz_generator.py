import json
from groq import Groq

GROQ_API_KEY = "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"


def generate_quiz(topic, level, num_questions, q_type):
    if q_type != "Mixed":
        type_instruction = "All questions must be type: " + q_type + "."
    else:
        type_instruction = "Mix these types: Multiple Choice, True/False, Fill in the Blank, Short Answer."

    prompt = (
        "Generate " + str(num_questions) + " quiz questions about '" + topic + "' at " + level + " level.\n"
        + type_instruction + "\n\n"
        "Return ONLY a JSON object with key 'questions' (array).\n"
        "Each question needs:\n"
        "  - type: one of 'Multiple Choice', 'True/False', 'Fill in the Blank', 'Short Answer'\n"
        "  - question: the question text (for Fill in the Blank, use ___ for the blank)\n"
        "  - options: 4 strings for MC, ['True','False'] for TF, [] for others\n"
        "  - answer: the correct answer string\n"
        "  - explanation: one sentence explaining why\n\n"
        "JSON only, no markdown, no backticks, no extra text."
    )

    try:
        client = Groq(api_key=GROQ_API_KEY)
        r = client.chat.completions.create(
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
            messages=[{"role": "user", "content": prompt}],
            max_tokens=1500
        )
        raw = r.choices[0].message.content.strip()
        if raw.startswith("```"):
            raw = raw.split("```", 2)[1]
            if raw.startswith("json"):
                raw = raw[4:]
        data = json.loads(raw.strip())
        return {
            "title": topic.title() + " Quiz",
            "topic": topic.title(),
            "difficulty": level,
            "questions": data["questions"]
        }
    except Exception as e:
        # Fallback single question so app never crashes
        return {
            "title": topic.title() + " Quiz",
            "topic": topic.title(),
            "difficulty": level,
            "questions": [
                {
                    "type": "Short Answer",
                    "question": f"Quiz generation failed ({str(e)}). Please retry.",
                    "options": [],
                    "answer": "retry",
                    "explanation": "An error occurred while generating the quiz."
                }
            ]
        }
