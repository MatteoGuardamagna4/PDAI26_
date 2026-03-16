"""
Class that defines the agent that processes the triage reports
and updates the database. The agent uses the Cohere API to process
the natural language commands and route the information to the right
tool function with the right arguments.
"""

# Agent class
import json

import cohere
import database as db


class TriageAgent:
    """
    Agent that processes the triage reports and updates the database.
    """

    tools = [
        {
            "type": "function",
            "function": {
                "name": "add_record",
                "description": "Adds a new patient record to the database",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "age": {
                            "type": "integer",
                            "description": "the age of the patient"
                        },
                        "temperature": {
                            "type": "number",
                            "description": "the temperature of the patient"
                        },
                        "reason_visit": {
                            "type": "string",
                            "description": "the reason for the patient's visit"
                        },
                        "tests_performed": {
                            "type": "string",
                            "description": "the tests performed on the patient"
                        },
                        "diagnosis": {
                            "type": "string",
                            "description": "the diagnosis of the patient",
                        }
                    },
                    "required": ["reason_visit"],
                },
            },
        },

        {
            "type": "function",
            "function": {
                "name": "release_patient",
                "description": "Releases the first patient in the queue",
                "parameters": {
                    "type": "object",
                    "properties": {},
                    "required": [],
                },
            },
        }
    ]

    SYSTEM_PROMPT = """
    You are an agent that processes triage reports one by one,
    without responding. 
    Your task is to route the information to the right tool function
    with the right arguments.
    """

    def __init__(self):
        with open("cohere.key", encoding="utf-8") as f:
            cohere_api_key = f.read()
        self.cohere_client = cohere.ClientV2(cohere_api_key)


    def process_command(self, input_text):
        """
        Process the natural language command.
        """

        messages = [
            {'role': 'system', 'content': self.SYSTEM_PROMPT},
            {'role': 'user', 'content': input_text}
        ]

        response = self.cohere_client.chat(
            model="command-a-03-2025", messages=messages, tools=self.tools
        )

        if response.message.tool_calls:

            for tool_call in response.message.tool_calls:
                if tool_call.function.name == "add_record":
                    raw_args = tool_call.function.arguments  # <- not tool_call["arguments"]

                    if isinstance(raw_args, str):
                        arguments = json.loads(raw_args) if raw_args else {}
                    elif isinstance(raw_args, dict):
                        arguments = raw_args
                    else:
                        arguments = {}
                    print("Parsed arguments:", arguments)
                    db.add_record(**arguments)
                elif tool_call.function.name == "release_patient":
                    db.release_patient()
                else:
                    pass

        return response
