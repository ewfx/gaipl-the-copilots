import streamlit as st
from openai import OpenAI


#ENTER API key below to enable OpenAI powered chat
client = OpenAI(api_key="<YOUR OPENAI API KEY>")


def main():
    # Page Configuration
    st.set_page_config(page_title="WF Integrated Platform", layout="wide")

    # Custom Styling
    st.markdown(
        """
        <style>
        body {
            background-color: #f8f8f8;
        }
        .banner {
            background-color: #cc0000;
            padding: 10px;
            text-align: center;
            font-size: 20px;
            font-weight: bold;
            color: white;
            border-radius: 5px;
        }
        .info-box {
            background-color: #e6e6e6;
            padding: 10px;
            margin: 10px 0;
            border-radius: 5px;
            font-size: 16px;
            font-weight: bold;
            text-align: center;
        }
        </style>
        """,
        unsafe_allow_html=True
    )

    # Banner
    st.markdown('<div class="banner">WF Integrated Platform Environment</div>', unsafe_allow_html=True)

    # Session state to track pages
    if 'page' not in st.session_state:
        st.session_state.page = "home"
    if 'messages' not in st.session_state:
        st.session_state.messages = []

    if st.session_state.page == "home":
        show_home()
    elif st.session_state.page == "chatbot":
        show_chatbot()
    elif st.session_state.page == "deploy_scripts":
        show_deploy_scripts()

def show_home():
    st.subheader("Application Selection")
    application_id = st.selectbox("Application ID", ["Select an option", "App1", "App2", "App3"], index=0)

    if application_id != "Select an option":
        environment = st.selectbox("Target Environment", ["Select an option", "DEV", "TEST", "PROD"], index=0)

        if environment != "Select an option":
            if st.button("Proceed to Chatbot"):
                st.session_state.page = "chatbot"
                st.session_state.application_id = application_id
                st.session_state.environment = environment
                st.rerun()

def show_chatbot():
    st.markdown(f'<div class="info-box">Application: {st.session_state.application_id} | Environment: {st.session_state.environment}</div>', unsafe_allow_html=True)

    col1, col2 = st.columns([1, 3])

    with col1:
        st.subheader("Quick Links")
        st.write("[View Application Health metrics](#)")
        st.write("[View Application Job Logs](#)")
        st.write("[Knowledge base](#)")

        st.subheader("Actions")
        if st.button("Deploy scripts"):
            st.session_state.page = "deploy_scripts"
            st.rerun()
        if st.button("Select different application"):
            st.session_state.page = "home"
            st.rerun()

    with col2:
        st.subheader("AI Chatbot Support")
        for message in st.session_state.messages:
            st.chat_message(message["role"]).write(message["content"])

        user_input = st.chat_input("Ask something...")
        if user_input:
            st.session_state.messages.append({"role": "user", "content": user_input})
            response = get_openai_response(user_input)
            st.session_state.messages.append({"role": "assistant", "content": response})
            st.rerun()

def get_openai_response(prompt):
      # Replace with your actual API key
    response = client.chat.completions.create(model="gpt-3.5-turbo",
    messages=[{"role": "system", "content": "You are a helpful assistant."},
              {"role": "user", "content": prompt}])
    return response.choices[0].message.content

def show_deploy_scripts():
    st.subheader("Deploy Scripts")
    st.write("Feature to run scripts in Git directly from UI will be added here.")

    if st.button("Go Back"):
        st.session_state.page = "chatbot"
        st.rerun()

if __name__ == "__main__":
    main()
