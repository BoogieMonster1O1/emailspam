import csv
from pypdf import PdfReader

# Function to parse a single line into a dictionary
def parse_line(line):
    # Tokenize the line by spaces
    tokens = line.split()
    
    if len(tokens) < 5:  # Ensure there are enough tokens
        return None

    # Check if the first word is a number (assuming USN should follow)
    if not tokens[0].isdigit():
        return None

    # Extract required fields based on the token positions
    department = tokens[1]  # Department is the second word
    usn = tokens[2]         # USN is the third word
    email = tokens[-1]      # Email is the last word
    phone = tokens[-2]      # Phone is the second last word
    name = " ".join(tokens[3:-2])  # Name is between the 4th word and 3rd last word

    # Return the parsed data as a dictionary
    return {
        "Department": department,
        "USN": usn,
        "Name": name,
        "Phone": phone,
        "Email": email
    }

# Function to read PDF and extract lines
def read_pdf(file_path):
    reader = PdfReader(file_path)
    lines = []

    # Iterate through all the pages
    for page in reader.pages:
        text = page.extract_text()
        if text:  # Ensure there's text to process
            # Split the text into lines
            page_lines = text.split('\n')
            lines.extend(page_lines)
    
    return lines

# Function to filter and parse lines
def process_lines(lines):
    parsed_data = []

    for line in lines:
        # Parse each line into an object, ignoring lines where parsing fails
        parsed_line = parse_line(line)
        if parsed_line:
            parsed_data.append(parsed_line)
    
    return parsed_data

# Function to write parsed data to a CSV file
def write_to_csv(parsed_data, output_file):
    # Define CSV column headers
    headers = ["Department", "USN", "Name", "Phone", "Email"]

    # Write data to CSV
    with open(output_file, mode='w', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=headers)
        writer.writeheader()  # Write the header
        for data in parsed_data:
            writer.writerow(data)

# Main function to orchestrate the PDF reading and CSV writing
def main():
    pdf_file = "input.pdf"  # Path to your input PDF file
    output_csv = "output.csv"  # Output CSV file name

    # Step 1: Read the PDF and extract lines
    lines = read_pdf(pdf_file)

    # Step 2: Process the lines and extract relevant data
    parsed_data = process_lines(lines)

    # Step 3: Write the parsed data into a CSV file
    write_to_csv(parsed_data, output_csv)

    print(f"Data successfully written to {output_csv}")

if __name__ == '__main__':
    main()
