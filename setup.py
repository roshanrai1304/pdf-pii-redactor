from setuptools import setup, find_packages

setup(
    name="pdf-pii-redactor",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "PyMuPDF",
        "openai",
        "langdetect",
        "click",
        "tqdm",
        "flask",
    ],
    entry_points={
        "console_scripts": [
            "pdf-pii-redactor=pdf_pii_redactor.main:main",
            "pdf-pii-redactor-web=pdf_pii_redactor.web:run_web_app",
        ],
    },
    author="Your Name",
    author_email="your.email@example.com",
    description="A tool to automatically redact PII from PDF documents",
    keywords="pdf, pii, redaction, privacy",
    url="https://github.com/yourusername/pdf-pii-redactor",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
    ],
    python_requires=">=3.8",
) 