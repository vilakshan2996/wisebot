from langchain.memory import ConversationBufferWindowMemory

memory = ConversationBufferWindowMemory(k=3, return_messages=True)

def load_memory(st) -> ConversationBufferWindowMemory:
    """Load memory from session state

    Args:
        st: streamlit object

    Returns:
        memory_loader: ConversationBufferMemory object
    """
   

    if "messages" not in st.session_state:
        st.session_state["messages"] = [
            {"role": "assistant", "content": "How can I help you?"}
        ]
    print(memory.load_memory_variables({}))
    for index, msg in enumerate(st.session_state.messages):
        st.chat_message(msg["role"]).write(msg["content"])
        if msg["role"] == "user" and index < len(st.session_state.messages) - 1:
            memory.save_context(
                {"input": msg["content"]},
                {"output": st.session_state.messages[index + 1]["content"]},
            )

    return memory