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
SECRET_KEY can be generated using the following code:
```python
import secrets
print(secrets.token_hex(32))
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

You can also use command line to redact a pdf:
```bash
python main.py input.pdf output.pdf
```

## Technical Approach & Architecture

### Architecture Overview

PDF PII Redactor utilizes a modular, component-based architecture designed to provide a clean and streamlined workflow:

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

### Technical Implementation

#### PDF Processing with PyMuPDF (fitz)
It is using PyMuPDF for PDF manipulation because it provides robust text extraction, precise text search, true redaction capabilities, and excellent performance with large documents.

#### PII Detection with OpenAI API
It leverage OpenAI's API for PII detection because it provides state-of-the-art language understanding, identifies complex PII patterns, adapts to different languages, and offers high accuracy with minimal false negatives.

#### Processing Workflow
1. **Text Extraction & Language Detection**: Document text is extracted, segmented by page, and its language is detected
2. **PII Detection**: Text segments are sent to OpenAI's API with specialized prompts
3. **Redaction Application**: For each identified PII instance, the exact location is determined and redaction is applied
4. **Output Generation**: A new PDF is created with all redactions applied

#### Security Considerations
- No PII data is stored between processing steps
- Temporary files are securely deleted
- Processing is done in-memory where possible
- API communications use secure connections

### Design Decisions

We chose an LLM-based approach over traditional rule-based systems because rule-based systems require extensive maintenance, struggle with context-dependent PII, and need language-specific rules for each supported language.

The system uses a modular design and stateless processing to enhance security, maintainability, and simplify deployment.

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
