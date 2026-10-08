# Task: Read a text file input.txt, capitalize every word, and write the modified text to output.txt.

def process_file(input_filename, output_filename):
    try:
        # Step 1: Create a dummy input file just for the sake of this challenge to work standalone
        with open(input_filename, 'w') as dummy_file:
            dummy_file.write("hello world! this is a test file.\nlearning python is fun.")
        print(f"Created '{input_filename}' with sample text.")

        # Step 2: Read the text file
        with open(input_filename, 'r') as file_in:
            content = file_in.read()

        # Step 3: Capitalize every word (Title Case)
        # .title() method capitalizes the first letter of each word
        capitalized_content = content.title()

        # Step 4: Write the modified content to the new file
        with open(output_filename, 'w') as file_out:
            file_out.write(capitalized_content)
        
        print(f"Successfully processed and wrote to '{output_filename}'.")
        print(f"Modified Content:\n{capitalized_content}")

    except FileNotFoundError:
        print(f"Error: The file {input_filename} was not found.")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

# Calling the function to execute the task
process_file('input.txt', 'output.txt')
