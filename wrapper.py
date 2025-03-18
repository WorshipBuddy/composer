from bs4 import BeautifulSoup
import re

# Load the HTML file
input_file = "au-songbook.html"  # Corrected input filename
output_file = "au.html"  # Corrected output filename

with open(input_file, "r", encoding="utf-8") as file:
    soup = BeautifulSoup(file, "html.parser")

# Regular expression to find song numbers at the beginning of a line
song_number_pattern = re.compile(r"^(\d+)\.")  # Matches "1.", "2.", etc.

songs = []
current_song = []
current_number = None

# Iterate through all paragraphs and divs in the document
for p in soup.find_all(["p", "div"]):
    text = p.get_text(strip=True)
    
    match = song_number_pattern.match(text)
    if match:  # Found a song number
        if current_song:  
            # Save the previous song
            songs.append((current_number, current_song))
        
        current_number = match.group(1)  # Extract song number
        current_song = [p]  # Start a new song group
    else:
        if current_number is not None:
            current_song.append(p)

# Save the last song
if current_song:
    songs.append((current_number, current_song))

# Wrap songs in divs
for number, song_content in songs:
    wrapper = soup.new_tag("div", **{"class": "sg", "id": f"song-{number}"})

    for element in song_content:
        element.extract()  # Remove from original placement
        wrapper.append(element)

    # Insert the new wrapper at the correct position
    soup.body.append(wrapper)  # Adds it to the body at the end

# Save the modified HTML
with open(output_file, "w", encoding="utf-8") as file:
    file.write(str(soup.prettify()))

print(f"Processed HTML saved to {output_file}")