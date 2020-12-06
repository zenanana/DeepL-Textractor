import time
import clipboard
from selenium import webdriver
from tkinter import Label, Tk, Button

# Language selection & placeholder texts for preloading
languages = {
  "jp": "選りすぐりのアンビエント作品",
  "zh": "氛围作品选",
  "de": "ausgewählte Umgebungsarbeiten",
  "fr": "des œuvres d'ambiance sélectionnées",
  "es": "obras de ambiente seleccionadas",
  "pt": "obras ambientais seleccionadas",
  "it": "opere ambientali selezionate",
  "nl": "geselecteerde omgevingswerken",
  "pl": "wybrane prace środowiskowe",
  "ru": "избранные окружающие работы"
}

loop_status = True

# Default set to Japanese in case initial selection GUI is exited without selection.
input_language = "jp"
output_language = "en"

# GUI for input language selection
language_selection_window = Tk()
language_selection_window_label = Label(language_selection_window, text="Please select language to translate from. Default is Japanese.")
language_selection_window_label.grid(row=0, column=0, columnspan=10)
def select_language(language):
  global input_language
  input_language = language
  language_selection_window.destroy()
language_number = 0
for language in languages:
  language_select_button = Button(language_selection_window, text=language, command= lambda bound_language=language: select_language(bound_language))
  language_select_button.grid(row=2, column=language_number)
  language_number += 1
language_selection_window.mainloop()


# Start a Selenium driver
driver_path = 'C:/webdrivers/chromedriver.exe'
driver = webdriver.Chrome(driver_path)

# URL logic
direct_url = "https://www.deepl.com/en/translator#" + input_language + "/" + output_language
def get_full_direct_url(text):
  return direct_url + "/" + text


def get_translation(timer, text):
  global loop_status
  try:
    driver.get(get_full_direct_url(text))
  except:
    loop_status=False
    print("End")
  
  
  # Code for copying result onto clipboard for display onto GUI
  '''time.sleep(timer)
  button_css = ' div.lmt__target_toolbar__copy button'
  button = driver.find_element_by_css_selector(button_css)
  button.click()
  while clipboard.paste() == "":
    button.click()
    time.sleep(0.2)
  clipboard.copy(text)'''


def start_translation_process():
  global loop_status
  clipboard.copy(languages[input_language])
  get_translation(5, languages[input_language])
  recent_value = clipboard.paste()
  loop_status = True
  while loop_status:
    tmp_value = clipboard.paste()
    if tmp_value == "Stop Script":
      loop_status = False
    if tmp_value != recent_value:
      recent_value = tmp_value
      get_translation(1.75, recent_value)
    time.sleep(0.1)
  driver.quit()

start_translation_process()