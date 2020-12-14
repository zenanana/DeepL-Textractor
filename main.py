import time
import clipboard
from selenium import webdriver
from tkinter import Label, Tk, Button
from languages import languages

# Defaults set in case GUI is closed prematurely
language_selections = {
  "input": "jp",
  "output": "en"
}

# GUI for input & output language selection
for selection in language_selections:
  print(selection)
  language_selection_window = Tk()
  language_selection_window_label = Label(language_selection_window, text=f"Please select {selection} language.")
  language_selection_window_label.grid(row=0, column=0, columnspan=len(languages))
  def select_language(language):
    global selection
    language_selections[selection] = language
    language_selection_window.destroy()
  language_number = 0
  for language in languages:
    language_select_button = Button(language_selection_window, text=language, command= lambda bound_language=language: select_language(bound_language))
    language_select_button.grid(row=2, column=language_number)
    language_number += 1
  language_selection_window.mainloop()

# Declarations
loop_status = True

# Start a Selenium driver
driver_path = 'C:/webdrivers/chromedriver.exe'
driver = webdriver.Chrome(driver_path)

# DeepL translation is faster when input text is queried with URL instead of using driver to select input box element and send_keys
def get_deepl_url(input_text):
  return "https://www.deepl.com/en/translator#" + language_selections["input"] + "/" + language_selections["output"] + "/" + input_text

# Doing a preload with sample translation to eliminate preload times for actual subsequent translations
def get_initial_translation(text):
  global loop_status
  try:
    driver.get(get_deepl_url(languages[language_selections["input"]]))
  except:
    loop_status=False
    print("End")

def get_subsequent_translation(text):
  global loop_status
  try:
    driver.get(get_deepl_url(text))
  except:
    loop_status=False
    print("End")

def start_translation_process():
  global loop_status
  clipboard.copy(languages[language_selections["input"]])
  get_initial_translation(languages[language_selections["input"]])
  recent_value = clipboard.paste()
  loop_status = True
  while loop_status:
    tmp_value = clipboard.paste()
    if tmp_value != recent_value:
      recent_value = tmp_value
      get_subsequent_translation(recent_value)
    time.sleep(0.01)
  driver.quit()

start_translation_process()