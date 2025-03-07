# AI Newsletter Generator

An AI-powered Apify actor that generates well-structured newsletters using a crew of specialized AI agents. The system uses CrewAI to coordinate multiple agents that research, write, and edit newsletter content based on user input.

## Features

- Multi-agent system using CrewAI
- Specialized agents for research, writing, and editing
- Markdown-formatted output
- Configurable newsletter sections
- Google's Gemini Pro LLM integration
- Apify Actor integration for scalable deployment

## Prerequisites

- Python 3.10+
- Google API key for Gemini Pro
- Apify CLI (for local development)

## Local Development

1. Clone the repository:
```bash
git clone [repository-url]
cd newsletter-agent
```

2. Install Apify CLI if you haven't already:
```bash
npm install -g apify-cli
```

3. Create a virtual environment and activate it:
```bash
python -m venv .venv
source .venv/bin/activate  # On Windows, use `.venv\Scripts\activate`
```

4. Install dependencies:
```bash
pip install -r requirements.txt
```

5. Create a `.env` file in the root directory and add your Google API key:
```
GOOGLE_API_KEY=your_api_key_here
```

## Running Locally

1. Run the actor using Apify CLI:
```bash
apify run
```

The actor will use the input from `storage/key_value_stores/default/INPUT.json`. You can modify this file to change the newsletter topic.

## Deploying to Apify

1. Log in to Apify:
```bash
apify login
```

2. Push the actor to Apify platform:
```bash
apify push
```

## Input

The actor accepts the following input:

```json
{
    "topic": "Your newsletter topic or requirements"
}
```

Example:
```json
{
    "topic": "I want to know everything about AI agents – current news, AI agentic platforms and frameworks, and companies in this field."
}
```

## Output

The actor outputs a dataset containing:
- Generated newsletter content in markdown format
- Topic information
- Generation status
- Timestamp

## Project Structure

```
newsletter-agent/
├── .actor/
│   ├── actor.json          # Actor configuration
│   ├── Dockerfile         # Docker build instructions
│   └── input_schema.json  # Input schema definition
├── src/
│   ├── agents/
│   │   ├── researcher.py  # Research agent implementation
│   │   ├── writer.py      # Content writer agent
│   │   └── editor.py      # Editor agent
│   ├── config/
│   │   └── config.py      # Configuration settings
│   ├── tools/             # Scraping and processing tools
│   ├── newsletter_crew.py # Agent coordination
│   └── main.py           # Entry point
├── requirements.txt       # Python dependencies
└── README.md
```

## Customization

You can customize the newsletter sections by modifying the `DEFAULT_NEWSLETTER_SECTIONS` list in `src/config/config.py`.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the LICENSE file for details.
