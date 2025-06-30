# This could be a JSON file, but this is simpler to load and it allows for comments.

prompts = {
    "emotion": {
        "prompt": 'Return only the word "high", "neutral", or "low" depending on the degree to which the author of the report exhibits emotion. Respond with only one word.',
        "valid_responses": ["high", "neutral", "low"],
    },
    "passivity": {
        "prompt": 'Return only the word "active", "passive", or "neutral" depending on what best characterizes the grammar and style of the report. Respond with only one word.',
        "valid_responses": ["active", "passive", "neutral"],
    },
    "panic/shame": {
        "prompt": 'Return only the word "high", "neutral", or "low" depending on the degree to which the author of the report is exhibiting panic or expressing guilt or shame.',
        "valid_responses": ["high", "neutral", "low"],
    },
    "apologetic": {
        "prompt": 'Return only the number "high", "neutral", or "low" depending on the degree to which the author of the following report could be described as defensive and seeking to justify their own actions.',
        "valid_responses": ["high", "neutral", "low"],
    },
    "self-aware": {
        "prompt": 'Return only the number "high", "neutral", or "low" depending on the degree to which the author of the following report is aware of and attempting to manage their public image.',
        "valid_responses": ["high", "neutral", "low"],
    },
    "aware-of-other-reports": {
        "prompt": 'Return only the number "high", "neutral", or "low" depending on the degree to which the author of the following report is aware of other reports being shared or made public (e.g., in newspapers).',
        "valid_responses": ["high", "neutral", "low"],
    },
    "boring": {  # this prompt is not returning expected results
        "prompt": 'Return only the word "vivid", "neutral", or "boring" depending on the degree to which the author of the following report depicts events in a lively and engaging manner compared to a dull report. Respond with only one word',
        "valid_responses": ["vivid", "neutral", "boring"],
    },
    "in-a-word": {
        "prompt": "Return only one word that best describes the overall tone or manner of the following report. Respond with only one word",
        "valid_responses": 1,
    },
}
