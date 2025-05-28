def get_formatted_prompt(number_of_events: int, prompt: str) -> str:
    return prompt.format(number_of_events=number_of_events)
