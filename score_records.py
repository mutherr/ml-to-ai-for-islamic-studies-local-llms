"""
This script outputs a JSON file with an object for its root rather than an array.
This is to ensure that the output file can be easily updated with new reports without losing existing data when using the --resume flag.
After running the script, use `llm_scripts/restructure_reports.py` to convert the output file into an array.
"""

import json
import argparse
from pathlib import Path

import llm

from prompts import prompts


def parse_arguments():
    """Parse and validate command line arguments."""
    parser = argparse.ArgumentParser(description="Score text reports using LLM prompts")
    parser.add_argument("input", help="Input filename containing reports (JSON format)")
    parser.add_argument(
        "prompt", help="Key for the prompt to use from the prompts dictionary"
    )
    parser.add_argument("--output", required=True, help="Output filename (required)")
    parser.add_argument(
        "--limit",
        type=int,
        default=50,
        help="Number of reports to process (default: 50)",
    )
    parser.add_argument(
        "--resume",
        action="store_true",
        help="Resume processing by skipping existing records in output file",
    )

    args = parser.parse_args()

    if args.prompt not in prompts:
        print(
            f"Error: '{args.prompt}' not found in ./llm_scripts/prompts.py. Available prompts: {list(prompts.keys())}"
        )
        return None

    output_filename = args.output

    return args, output_filename


def load_existing_scores(output_filename):
    """Load existing scores from output file if it exists."""
    if Path(output_filename).exists():
        try:
            with open(output_filename, "r") as file:
                return json.load(file)
        except (json.JSONDecodeError, IOError) as e:
            print(
                f"Warning: Could not load existing scores from '{output_filename}': {e}"
            )
            return {}
    return {}


def generate_response(model, text, prompt_key):
    """Generate a response from the LLM model based on the provided text and prompt."""
    for i in range(3):
        response = model.prompt(
            temperature=0.1,
            seed=42,
            system="You respond with only a single word per response. Do not include any additional text or explanations. Do not include a summary or use examples. Respond to the prompt with one word.",
            prompt=f"""
                BEGIN REPORT
                {text}
                END REPORT
                \n\n
                {prompts[prompt_key]["prompt"]}
            """,
        )
        response = response.text().strip().lower()
        if (
            isinstance(prompts[prompt_key]["valid_responses"], int)
            and len(response.split()) == prompts[prompt_key]["valid_responses"]
        ):
            return response
        elif response in prompts[prompt_key]["valid_responses"]:
            return response
        else:
            print(f"Invalid response {response} for report. Retrying ({i + 1})...")


def process_reports(
    reports, model: llm.Model, prompt_key, limit, output_filename, resume=False
):
    """Process reports using the LLM model and return scores."""
    total_reports = len(reports)

    # Load existing scores if resuming
    if resume:
        scores = load_existing_scores(output_filename)
        print(f"Loaded {len(scores)} existing scores from '{output_filename}'")
    else:
        scores = {}

    processed_count = 0

    for i, report in enumerate(reports, start=1):
        report_id = report["id"]

        # Skip if already processed and resuming
        if resume and report_id in scores:
            continue

        # Check limit against newly processed reports
        if processed_count >= limit:
            break

        print(
            f"Processing {report_id} ({i} of {total_reports}, {processed_count + 1} new)"
        )
        text = report.get("text", "")
        if not text.strip():
            print("Skipping empty text report.")
            continue

        response = generate_response(model, text, prompt_key)

        report[prompt_key] = response
        scores[report_id] = report

        # Save immediately after each successful processing
        save_scores(scores, output_filename)

        processed_count += 1

    return scores


def save_scores(scores, output_filename):
    """Save scores to a JSON file."""
    with open(output_filename, "w") as file:
        json.dump(scores, file, indent=4)


def main():
    # Parse and validate arguments
    result = parse_arguments()
    if result is None:
        return

    args, output_filename = result

    with open(args.input, "r") as file:
        reports = json.load(file)

    model = llm.get_model("gemma3:4b")

    # Ensure output directory exists
    Path(output_filename).parent.mkdir(parents=True, exist_ok=True)

    scores = process_reports(
        reports, model, args.prompt, args.limit, output_filename, args.resume
    )

    print(
        f"Processing complete. Final results saved to '{output_filename}' with {len(scores)} total scores."
    )


if __name__ == "__main__":
    main()
