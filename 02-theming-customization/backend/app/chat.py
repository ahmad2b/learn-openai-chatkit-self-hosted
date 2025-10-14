from __future__ import annotations

from typing import Any, AsyncIterator

from agents import Agent
from chatkit.agents import AgentContext, stream_agent_response
from chatkit.server import ChatKitServer
from chatkit.types import (
    Attachment,
    ClientToolCallItem,
    ThreadItem,
    ThreadMetadata,
    ThreadStreamEvent,
    UserMessageItem,
)
from openai.types.responses import ResponseInputContentParam
from agents import Runner

from .memory_store import MemoryStore


# Agent instructions
INSTRUCTIONS = """You are a helpful and friendly AI assistant.
Answer questions clearly and concisely. Be conversational and natural.
If you don't know something, say so honestly."""

MODEL = "gpt-4.1-mini"


class ChatAgentContext(AgentContext):
    """Context for the conversational agent including thread and storage."""
    store: MemoryStore
    request_context: dict[str, Any]


def _extract_user_text(item: UserMessageItem) -> str:
    """Extract text content from a user message."""
    parts: list[str] = []
    for part in item.content:
        text = getattr(part, "text", None)
        if text:
            parts.append(text)
    return " ".join(parts).strip()


class MyChatKitServer(ChatKitServer[dict[str, Any]]):
    """
    Custom ChatKit server implementation for conversational Agent.

    Handles user messages and streams AI assistant responses.
    """

    def __init__(self) -> None:
        self.store: MemoryStore = MemoryStore()
        super().__init__(self.store)

        # Create agent with conversational capabilities
        self.assistant = Agent[ChatAgentContext](
            model=MODEL,
            name="AI Assistant",
            instructions=INSTRUCTIONS,
            tools=[],  # No additional tools configured
        )

    async def respond(
        self,
        thread: ThreadMetadata,
        input: ThreadItem | None,
        context: dict[str, Any],
    ) -> AsyncIterator[ThreadStreamEvent]:
        """
        Core method that processes user messages and streams agent responses.

        Flow:
        1. Check if input is a user message (ignore others)
        2. Extract text from user message
        3. Create agent context
        4. Run agent with user input
        5. Stream response events back to client
        """
        # Ignore None input
        if input is None:
            return

        # Ignore client tool calls (not implemented)
        if isinstance(input, ClientToolCallItem):
            return

        # Only process user messages
        if not isinstance(input, UserMessageItem):
            return

        # Create agent context
        agent_context = ChatAgentContext(
            thread=thread,
            store=self.store,
            request_context=context,
        )

        # Extract user text
        user_text = _extract_user_text(input)
        if not user_text:
            return

        # Run agent (streamed mode)
        result = Runner.run_streamed(
            self.assistant,
            user_text,
            context=agent_context,
        )

        # Stream agent response events
        async for event in stream_agent_response(agent_context, result):
            yield event

    async def to_message_content(self, _input: Attachment) -> ResponseInputContentParam:
        """File attachments are not supported in this implementation."""
        raise RuntimeError("File attachments are not supported in this implementation.")


def create_chatkit_server() -> MyChatKitServer:
    """Factory function to create the ChatKit server instance."""
    return MyChatKitServer()