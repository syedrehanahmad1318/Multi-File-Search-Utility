import os
import re
import time

def search_in_file(file_path, pattern):
    """Search for a regex pattern inside a file and return matches."""
    matches = []
    try:
        with open(file_path, 'r', encoding='utf-8', errors='ignore') as file:
            for line_number, line in enumerate(file, start=1):
                if re.search(pattern, line, re.IGNORECASE):
                    matches.append((line_number, line.strip()))
    except Exception as e:
        print(f"Error reading {file_path}: {e}")
    return matches


def search_in_directory(directory, pattern, extension=None, output_file=None):
    """Search pattern in all files within directory (recursively)."""
    results = []
    for root, _, files in os.walk(directory):
        for file in files:
            if extension and not file.endswith(extension):
                continue

            file_path = os.path.join(root, file)
            file_matches = search_in_file(file_path, pattern)

            if file_matches:
                results.append((file_path, file_matches))

    # Display results
    for file_path, matches in results:
        print(f"\nFile: {file_path}")
        for line_number, line in matches:
            print(f"  Line {line_number}: {line}")

    if not results:
        print("\n⚠️ No matches found.")

    # Optionally save to output file
    if output_file:
        with open(output_file, 'w', encoding='utf-8') as f:
            for file_path, matches in results:
                f.write(f"\nFile: {file_path}\n")
                for line_number, line in matches:
                    f.write(f"  Line {line_number}: {line}\n")
        print(f"\nResults saved to {output_file}")


if __name__ == "__main__":
    print("=== Multi-File Search Utility ===\n")
    directory = input("Enter directory path to search: ").strip()
    pattern = input("Enter search pattern (regex supported): ").strip()
    extension = input("Enter file extension (e.g. .txt) or press Enter for all: ").strip() or None
    save = input("Save results to file? (y/n): ").strip().lower()

    output_file = f"search_results_{int(time.time())}.txt" if save == 'y' else None

    search_in_directory(directory, pattern, extension, output_file)
