# showmap.py - Launches a map in the browser using an address from the
# command line or clipboard

import webbrowser, sys, pyperclip

if len(sys.argv) > 1:
    # Get address from command line.
    address = ' '.join(sys.argv[1:])
else:
    # Get address from clipboard.
    address = pyperclip.paste()

# TODO: Get address from clipboard.
if not address.strip():
    print("Error: No address provided. Please provide an address via command line or clipboard.")
    sys.exit(1)
    
# TODO: Open the web browser.
webbrowser.open('https://www.openstreetmap.org/search?query=' + address)
