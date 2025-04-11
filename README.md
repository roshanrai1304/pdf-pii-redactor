# PDF PII Redactor

A Python tool to automatically identify and redact personally identifiable information (PII) from PDF documents using OpenAI's API.

## Features

- Accepts PDF documents containing selectable text as input
- Automatically detects the document's language
- Identifies various types of PII:
  - Names
  - Email addresses
  - Phone numbers
  - Addresses
  - Credit card numbers
  - Dates of birth
- Applies redactions to the identified PII
- Outputs a redacted version of the document
- Supports multiple languages
- Provides both command-line and web interfaces

## Installation

 Clone the repository:
   ```bash
   git clone https://github.com/yourusername/pdf-pii-redactor.git
   cd pdf-pii-redactor
   ```

Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

Set your OpenAI API key (For Linux/Mac)
```bash
export OPENAI_API_KEY=your_api_key_here
```

Set your OpenAI API key (For Windows)
```bash
set OPENAI_API_KEY=your_api_key_here
```

or create a .env file and add the following:
```
OPENAI_API_KEY=your_api_key_here
SECRET_KEY=your_secret_key_here ## This is used for flask
```

Start the web server
```bash
python web.py
```

Access the web interface at http://localhost:5000

### Python API
```python
from pdf_pii_redactor.redactor import PDFRedactor
# Initialize the redactor
redactor = PDFRedactor(openai_api_key="your_api_key_here")
# Redact a PDF
stats = redactor.redact_pdf("input.pdf", "output.pdf")
# Print statistics
print(f"Redacted {stats['redacted_items']} PII instances across {stats['pages_processed']} pages")
```

### Example Redaction

<table>
  <tr>
    <th>Original Document</th>
    <th>Redacted Document</th>
  </tr>
  <tr>
    <td><img src="https://github.com/roshanrai1304/pdf-pii-redactor/blob/main/sample_images/test.png" alt="Original Document" width="100%"></td>
    <td><img src="https://github.com/roshanrai1304/pdf-pii-redactor/blob/main/sample_images/output.png" alt="Redacted Document" width="100%"></td>
  </tr>
</table>

## How It Works

1. **Text Extraction**: The tool extracts text content from the PDF document.
2. **Language Detection**: It automatically detects the language of the document.
3. **PII Detection**: Using OpenAI's API, the tool identifies various types of PII in the text.
4. **Redaction**: The identified PII is completely removed from the PDF content, not just visually obscured.
5. **Output**: A new PDF file is created with all PII redacted.

## Technical Approach & Architecture

### Architecture Overview

PDF PII Redactor is built with a modular, component-based architecture that separates concerns and provides a clean workflow:

<div align="center">
  <img src="https://github.com/roshanrai1304/pdf-pii-redactor/blob/main/sample_images/architecture.png" alt="PDF PII Redactor Architecture" width="80%" style="border-radius: 8px; box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);">
</div>

### Core Components

1. **PDFRedactor**: The main orchestrator class that coordinates the entire redaction process.
   - Manages workflow between components
   - Handles input/output operations
   - Provides statistics on redaction results

2. **PDFProcessor**: Responsible for all PDF manipulation operations.
   - Extracts text from PDF documents
   - Locates text instances within the PDF
   - Applies redactions to create sanitized output

3. **PIIDetector**: Identifies PII in text using OpenAI's API.
   - Constructs prompts for the LLM
   - Processes API responses
   - Maps detected PII to original document positions

4. **LanguageDetector**: Determines the document's language.
   - Analyzes text samples from the document
   - Identifies the primary language
   - Helps optimize PII detection for specific languages

### Technical Choices

#### PDF Processing with PyMuPDF (fitz)
We chose PyMuPDF for PDF manipulation because it provides:
- Robust text extraction capabilities
- Precise text search and location functionality
- True redaction capabilities (not just visual masking)
- Excellent performance with large documents
- Active maintenance and good documentation

#### PII Detection with OpenAI API
We leverage OpenAI's API for PII detection because:
- It provides state-of-the-art natural language understanding
- Can identify complex PII patterns that rule-based systems might miss
- Adapts to different languages and contexts
- Can be prompted to identify specific types of PII
- Offers high accuracy with minimal false negatives

#### Language Detection
The system uses langdetect to:
- Automatically identify document language
- Support multilingual documents
- Optimize PII detection prompts for specific languages

#### Web Interface
The web interface is built with Flask, providing:
- Simple file upload and processing
- Model selection options
- Secure file handling
- Download of redacted documents

### Implementation Details

#### PII Detection Process
1. Document text is extracted and segmented by page
2. The language of the document is detected
3. Text segments are sent to OpenAI's API with a specialized prompt
4. The API returns structured data identifying PII instances
5. Results are processed to map PII to exact positions in the PDF

#### Redaction Workflow
1. For each identified PII instance:
   - The exact location in the PDF is determined
   - A redaction annotation is applied
   - The text is permanently removed (not just visually masked)
2. A new PDF is created with all redactions applied
3. Statistics are collected on the redaction process

#### Security Considerations
- No PII data is stored between processing steps
- Temporary files are securely deleted
- Processing is done in-memory where possible
- API communications use secure connections

### Design Decisions

#### LLM-Based vs. Rule-Based Detection
We chose an LLM-based approach over traditional rule-based systems because:
- Rule-based systems require extensive maintenance of regex patterns
- They struggle with context-dependent PII
- They need language-specific rules for each supported language
- LLMs understand context and nuance in ways rule-based systems cannot

#### Modular Architecture
The system uses a modular design to:
- Separate concerns for better maintainability
- Allow for easy testing of individual components
- Enable future extensions and improvements
- Provide clear interfaces between components

#### Stateless Processing
Each document is processed independently:
- No PII data is stored between requests
- Temporary files are securely deleted
- This enhances security and simplifies deployment

### Future Enhancements

- **OCR Integration**: Add support for scanned documents
- **Local Models**: Option to use local LLMs for offline processing
- **Custom PII Types**: Allow users to define additional PII categories
- **Batch Processing**: Improve handling of large document sets
- **Confidence Scores**: Provide confidence levels for detected PII
- **Redaction Verification**: Add post-processing verification
- **Performance Optimization**: Reduce API calls through smarter text chunking

## Requirements

- Python 3.10 or higher
- PyMuPDF (fitz)
- OpenAI API key
- Other dependencies listed in requirements.txt

## Limitations

- Only works with PDFs containing selectable text (not scanned image PDFs)
- Accuracy depends on the quality of the OpenAI model used
- May not detect PII in complex layouts or unusual formats
- Processing large documents may take time and consume API tokens

## Author

- [Roshan Rai](https://github.com/roshanrai1304)

## License

[MIT License](LICENSE)