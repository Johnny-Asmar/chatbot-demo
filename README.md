# AI Virtual Assistant Chatbot

A modern, intelligent chatbot application that combines web crawling, document processing, and AI-powered conversations using OpenAI's GPT models and vector databases.

## 🚀 Quick Start

### 1. Run the Backend
From the root directory of the project:
```bash
python -m src.app
```
This will start the Flask application.

### 2. Open the Interface
- Navigate to the `interface` folder
- Open `main.html` in your web browser
- Start chatting with your AI assistant!

## 📋 Prerequisites

- Python 3.8+
- Required packages in requirements.txt
- OpenAI API key

### Set OpenAI API Key
Edit `src/ai/ai_model.py` and add your OpenAI API key:
```python
os.environ["OPENAI_API_KEY"] = "your-api-key-here"
```

## 🌟 Features

- **Intelligent Q&A**: Ask questions about your documents and get AI-powered answers
- **Web Crawling**: Automatically crawl websites and download PDF documents
- **Vector Database**: Efficient document storage and retrieval using ChromaDB
- **Modern UI**: Beautiful, responsive web interface with real-time chat
- **Document Processing**: Automatic PDF text extraction and indexing

## 🏗️ Architecture

```
├── interface/          # Frontend (HTML/CSS/JS)
├── src/
│   ├── ai/            # AI model and OpenAI integration
│   ├── vector_db/     # ChromaDB vector database service
│   ├── app.py         # Flask backend API
│   ├── helpers.py     # Utility functions and web crawling
│   └── constants.py   # Configuration constants
├── ressources/        # Document storage directory
├── downloaded_pdfs/   # Downloaded PDF files
└── vector_database_data/  # ChromaDB persistent storage
```

## 📋 Prerequisites

- Python 3.8+
- Miniconda or Anaconda
- OpenAI API key

## 🛠️ Installation

### 1. Clone the Repository
```bash
git clone <your-repo-url>
cd chatbot
```

### 2. Create Conda Environment
```bash
conda create -n chatbot python=3.9
conda activate chatbot
```

### 3. Install Dependencies


#### Manual installation Or requirement.txt
```bash
pip install flask flask-cors openai langchain chromadb beautifulsoup4 requests selenium webdriver-manager PyPDF2
```

### 4. Set OpenAI API Key

Edit `src/ai/ai_model.py` and replace the placeholder API key:
```python
os.environ["OPENAI_API_KEY"] = "your-openai-api-key-here"
```

## 🚀 Usage

### 1. Start the Backend
```bash
cd src
python app.py
```
The Flask server will start on `http://localhost:5000`

### 2. Open the Frontend
Open `interface/main.html` in your web browser.

### 3. Import Documents
Use the API endpoint to import your documents:
```bash
curl http://localhost:5000/import_all_files_to_collection
```

### 4. Start Chatting
- The chatbot will greet you automatically
- Ask questions about your documents
- The AI will provide context-aware answers

## 🌐 API Endpoints

- `GET /import_all_files_to_collection` - Import all documents from ressources/ folder
- `POST /query_result` - Send a message and get AI response
- `POST /crawling` - Crawl a website and download PDFs

### Example API Usage
```python
import requests

# Send a message
response = requests.post('http://localhost:5000/query_result',
                        json={'prompt': 'What is the main topic?'})
print(response.json())
```

## 🔧 Configuration

Edit `src/constants.py` to configure:
- `RESSOURCES_DIR`: Document storage directory
- `COLLECTION_NAME`: Vector database collection name
- `N_RESULTS`: Number of search results to retrieve

## 🕷️ Web Crawling

The application includes a powerful web crawler that can:
- Crawl entire websites
- Download PDF files automatically
- Handle JavaScript-heavy sites using Selenium

### Usage
```python
from src.helpers import crawl_and_download_pdfs

# Crawl a website and download all PDFs
crawl_and_download_pdfs("https://example.com")
```

## 📁 Project Structure Details

### Frontend (`interface/`)
- `main.html` - Main chat interface
- `main.css` - Modern styling with gradients and animations
- `main.js` - Chat functionality and API integration

### Backend (`src/`)
- `app.py` - Flask REST API
- `ai/ai_model.py` - OpenAI integration with LangChain
- `vector_db/chroma_db_service.py` - Vector database operations
- `helpers.py` - PDF processing and web crawling utilities

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🆘 Troubleshooting

### Common Issues:

1. **OpenAI API Errors**: Check your API key and billing status
2. **CORS Issues**: Ensure Flask CORS is properly configured
3. **PDF Processing**: Make sure PyPDF2 can read your PDF files
4. **Selenium Issues**: Install ChromeDriver or use webdriver-manager

### Getting Help:
- Check the browser console for JavaScript errors
- Verify Flask server is running on port 5000
- Ensure all dependencies are installed correctly

## 🔄 Updates

To update the application:
1. Pull latest changes
2. Update dependencies: `pip install -r requirements.txt --upgrade`
3. Restart the Flask server
4. Clear browser cache if needed

---

Built with ❤️ using Flask, OpenAI, LangChain, and ChromaDB</content>
<parameter name="filePath">README.md
