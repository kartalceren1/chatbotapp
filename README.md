# AI Interview Helper

A web application that provides mock interviews using AI. Users can choose a persona (HR, Tech, Manager), answer questions, and receive feedback and guidance in a natural, conversational way. Powered by OpenAI's GPT-4o-mini model.

## Live Demo

The app is deployed and running on Render! You can try it here:  

[AI Interview Helper on Render](https://chatbotapp-dzwd.onrender.com)

## Features

- **Multiple Personas**: HR, Tech, and Manager interview styles.  
- **Interactive Chat**: AI responds naturally to answers and provides feedback on request.  
- **Dynamic Questions**: Randomized questions from JSON files.  
- **Frontend**: Responsive chat interface with styled message bubbles.  
- **Rate Limiting**: Protects the backend from excessive requests.  


## Technologies Used

- **Backend**: Python, Flask, Flask-Limiter  
- **Frontend**: HTML, CSS, JavaScript  
- **AI Integration**: OpenAI GPT-4o-mini  


## Usage

1. Go to the homepage.

2. Select a persona: HR, Tech, or Manager.

3. Start the mock interview.

4. Type your answer in the chat.

5. When ready for formal feedback, type:

Ok, I want my feedback now

6. The AI will provide a score, feedback paragraph, and practical tip.


## Installation
- **Clone the repository:**
  
git clone https://github.com/kartalceren1/mtapplication.git

cd chatbotapp

- **Create and activate a virtual environment:**
  
python3 -m venv venv

source venv/bin/activate   

On Windows: venv\Scripts\activate

- **Install the Python dependencies:**
  
pip install -r requirements.txt

