class AssistantAgent:
    def __init__(self, llm):
        self.llm = llm
        self.reset()

    def reset(self):
        self.messages = [
            {
                "role": "system",
                "content": (
                    "You are a helpful general-purpose AI assistant. "
                    "Respond naturally and help the user accomplish their goal. "
                    "Keep each response concise and conversational, usually 2-5 sentences. "
                    "Do not provide exhaustive reports, long checklists, or large tables unless "
                    "the user explicitly asks for them. "
                    "When more information is needed, ask one or two focused follow-up questions "
                    "instead of trying to solve everything at once."
                ),
            }
        ]

    def next_turn(
        self,
        user_message: str,
    ) -> str:

        self.messages.append(
            {
                "role": "user",
                "content": user_message,
            }
        )

        response = self.llm.generate(
            self.messages,
        )

        self.messages.append(
            {
                "role": "assistant",
                "content": response,
            }
        )

        return response
