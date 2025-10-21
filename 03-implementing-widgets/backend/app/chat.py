from __future__ import annotations

from typing import Any, AsyncIterator, AsyncGenerator
import asyncio

from agents import Agent, function_tool
from chatkit.agents import AgentContext, stream_agent_response
from chatkit.server import ChatKitServer, StreamingResult, stream_widget
from chatkit.types import (
    Attachment,
    ClientToolCallItem,
    ThreadItem,
    ThreadMetadata,
    ThreadStreamEvent,
    UserMessageItem,
    WidgetItem,
)
from chatkit.widgets import (
    WidgetRoot,
    Card,
    Button,
    Text,
    WidgetComponent
)
from chatkit.actions import ActionConfig
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
            # tools=[show_products],  # Add the streaming tool for Phase 2
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
 
        # Phase 1: Static widget rendering
        # Uncomment the following block to test Phase 1 (static product card)
        #
        if "show products" in user_text.lower():
            widget = Card(  
            children=[  
                Text(value="iPhone 17 Pro"),  
                Text(value="$999"),  
                Button(  
                    label="Add to Cart",  
                    onClickAction=ActionConfig(  
                        type="add_to_cart",  
                        payload={"product": "iphone17pro"}  
                    )  
                )  
            ]  
        )  
            # Stream a widget response
            async for event in stream_widget(
                thread,
                widget
                
            ):
                yield event
 
        # Phase 2: Streaming widgets via agent tool
        # The agent now has the show_products tool. When user says "show products",
        # the agent will call the tool, which streams the widget progressively.
        # No additional code needed here; the agent handles it.
 
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
    
    # Phase 3: Client-side actions
    # This method handles widget actions. For Phase 3, actions are handled client-side,
    # but this method can be used for server-side action processing in later phases.
    async def action(self, thread: ThreadMetadata, action, sender, context) -> AsyncIterator[ThreadStreamEvent]:
        card = Card(children=[Text(value="Added to cart!")])
        
        if action.type == "add_to_cart":
            async for event in stream_widget(
                thread,
                card,
            ):
                yield event


def create_chatkit_server() -> MyChatKitServer:
    """Factory function to create the ChatKit server instance."""
    return MyChatKitServer()


# Phase 2: Streaming widgets via @function_tool
@function_tool
async def show_products() -> AsyncGenerator[WidgetRoot, None]:
    """Stream a product card widget with progressive updates."""
    # Initial product card
    card = Card(
        children=[
            Text(value="iPhone 17 Pro"),
            Text(value="$999"),
            Button(
                label="Add to Cart",
                onClickAction=ActionConfig(
                    type="add_to_cart",
                    payload={"product": "iphone17pro"}
                )
            )
        ]
    )
    yield card
    
    await asyncio.sleep(1)  # Simulate loading more details
    
    # Update with additional info
    card.children.append(Text(value="In stock: 5 units"))
    yield card