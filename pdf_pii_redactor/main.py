#!/usr/bin/env python3
"""
Command-line interface for the PDF PII Redactor tool.
"""

import os
import sys
import click
from tqdm import tqdm
from dotenv import load_dotenv

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from pdf_pii_redactor.redactor import PDFRedactor

load_dotenv()


@click.command()
@click.argument("input_pdf", type=click.Path(exists=True, readable=True))
@click.argument("output_pdf", type=click.Path(writable=True))
@click.option(
    "--openai-api-key", 
    envvar="OPENAI_API_KEY",
    help="OpenAI API key. If not provided, will use OPENAI_API_KEY environment variable."
)
@click.option(
    "--model", 
    default="gpt-4o",
    help="OpenAI model to use for PII detection. Default: gpt-4o"
)
@click.option(
    "--verbose", 
    is_flag=True, 
    help="Enable verbose output"
)
def main(input_pdf, output_pdf, openai_api_key, model, verbose):
    """
    Redact PII from a PDF document.
    
    INPUT_PDF: Path to the input PDF file.
    OUTPUT_PDF: Path where the redacted PDF will be saved.
    """
    if not openai_api_key and "OPENAI_API_KEY" not in os.environ:
        click.echo("Error: OpenAI API key not provided. Please provide it via --openai-api-key option or set the OPENAI_API_KEY environment variable.", err=True)
        sys.exit(1)
    
    click.echo(f"Processing {input_pdf}...")
    
    try:
        redactor = PDFRedactor(openai_api_key=openai_api_key, model=model, verbose=verbose)
        redactor.redact_pdf(input_pdf, output_pdf)
        click.echo(f"Successfully redacted PII. Redacted PDF saved to {output_pdf}")
    except Exception as e:
        click.echo(f"Error: {str(e)}", err=True)
        sys.exit(1)


if __name__ == "__main__":
    main() 