# NovaSense AI — Customizable Multimodal Intelligent Assistant

NovaSense AI is a Streamlit-based intelligent assistant designed for university FAQ support and general smart responses. It combines a clean chat interface, semantic question matching, voice input, text-to-speech output, theme switching, and an editable FAQ knowledge base.

The repository is built around two main files:

* `app.py` — Streamlit user interface
* `backend.py` — semantic FAQ assistant backend

\---

## Overview

NovaSense AI provides a practical assistant interface where users can ask questions through text or voice. The assistant searches a university FAQ dataset, identifies the most semantically similar question, and returns the matching answer.

Instead of relying on exact keyword matching, the project uses sentence embeddings through `sentence-transformers`. This helps the assistant understand the meaning of a user query even when the wording is different from the stored FAQ question.

\---

## Key Features

### Interactive Streamlit Chat Interface

* Wide-layout Streamlit application.
* Chat-style user and assistant message bubbles.
* Persistent conversation history using Streamlit session state.
* Clear chat option from the sidebar.

### Semantic FAQ Matching

* Loads questions and answers from a CSV file.
* Uses `SentenceTransformer('paraphrase-MiniLM-L6-v2')` to generate embeddings.
* Compares the user query with stored FAQ questions using cosine similarity.
* Returns the answer corresponding to the closest semantic match.

### Voice Input

* Supports microphone-based input using `speech\_recognition`.
* Converts spoken input into text using Google speech recognition.
* Automatically sends the recognized text to the assistant.

### Text-to-Speech Output

* Uses `pyttsx3` for voice responses.
* Runs speech output asynchronously using threading.
* Allows users to enable or disable voice output from the sidebar.

### Add New FAQ Knowledge

* Users can add new question-answer pairs directly from the sidebar.
* New entries are appended to the FAQ CSV file.
* The cached assistant resource is cleared after adding knowledge so the assistant can reload updated data.

### Theme Toggle

* Sidebar option to switch between Light and Dark modes.
* Dark mode applies custom CSS for a darker interface appearance.

### Optional Translation Support

* The backend attempts to import `googletrans`.
* If available, user queries are translated into English before semantic matching.
* If unavailable, the assistant continues to work without translation.

\---

## Tech Stack

|Category|Tools / Libraries|
|-|-|
|Web App|Streamlit|
|Data Handling|Pandas|
|NLP / Semantic Search|SentenceTransformers|
|Similarity Matching|PyTorch, `sentence\_transformers.util`|
|Voice Input|SpeechRecognition|
|Text-to-Speech|pyttsx3|
|Threading|Python threading|
|Optional Translation|googletrans|

\---

## Project Structure

```text
project-root/
├── app.py
├── backend.py
├── university\_faq\_v2.csv
├── requirements.txt
└── README.md
```

### File Description

|File|Purpose|
|-|-|
|`app.py`|Main Streamlit application. Handles UI, sidebar controls, chat display, voice input, voice output, and FAQ addition.|
|`backend.py`|Backend assistant logic. Loads FAQ data, creates sentence embeddings, performs similarity matching, and returns responses.|
|`university\_faq\_v2.csv`|FAQ knowledge base containing questions and answers.|
|`requirements.txt`|Python dependencies required to run the project.|
|`README.md`|Project documentation.|

\---

## Dataset Format

The project expects a CSV file named:

```text
university\_faq\_v2.csv
```

The CSV file must contain at least the following columns:

```text
Question,Answer
```

Example:

```csv
Question,Answer
What is the admission process?,You can apply through the university admission portal during the announced admission period.
What are the office timings?,The office is open from 9:00 AM to 4:00 PM from Monday to Friday.
```

If the required `Question` and `Answer` columns are missing, the backend raises an error.

\---

## Installation

### 1\. Clone the Repository

```bash
git clone https://github.com/your-username/your-repository-name.git
cd your-repository-name
```

### 2\. Create a Virtual Environment

```bash
python -m venv .venv
```

Activate it:

**Windows**

```bash
.venv\\Scripts\\activate
```

**macOS / Linux**

```bash
source .venv/bin/activate
```

### 3\. Install Dependencies

```bash
pip install -r requirements.txt
```

Suggested `requirements.txt`:

```text
streamlit
pandas
torch
sentence-transformers
SpeechRecognition
pyttsx3
googletrans==4.0.0-rc1
pyaudio
```

> Note: `pyaudio` may require extra installation steps depending on the operating system. If microphone input is not needed, the text-based assistant can still run without voice input configuration.

\---

## How to Run

From the project root, run:

```bash
streamlit run app.py
```

Then open the local Streamlit URL shown in the terminal, usually:

```text
http://localhost:8501
```

\---

## How the Application Works

### 1\. Load the Assistant

The Streamlit app loads the assistant using:

```python
DevNovaAssistant("university\_faq\_v2.csv")
```

The assistant reads the FAQ dataset and validates that it contains `Question` and `Answer` columns.

### 2\. Generate Question Embeddings

All FAQ questions are encoded using:

```python
SentenceTransformer('paraphrase-MiniLM-L6-v2')
```

These embeddings are stored in memory for fast semantic matching.

### 3\. Process User Query

When the user enters text or speaks through the microphone:

1. The query is received by the Streamlit app.
2. The query is passed to `bot.get\_response(user\_input)`.
3. The backend optionally translates the input into English.
4. The query is encoded into an embedding.
5. Cosine similarity is calculated against all FAQ question embeddings.
6. The answer with the highest matching score is returned.

### 4\. Display and Speak the Response

The assistant response is displayed in the chat window. If voice output is enabled, the response is also spoken using `pyttsx3`.

\---

## User Guide

### Text Chat

Type your question in the chat input box and press Enter.

### Voice Chat

Use the **Speak** button in the sidebar. The system listens through the microphone, converts speech to text, and sends it to the assistant.

### Enable or Disable Voice Output

Use the **Enable Voice Output** checkbox in the sidebar.

### Clear Chat

Click **Clear Chat** from the sidebar to reset the conversation.

### Add Knowledge

Use the **Add Knowledge** section in the sidebar:

1. Enter a new question.
2. Enter the corresponding answer.
3. Click **Add Knowledge**.
4. The new FAQ entry is saved to `university\_faq\_v2.csv`.

\---

## Screenshots

<img width="1910" height="958" alt="image" src="https://github.com/user-attachments/assets/6e29ccd5-067f-425b-87f9-189aff774f49" />
<img width="1912" height="963" alt="image" src="https://github.com/user-attachments/assets/8b122000-d5a4-4c84-b1c0-5d5583fe470f" />


## Strengths of the Project

* Simple and clean Streamlit interface.
* Semantic search gives better results than exact keyword matching.
* Supports both text and voice interaction.
* Allows knowledge base expansion without modifying backend code.
* Modular structure with separate frontend and backend files.
* Useful for university FAQ systems, help desks, and small knowledge assistants.

\---

## Limitations

* The assistant returns the closest FAQ answer even if the similarity is weak.
* No confidence threshold is currently used before returning an answer.
* The FAQ CSV file is updated directly, which is simple but not ideal for multi-user production systems.
* Voice input depends on microphone availability and speech recognition configuration.
* Translation support depends on the optional `googletrans` package.

\---

## Future Improvements

* Add a confidence threshold and fallback response for low-similarity queries.
* Display the confidence score with each response.
* Add admin authentication before allowing new FAQ entries.
* Store FAQ data in a database instead of a CSV file.
* Add support for document upload and retrieval.
* Improve multilingual support.
* Add deployment instructions for Streamlit Community Cloud.
* Add logging for user questions and unanswered queries.
* Add custom branding and responsive mobile styling.

\---

## Possible Use Cases

* University admission FAQ assistant.
* Student help desk chatbot.
* Department-level support assistant.
* Internal organization knowledge assistant.
* Voice-enabled information kiosk.
* FAQ chatbot prototype for small institutions.

\---

## Deployment Notes

For Streamlit Community Cloud deployment:

1. Push the repository to GitHub.
2. Ensure `requirements.txt` is included.
3. Ensure `university\_faq\_v2.csv` is included in the repository.
4. Set the main file as:

```text
app.py
```

5. Deploy from Streamlit Community Cloud.

\---

## License

This project can be released under license preferred by the repository owner.

\---

## Contact

Nafees Ayub
Data Scientist
nafeesayub@gmail.com
+923365901990

