# mcq-generator/mcq-generator/README.md

# MCQ Generator

This project is a FastAPI application that generates multiple-choice questions (MCQs) based on a specified topic using the Ollama API. The generated MCQs are formatted in CSV and can be downloaded directly from the web interface.

## Features

- Generate MCQs by specifying a topic and the number of questions.
- Download the generated MCQs in CSV format.
- User-friendly web interface for input.

## Project Structure

```
mcq-generator
├── src
│   ├── main.py               # Entry point of the FastAPI application
│   ├── api
│   │   ├── __init__.py       # Marks the api directory as a package
│   │   └── routes.py         # Defines API routes for generating MCQs
│   ├── services
│   │   ├── __init__.py       # Marks the services directory as a package
│   │   ├── ollama_service.py  # Logic for interacting with the Ollama API
│   │   └── mcq_service.py     # Logic for processing and formatting MCQs
│   ├── models
│   │   ├── __init__.py       # Marks the models directory as a package
│   │   └── mcq.py            # Defines the MCQ model
│   ├── templates
│   │   ├── index.html        # Main HTML template for user input
│   │   └── base.html         # Base HTML template for layout
│   └── static
│       ├── css
│       │   └── style.css     # CSS styles for the web application
│       └── js
│           └── main.js       # JavaScript for client-side interactions
├── tests
│   ├── __init__.py           # Marks the tests directory as a package
│   ├── test_api.py           # Unit tests for API routes
│   └── test_services.py      # Unit tests for service functions
├── requirements.txt          # Project dependencies
├── .env                      # Environment variables for configuration
└── README.md                 # Project documentation
```

## Installation

1. Clone the repository:
   ```
   git clone https://github.com/Xer0bit/MCQs-bot
   cd MCQs-bot
   ```

2. Install the required dependencies:
   ```
   pip install -r requirements.txt
   ```

3. Set up environment variables in the `.env` file.

## Usage

1. Run the application:
   ```
   uvicorn src.main:app --reload
   ```

2. Open your browser and navigate to `http://localhost:8000` to access the web interface.

## Contributing

Contributions are welcome! Please open an issue or submit a pull request for any improvements or bug fixes.

## License

This project is licensed under the MIT License.