import asyncio
import json
import random
import aiohttp
from transformers import AutoModelForCausalLM, AutoTokenizer, pipeline

CONTEXT_FILE = "CONTEXT.txt"
EVENTS_FILE = "events.json"
MODEL_NAME = "Cr0n3/h0l0-3.4.2-13b-uncen"

tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)
model = AutoModelForCausalLM.from_pretrained(MODEL_NAME)

text_generator = pipeline("text-generation", model=model, tokenizer=tokenizer)

def read_context(truncate_length=100000):
    try:
        with open(CONTEXT_FILE, "r", encoding="utf-8") as file:
            content = file.read().strip()
            return content[-truncate_length:] if len(content) > truncate_length else content
    except FileNotFoundError:
        return ""

def write_context(new_entry):
    with open(CONTEXT_FILE, "a", encoding="utf-8") as file:
        file.write(f"{new_entry}\n")

def load_events():
    try:
        with open(EVENTS_FILE, "r", encoding="utf-8") as file:
            data = json.load(file)
            return data.get("events", [])
    except FileNotFoundError:
        print(f"Error: {EVENTS_FILE} not found.")
        return []
    except json.JSONDecodeError:
        print(f"Error: {EVENTS_FILE} is not a valid JSON file.")
        return []

def generate_random_event():
    events = load_events() #List of random events to generate more entropy.
    if not events:
        print("No prompts available. Please check the prompts.json file.")
        return "Continue the story."
    return random.choice(events)

def get_answer(input_text):
    names_to_exclude = ["CR0N3", "HOLO", "Cr0n3", "Dr. Cr0n3", "Cronus Vossman", "Cronus", "Vossman"]

    placeholders = {}
    for name in names_to_exclude:
        placeholder = f"{{{{{name}}}}}"
        input_text = input_text.replace(name, placeholder)
        placeholders[placeholder] = name

    context = read_context()
    prompt = f"{context}\n{input_text}"

    completion = text_generator(prompt, max_length=5000, temperature=1.0, top_p=0.95)
    generated_text = completion[0]["generated_text"]

    if "." in generated_text:
        truncated_text = generated_text[:generated_text.rfind(".") + 1]
    else:
        truncated_text = generated_text

    for placeholder, name in placeholders.items():
        truncated_text = truncated_text.replace(placeholder, name)

    return truncated_text.replace('"', "")


async def send_to_api(entry):
    url = "http://localhost:4030/process-h0l0"
    async with aiohttp.ClientSession() as session:
        try:
            async with session.post(url, json={"entry": entry}) as response:
                response_text = await response.text()
                print(f"API response: {response_text}")
        except Exception as e:
            print(f"Failed to send to API: {e}")

async def main():
    print("Continue story generation.")
    iteration = 0

    # variant for lm-studio with OpenAI package

    # client = OpenAI(base_url="http://localhost:1234/v1", api_key="lm-studio")
    #
    # messages = [
    #     {"role": "system", "content": system_message},
    #     {"role": "user", "content": f"{context} \n {input_text}"}
    # ]
    #
    # completion = client.chat.completions.create(
    #     model="h0l0-3.4.2-13b-uncen",
    #     messages=messages,
    #     temperature=1,
    #     max_completion_tokens=5000,
    #     logprobs=3,
    #     top_p=0.92,
    #     frequency_penalty=1.15,
    #     presence_penalty=0.9
    # )

    while True:
        prompt = "Continue the story." if iteration % 2 == 0 else generate_random_event()
        new_entry = get_answer(prompt)
        write_context(new_entry)
        send_to_api(new_entry)
        print(new_entry)
        iteration += 1
        await asyncio.sleep(1)

if __name__ == "__main__":
    asyncio.run(main())
