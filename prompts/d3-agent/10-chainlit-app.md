Create src/day3/chainlit_app.py that wraps the agent in a chat interface:

1. Import the agent from agent.py
2. Use @cl.on_chat_start to show a welcome message explaining the two stores
3. Use @cl.on_message to send user messages to the agent
4. Stream the agent's response back to the chat
5. Show the agent's thinking (Thought/Action) as intermediate steps

Run with: chainlit run src/day3/chainlit_app.py

Test the chat with questions in Portuguese. The agent should decide autonomously
which store to query -- no manual intervention. This is the moment: the agent
decides alone.
