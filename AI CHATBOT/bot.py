import pyautogui
import time
import pyperclip
import google.generativeai as genai

print("Starting in 3 seconds...")
time.sleep(1.5)

# 1. Define the coordinates

# icon_x, icon_y = 1102, 1045

pyautogui.FAILSAFE = True

def  is_last_msg_from_sender(chat_log,sender_name="chatname"):
    messages = chat_log.strip().split('/2025]')[-1]

    if sender_name in messages:
        return True
    else:
        return False



pyautogui.click(1249,1043 )
time.sleep(2)

while True:
   
    # pyautogui.click(1317, 906)
    # time.sleep(2)

    pyautogui.moveTo(702,233)
    pyautogui.dragTo(1141,1039, duration=1.5, button='left')

    pyautogui.hotkey('ctrl', 'c')
    pyautogui.click(1135,715) 
    time.sleep(2)

    chat_history = pyperclip.paste()
    print(chat_history)

    if is_last_msg_from_sender(chat_history):


        genai.configure(api_key="your api")

        act_as_me = f"""Act as me,you are a person nammed nitesh who speaks hindi,gujarati as well as english.
            he is from india and is a coder.you analyze chat history and response like nitesh but dont response long answer just give short and
            clear answer and if dont get any history then dont give any text this is the chat histort for analyze :{chat_history}"""
            # -- 2. Initialize the Model with the Settings --
            # Make sure to use a model that supports a large context, like 1.5 Flash or Pro
        model = genai.GenerativeModel(model_name="gemini-1.5-flash-latest")


        response = model.generate_content(act_as_me)
        pyperclip.copy(response.text)

        pyautogui.click(921, 1027)
        time.sleep(2)

        pyautogui.hotkey('ctrl', 'v')
        time.sleep(2)

        pyautogui.press('enter')