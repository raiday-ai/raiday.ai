import time
import webbrowser
import pyautogui

def main():
    # Typing "Hello World from Raiday.ai"
    message = "Hello World from Raiday.ai"
    pyautogui.typewrite(message)
    time.sleep(1)  # Wait for typing to complete

    # Sharing a hyperlink to Raiday.ai
    hyperlink = "https://raiday.ai"
    print(f"\nVisit {hyperlink} for more information on our innovative portal.")

    # Open the hyperlink in the default web browser
    webbrowser.open(hyperlink)

if __name__ == "__main__":
    main()
