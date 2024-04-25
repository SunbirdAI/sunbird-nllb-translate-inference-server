import os
import sys
import argparse
import pandas as pd

current_directory = os.path.dirname(os.path.realpath(__file__))
sys.path.append(current_directory)

from ai_tasks import AITasks


def process_directory(directory, output_file, base_url, auth_token):
    """
    Transcribes and translates audio files in the provided directory and its subdirectories.

    Parameters:
        directory (str): Path to the directory containing language subdirectories.
        output_file (str): Path to the output CSV file.
        base_url (str): Base URL of the API.
        auth_token (str): Authentication token for accessing the API.
    """
    # Initialize AITasks object
    ai_tasks = AITasks(base_url=base_url, auth_token=auth_token)

    # Initialize empty DataFrame to store results
    df = pd.DataFrame(columns=["filename", "language", "transcription", "translation"])

    # Traverse the directory and its subdirectories
    for root, dirs, files in os.walk(directory):
        for file in files:
            # Extract language from directory name
            language = os.path.basename(root)
            # Transcribe audio file
            transcription = ai_tasks.transcribe(
                endpoint="stt", audio_path=os.path.join(root, file), language=language
            )

            # Translate transcription to English
            translation = ai_tasks.translate(
                endpoint="nllb_translate",
                source_language=language,
                target_language="eng",
                text=transcription,
            )
            # Add results to DataFrame
            df = df._append(
                pd.DataFrame.from_dict(
                    {
                        "filename": [file],
                        "language": [language],
                        "transcription": [transcription],
                        "translation": [translation],
                    }
                ),
                ignore_index=True,
            )

    # Export DataFrame to CSV
    df.to_csv(output_file, index=False)
    print(f"Results saved to '{output_file}'")


def main():
    parser = argparse.ArgumentParser(
        description="Transcribe and translate audio files in a directory."
    )
    parser.add_argument(
        "directory", help="Path to the directory containing language subdirectories."
    )
    parser.add_argument("output_file", help="Path to the output CSV file.")
    parser.add_argument(
        "--base_url",
        default="https://sunbird-ai-api-5bq6okiwgq-ew.a.run.app/tasks",
        help="Base URL of the API.",
    )
    parser.add_argument(
        "--auth_token",
        required=True,
        help="Authentication token for accessing the API.",
    )
    args = parser.parse_args()

    process_directory(args.directory, args.output_file, args.base_url, args.auth_token)


if __name__ == "__main__":
    main()
