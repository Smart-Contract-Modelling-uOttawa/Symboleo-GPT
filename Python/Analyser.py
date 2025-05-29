import os
import csv
from collections import defaultdict
import statistics

# Define paths
error_file_path = os.path.expanduser("/Users/gurdarshansingh/Desktop/runtime-EclipseApplication/errors.txt")
csv_output_directory = os.path.expanduser("/Users/gurdarshansingh/Desktop/runtime-EclipseApplication/Error_Reports/")
os.makedirs(csv_output_directory, exist_ok=True)

# Get list of all .symboleo files in the directory (assuming this is where your contracts are)
contracts_directory = os.path.expanduser("/Users/gurdarshansingh/Desktop/runtime-EclipseApplication/meatsale/")
all_files = [f for f in os.listdir(contracts_directory) if f.endswith('.symboleo')]

# Data structures
error_data = defaultdict(lambda: defaultdict(lambda: defaultdict(int)))
all_file_stats = {filename: 0 for filename in all_files}  # Initialize all files with 0 errors

# Error categorization function (from old code)
def categorize_error(error_message):
    """Categorize errors based on predefined patterns in error messages."""
    syntactic_keywords = ["unexpected token", "missing", "syntax error", "mismatched input", "no viable alternative", "expecting", ":", ";", "EOF"]
    type_keywords = ["type mismatch", "expected type", "found", "incompatible types", "is not type of", "only variable of type"]
    semantic_keywords = ["undeclared", "undefined", "not defined", "couldn't resolve reference", "attribute", "variable"]
    logic_keywords = ["invalid temporal", "temporal operator misused", "conflicting timing", "conflict"]
    unreachable_keywords = ["not reachable", "never activated"]

    error_lower = error_message.lower()
    if "type" in error_lower:
        return "Type Error"
    
    if any(keyword.lower() in error_lower for keyword in syntactic_keywords):
        return "Syntax Error"
    elif any(keyword.lower() in error_lower for keyword in type_keywords):
        return "Type Error"
    elif any(keyword.lower() in error_lower for keyword in semantic_keywords):
        return "Semantic Error"
    elif any(keyword.lower() in error_lower for keyword in logic_keywords):
        return "Logic Error"
    elif any(keyword.lower() in error_lower for keyword in unreachable_keywords):
        return "Missing or Unreachable Elements"
    else:
        return "Uncategorized Error"

try:
    # Process error file
    with open(error_file_path, "r") as file:
        for line in file:
            if line.startswith("File: "):
                parts = line.split(", ")
                if len(parts) >= 3:
                    filename = parts[0].replace("File: ", "").strip()
                    line_number = parts[1].replace("Line: ", "").strip()
                    error_message = parts[2].replace("Message: ", "").strip()
                    
                    if line_number.isdigit():
                        line_number = int(line_number)
                    else:
                        line_number = "Unknown"

                    # Categorize the error (using the categorize_error function)
                    error_category = categorize_error(error_message)

                    # Increment count for this file, line, and error message
                    error_data[filename][line_number][(error_message, error_category)] += 1
                    all_file_stats[filename] = sum(sum(count for count in messages.values()) 
                                                 for messages in error_data[filename].values())

    # Prepare summary stats (now includes all files)
    summary_stats = [(filename, all_file_stats[filename]) for filename in all_files]

    # Calculate statistics
    error_counts = [count for _, count in summary_stats]
    average_errors = statistics.mean(error_counts)
    stdev_errors = statistics.stdev(error_counts) if len(error_counts) > 1 else 0
    min_errors = min(error_counts)
    max_errors = max(error_counts)

    # Write summary report
    summary_file_path = os.path.join(csv_output_directory, "summary_report.csv")
    with open(summary_file_path, "w", newline="") as summary_file:
        writer = csv.writer(summary_file)
        writer.writerow(["Filename", "Total Errors"])
        for filename, total in summary_stats:
            writer.writerow([filename, total])

        writer.writerow([])
        writer.writerow(["Overall Statistics (Including Zero-Error Files)"])
        writer.writerow(["Total Files Analyzed", len(all_files)])
        writer.writerow(["Files with Errors", sum(1 for _, count in summary_stats if count > 0)])
        writer.writerow(["Files without Errors", sum(1 for _, count in summary_stats if count == 0)])
        writer.writerow(["Average Errors", average_errors])
        writer.writerow(["Standard Deviation", stdev_errors])
        writer.writerow(["Minimum Errors", min_errors])
        writer.writerow(["Maximum Errors", max_errors])

    print(f"Summary report saved at: {summary_file_path}")

    # Create detailed reports only for files with errors
    for filename, lines in error_data.items():
        file_path = os.path.join(csv_output_directory, f"{filename}_error_stats.csv")
        with open(file_path, "w", newline="") as csvfile:
            csv_writer = csv.writer(csvfile)
            total_errors = all_file_stats[filename]
            csv_writer.writerow(["Total Errors", total_errors])
            csv_writer.writerow(["Filename", "Line Number", "Error Message", "Error Category", "Error Count"])
            
            for line_num, messages in lines.items():
                for (message, category), count in messages.items():
                    csv_writer.writerow([filename, line_num, message, category, count])

        print(f"Error details for {filename} saved at: {file_path}")

except FileNotFoundError:
    print(f"Error: The file {error_file_path} was not found.")
except Exception as e:
    print(f"An error occurred: {e}")

# import os
# import csv
# from collections import defaultdict
# import statistics

# # Define paths
# error_file_path = os.path.expanduser("/Users/gurdarshansingh/Desktop/runtime-EclipseApplication/errors.txt")
# csv_output_directory = os.path.expanduser("/Users/gurdarshansingh/Desktop/runtime-EclipseApplication/Error_Reports/")
# os.makedirs(csv_output_directory, exist_ok=True)

# # Get list of all .symboleo files in the directory (assuming this is where your contracts are)
# contracts_directory = os.path.expanduser("/Users/gurdarshansingh/Desktop/runtime-EclipseApplication/meatsale/")
# all_files = [f for f in os.listdir(contracts_directory) if f.endswith('.symboleo')]

# # Data structures
# error_data = defaultdict(lambda: defaultdict(lambda: defaultdict(int)))
# all_file_stats = {filename: 0 for filename in all_files}  # Initialize all files with 0 errors

# def categorize_error(error_message):
#     """Categorize errors (keep your existing implementation)"""
#     # ... (your existing categorize_error function) ...

# try:
#     # Process error file
#     with open(error_file_path, "r") as file:
#         for line in file:
#             if line.startswith("File: "):
#                 parts = line.split(", ")
#                 if len(parts) >= 3:
#                     filename = parts[0].replace("File: ", "").strip()
#                     line_number = parts[1].replace("Line: ", "").strip()
#                     error_message = parts[2].replace("Message: ", "").strip()
                    
#                     if line_number.isdigit():
#                         line_number = int(line_number)
#                     else:
#                         line_number = "Unknown"

#                     error_category = categorize_error(error_message)
#                     error_data[filename][line_number][(error_message, error_category)] += 1
#                     all_file_stats[filename] = sum(sum(count for count in messages.values()) 
#                                                  for messages in error_data[filename].values())

#     # Prepare summary stats (now includes all files)
#     summary_stats = [(filename, all_file_stats[filename]) for filename in all_files]

#     # Calculate statistics
#     error_counts = [count for _, count in summary_stats]
#     average_errors = statistics.mean(error_counts)
#     stdev_errors = statistics.stdev(error_counts) if len(error_counts) > 1 else 0
#     min_errors = min(error_counts)
#     max_errors = max(error_counts)

#     # Write summary report
#     summary_file_path = os.path.join(csv_output_directory, "summary_report.csv")
#     with open(summary_file_path, "w", newline="") as summary_file:
#         writer = csv.writer(summary_file)
#         writer.writerow(["Filename", "Total Errors"])
#         for filename, total in summary_stats:
#             writer.writerow([filename, total])

#         writer.writerow([])
#         writer.writerow(["Overall Statistics (Including Zero-Error Files)"])
#         writer.writerow(["Total Files Analyzed", len(all_files)])
#         writer.writerow(["Files with Errors", sum(1 for _, count in summary_stats if count > 0)])
#         writer.writerow(["Files without Errors", sum(1 for _, count in summary_stats if count == 0)])
#         writer.writerow(["Average Errors", average_errors])
#         writer.writerow(["Standard Deviation", stdev_errors])
#         writer.writerow(["Minimum Errors", min_errors])
#         writer.writerow(["Maximum Errors", max_errors])

#     print(f"Summary report saved at: {summary_file_path}")

#     # Create detailed reports only for files with errors
#     for filename, lines in error_data.items():
#         file_path = os.path.join(csv_output_directory, f"{filename}_error_stats.csv")
#         with open(file_path, "w", newline="") as csvfile:
#             csv_writer = csv.writer(csvfile)
#             total_errors = all_file_stats[filename]
#             csv_writer.writerow(["Total Errors", total_errors])
#             csv_writer.writerow(["Filename", "Line Number", "Error Message", "Error Category", "Error Count"])
            
#             for line_num, messages in lines.items():
#                 for (message, category), count in messages.items():
#                     csv_writer.writerow([filename, line_num, message, category, count])

#         print(f"Error details for {filename} saved at: {file_path}")

# except FileNotFoundError:
#     print(f"Error: The file {error_file_path} was not found.")
# except Exception as e:
#     print(f"An error occurred: {e}")

# import os
# import csv
# from collections import defaultdict
# import statistics

# # Define the path to the errors.txt file on the desktop
# error_file_path = os.path.expanduser("/Users/gurdarshansingh/Desktop/runtime-EclipseApplication/errors.txt")

# # Define the directory to save the CSV files (change this to your desired location)
# csv_output_directory = os.path.expanduser("/Users/gurdarshansingh/Desktop/runtime-EclipseApplication/Error_Reports/")

# # Create the directory if it doesn't exist
# os.makedirs(csv_output_directory, exist_ok=True)

# # Dictionary to store error counts per file, line numbers, and descriptions
# error_data = defaultdict(lambda: defaultdict(lambda: defaultdict(int)))  # {filename: {line_number: {error_message: count}}}

# def extract_sections(file_path):
#     """Return a dict with section name and corresponding line number ranges."""
#     section_lines = {}
#     current_section = None
#     start_line = 0

#     with open(file_path, "r") as f:
#         lines = f.readlines()

#     for idx, line in enumerate(lines, start=1):
#         line_lower = line.strip().lower()
#         if line_lower.startswith("domain "):
#             if current_section:
#                 section_lines[current_section] = (start_line, idx - 1)
#             current_section = "Domain"
#             start_line = idx
#         elif line_lower.startswith("contract "):
#             if current_section:
#                 section_lines[current_section] = (start_line, idx - 1)
#             current_section = "Contract"
#             start_line = idx
#         elif line_lower.startswith("declarations"):
#             if current_section:
#                 section_lines[current_section] = (start_line, idx - 1)
#             current_section = "Declarations"
#             start_line = idx
#         elif line_lower.startswith("obligations"):
#             if current_section:
#                 section_lines[current_section] = (start_line, idx - 1)
#             current_section = "Obligations"
#             start_line = idx
#         elif line_lower.startswith("powers"):
#             if current_section:
#                 section_lines[current_section] = (start_line, idx - 1)
#             current_section = "Powers"
#             start_line = idx
#         elif line_lower.startswith("endcontract") or line_lower.startswith("enddomain"):
#             if current_section:
#                 section_lines[current_section] = (start_line, idx)

#     return section_lines

# # Error categorization function
# def categorize_error(error_message):
#     """Categorize errors based on predefined patterns in error messages."""
#     syntactic_keywords = ["unexpected token", "missing", "syntax error", "mismatched input", "no viable alternative", "expecting", ":", ";", "EOF"]
#     type_keywords = ["type mismatch", "expected type", "found", "incompatible types", "is not type of", "only variable of type"]
#     semantic_keywords = ["undeclared", "undefined", "not defined", "couldn't resolve reference", "attribute", "variable"]
#     logic_keywords = ["invalid temporal", "temporal operator misused", "conflicting timing", "conflict"]
#     unreachable_keywords = ["not reachable", "never activated"]

#     error_lower = error_message.lower()
#     if "type" in error_lower:
#         return "Type Error"
    
#     if any(keyword.lower() in error_lower for keyword in syntactic_keywords):
#         return "Syntax Error"
#     elif any(keyword.lower() in error_lower for keyword in type_keywords):
#         return "Type Error"
#     elif any(keyword.lower() in error_lower for keyword in semantic_keywords):
#         return "Semantic Error"
#     elif any(keyword.lower() in error_lower for keyword in logic_keywords):
#         return "Logic Error"
#     elif any(keyword.lower() in error_lower for keyword in unreachable_keywords):
#         return "Missing or Unreachable Elements"
#     else:
#         return "Uncategorized Error"

# try:
#     # Open and read the error file
#     with open(error_file_path, "r") as file:
#         for line in file:
#             if line.startswith("File: "):
#                 # Extract filename, line number, and message from the format:
#                 # "File: <filename>, Line: <num>, Message: <message>"
#                 parts = line.split(", ")
#                 if len(parts) >= 3:
#                     filename = parts[0].replace("File: ", "").strip()
#                     line_number = parts[1].replace("Line: ", "").strip()
#                     error_message = parts[2].replace("Message: ", "").strip()
                    
#                     # Ensure line_number is valid
#                     if line_number.isdigit():
#                         line_number = int(line_number)
#                     else:
#                         line_number = "Unknown"

#                     # Categorize the error
#                     error_category = categorize_error(error_message)

#                     # Increment count for this file, line, and error message
#                     error_data[filename][line_number][(error_message, error_category)] += 1
#     # Get section line ranges
#     # For storing overall summary
#     summary_stats = []

#     # Iterate through files to populate summary_stats
#     for filename, lines in error_data.items():
#         total_errors = sum(sum(count for count in messages.values()) for messages in lines.values())
#         summary_stats.append((filename, total_errors))

#     # Extract just the error counts for stats
#     error_counts = [count for _, count in summary_stats]

#     # Calculate overall stats
#     average_errors = statistics.mean(error_counts) if error_counts else 0
#     stdev_errors = statistics.stdev(error_counts) if len(error_counts) > 1 else 0
#     min_errors = min(error_counts) if error_counts else 0
#     max_errors = max(error_counts) if error_counts else 0

#     # Write the summary report CSV
#     summary_file_path = os.path.join(csv_output_directory, "summary_report.csv")
#     with open(summary_file_path, "w", newline="") as summary_file:
#         writer = csv.writer(summary_file)
#         writer.writerow(["Filename", "Total Errors"])
#         for filename, total in summary_stats:
#             writer.writerow([filename, total])

#         writer.writerow([])  # Empty row
#         writer.writerow(["Overall Statistics"])
#         writer.writerow(["Average Errors", average_errors])
#         writer.writerow(["Standard Deviation", stdev_errors])
#         writer.writerow(["Minimum Errors", min_errors])
#         writer.writerow(["Maximum Errors", max_errors])

#     print(f"Summary report saved successfully at: {summary_file_path}")
#     # Create separate CSV file for each file in the error_data dictionary
#     for filename, lines in error_data.items():
#         file_path = os.path.join(csv_output_directory, f"{filename}_error_stats.csv")
        
#         # Open the CSV file for writing
#         with open(file_path, "w", newline="") as csvfile:
#             csv_writer = csv.writer(csvfile)
            
#             # Calculate total errors for the current file
#             total_errors = sum(sum(count for count in messages.values()) for messages in lines.values())
            
#             # Write total errors as the first row
#             csv_writer.writerow(["Total Errors", total_errors])
            
#             # Write the headers for the error details
#             csv_writer.writerow(["Filename", "Line Number", "Error Message", "Error Category", "Error Count"])
            
#             # Write each error's details
#             for line_num, messages in lines.items():
#                 for (message, category), count in messages.items():
#                     csv_writer.writerow([filename, line_num, message, category, count])

#         print(f"Error statistics for {filename} saved successfully at: {file_path}")

# except FileNotFoundError:
#     print(f"Error: The file {error_file_path} was not found.")
# except Exception as e:
#     print(f"An error occurred: {e}")