# 📝 Summarize Transcript

This Python tool generates a concise summary from a text transcript file. It supports transcripts in plain text (.txt) format or JSON format (specifically, the output from OpenAI Whisper).

### 🔧 Features
- Summarizes long texts into a shorter, coherent summary.
- Uses pre-trained summarization models from Hugging Face Transformers (e.g., BART, T5).
- Supports input from `.txt` files or Whisper-generated `.json` files.
- Allows customization of summary length (min/max tokens).
- Option to specify which summarization model to use.

### 🏁 Quickstart
```bash
# Install dependencies
pip install -r requirements.txt

# Summarize a plain text transcript
python summarize_script.py --input_file examples/sample_transcript.txt --output_file summary_plain.txt

# Summarize a Whisper JSON transcript
python summarize_script.py --input_file examples/sample_transcript.json --output_file summary_whisper.txt --model_name t5-small

# Specify summary length constraints
python summarize_script.py --input_file examples/sample_transcript.txt --output_file custom_summary.txt --min_length 30 --max_length 150
```

### ⚙️ How it Works
1.  **Load Transcript**: The script loads the input transcript. If it's a JSON file from Whisper, it extracts the full transcribed text. If it's a `.txt` file, it reads the content directly.
2.  **Load Model**: A pre-trained summarization model (e.g., `facebook/bart-large-cnn` by default, or another specified by the user) is loaded from the Hugging Face Transformers library.
3.  **Summarization**: The transcript text is fed into the model, which generates a summary.
4.  **Output**: The generated summary is saved to the specified output text file.

### 📂 Input Files
-   **`.txt`**: A plain text file containing the transcript.
-   **`.json`**: A JSON file in the format output by OpenAI Whisper (must contain a `"text"` field with the full transcript or `"segments"` array).

### 📄 Output File
A plain text file containing the generated summary. 