from bs4 import BeautifulSoup
import re

# Load the HTML file
input_file = "au-songbook.html"  # The full songbook
output_file = "au.html"  # The new extracted file

# List of song numbers to extract
target_songs = {
    17, 32, 59, 63, 76, 77, 81, 85, 89, 97, 100, 105, 107, 129, 132, 137, 141, 147, 151,
    219, 220, 291, 380, 407, 439, 446, 456, 468, 485, 486, 505, 544, 565, 576, 638, 643, 
    657, 765, 780, 814, 938, 939, 940, 948, 952, 953, 954, 955, 956, 957, 958, 959, 960, 
    962, 964, 968, 969, 971, 972, 973, 974, 976, 977, 978, 983, 984, 985, 988, 989, 991, 
    992, 994, 995, 996, 998, 999, 1000, 1005, 1008, 1010, 1012, 1013, 1016, 1020, 1022, 
    1026, 1029, 1030, 1031, 1032, 1036, 1042, 1043, 1045, 1046, 1047, 1048, 1050, 1051, 
    1054, 1055, 1058, 1060, 1062, 1063, 1065, 1067, 1068, 1075, 1076, 1077, 1078, 1079, 
    1080, 1081, 1082, 1085, 1086, 1087, 1088, 1093, 1095, 1096, 1097, 1101, 1102, 1104, 
    1105, 1106, 1107, 1108, 1109, 1110, 1111, 1112, 1113, 1114, 1115, 1118
}

with open(input_file, "r", encoding="utf-8") as file:
    soup = BeautifulSoup(file, "html.parser")

# Regular expression to find song numbers followed by an underlined title
song_number_pattern = re.compile(r"^(\d+)\.\s*")  # Matches "623. " etc.

songs = []
current_song = []
current_number = None

# Iterate through all paragraphs in the document
for p in soup.find_all("p"):
    text = p.get_text()  # ✅ DO NOT strip spaces, keep all `&nbsp;`
    
    # Check if the paragraph contains a song number
    match = song_number_pattern.match(text)
    
    # Verify that the number is followed by an underlined title
    if match and p.find("u"):  # Ensures the song number has an underlined title
        song_num = int(match.group(1))  # Extract song number
        
        if song_num in target_songs:  # If this song is in the target list
            if current_song:
                songs.append((current_number, current_song))  # Save previous song
            
            current_number = song_num
            current_song = [p]  # Start a new song group
        else:
            current_number = None  # Reset if the song is not in the list
    else:
        if current_number is not None:
            current_song.append(p)

# Save the last song
if current_song:
    songs.append((current_number, current_song))

# Create a new soup for the extracted songs
new_soup = BeautifulSoup("<html><body></body></html>", "html.parser")

# Function to restore `&nbsp;` inside `mso-spacerun:yes` spans
def restore_nbsp(tag):
    for span in tag.find_all("span", style=re.compile(r"mso-spacerun:yes")):
        if span.string:
            span.string.replace_with(span.string.replace(" ", "\xa0"))  # Keep non-breaking spaces

# Wrap and append extracted songs
for number, song_content in songs:
    wrapper = new_soup.new_tag("div", **{"class": "sg", "id": f"song-{number}"})
    
    for element in song_content:
        restore_nbsp(element)  # Restore `&nbsp;` inside spacerun spans
        wrapper.append(element)

    new_soup.body.append(wrapper)

# Convert final soup object to a string and manually fix `&nbsp;`
html_string = str(new_soup)

# Replace `\xa0` with `&nbsp;` explicitly to ensure it's preserved
html_string = html_string.replace("\xa0", "&nbsp;")

# Save the extracted songs to a new file
with open(output_file, "w", encoding="utf-8") as file:
    file.write(html_string)

print(f"Extracted {len(songs)} songs. Processed HTML saved to {output_file}")