from bs4 import BeautifulSoup
import sys

def add_class_to_song_divs(input_file, output_file):
    try:
        # Read the input HTML file
        with open(input_file, 'r', encoding='utf-8') as file:
            html_content = file.read()

        # Parse the HTML content
        soup = BeautifulSoup(html_content, 'html.parser')

        # Find all divs with id starting with 'song-' and add class 'sg'
        for song_div in soup.find_all('div', id=lambda x: x and x.startswith('song-')):
            song_div['class'] = song_div.get('class', []) + ['sg']

        # Write the modified HTML to the output file
        with open(output_file, 'w', encoding='utf-8') as file:
            file.write(str(soup))

        print(f"Successfully added class 'sg' to song divs. Output saved to '{output_file}'.")
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python add_class_to_song_divs.py input.html output.html")
    else:
        input_file = sys.argv[1]
        output_file = sys.argv[2]
        add_class_to_song_divs(input_file, output_file)
