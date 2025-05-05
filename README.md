# Mini Conlang Chatbot

A simple single-page web application built with Streamlit that allows you to chat with a Google Generative AI model (Gemini) instructed on the rules of the Mini conlang.

## Setup

1.  **Clone/Download:** Get the `app.py`, `requirements.txt`, and `mini_system_prompt.txt` files into a single directory.
2.  **Get API Key:** Obtain an API key from [Google AI Studio](https://aistudio.google.com/app/apikey).
3.  **Install Dependencies:** Open your terminal in the project directory and run:
    ```bash
    pip install -r requirements.txt
    ```
4.  **Ensure Prompt File:** Make sure the `mini_system_prompt.txt` file containing the Mini language specification is present in the same directory as `app.py`.

## Running the App

1.  Open your terminal in the project directory.
2.  Run the Streamlit app:
    ```bash
    streamlit run app.py
    ```
3.  The app will open in your web browser.
4.  Enter your Google AI API Key in the sidebar when prompted.
5.  Start chatting!

## Notes

*   The chatbot's knowledge of Mini is based entirely on the content of `mini_system_prompt.txt`.
*   The system prompt used (`mini_system_prompt.txt`) is quite large. Depending on the specific Gemini model used (default is `gemini-1.5-flash-latest`) and the length of your conversation, you might encounter context length limits or other API errors (like InvalidArgument). If this happens, you may need to:
    *   Use a model with a larger context window if available.
    *   Further shorten the content within `mini_system_prompt.txt` (e.g., remove less critical grammar examples or sentence pairs).
*   Your API key is not stored by the application; it's only used for the current session in your browser. 