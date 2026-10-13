# test_sdk.py

from sdk.llm_service import llm_task


@llm_task(system_prompt="You are a helpful assistant. Be concise.")
def ask_question(question):
    return question


@llm_task(system_prompt="Summarize the following text in 3 bullet points.")
def summarize(text):
    return text


@llm_task(system_prompt="Classify this text as 'positive', 'negative', or 'neutral'. Reply with one word only.")
def classify_sentiment(text):
    return text


if __name__ == "__main__":
    print("=" * 50)
    print("Test 1: Simple question")
    print("=" * 50)
    answer = ask_question("What is the capital of Saudi Arabia?")
    print(f"Answer: {answer}\n")

    print("=" * 50)
    print("Test 2: Summarize")
    print("=" * 50)
    summary = summarize(
        "Rewaa is a Saudi retail-tech startup that provides inventory management "
        "and POS systems for small and medium businesses. They raised 72.8 million "
        "dollars in funding and serve over 7000 merchants across the Kingdom. "
        "They are part of the Saudi Unicorns Program backed by MCIT."
    )
    print(f"Summary: {summary}\n")

    print("=" * 50)
    print("Test 3: Classify sentiment")
    print("=" * 50)
    label = classify_sentiment("This product is amazing, I love it!")
    print(f"Sentiment: {label}\n")

    print("All tests passed! SDK is working. ✅")