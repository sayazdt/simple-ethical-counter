# from dbr import *
import flet as ft
import pathlib
from google import genai
from google.genai import types
import PIL.Image
import easygui



client = genai.Client(api_key='AIzaSyDQnB2xE-NyPBSfukf-uWlcEw42tpwsLuw')

# license_key = "LICENSE-KEY"
# BarcodeReader.init_license(license_key)
# reader = BarcodeReader()

# for m in genai.list_models():
#     if 'generateContent' in m.supported_generation_methods:
#         print(m.name)


class Message():
    def __init__(self, user_name: str, text: str, message_type: str, is_image: bool = False):
        self.user_name = user_name
        self.text = text
        self.message_type = message_type
        self.is_image = is_image


class ChatMessage(ft.Row):
    def __init__(self, message: Message):
        super().__init__()
        self.vertical_alignment = "start"
        if message.is_image:
            self.controls = [
                ft.CircleAvatar(
                    content=ft.Text(self.get_initials(message.user_name)),
                    color=ft.Colors.WHITE,
                    bgcolor=self.get_avatar_color(message.user_name),
                ),
                ft.Column(
                    [
                        ft.Text(message.user_name, weight="bold"),
                        ft.Image(src=message.text, width=300,
                                 height=300, fit=ft.ImageFit.CONTAIN),
                    ],
                    tight=True,
                    spacing=2,
                ),
            ]
        else:
            self.controls = [
                ft.CircleAvatar(
                    content=ft.Text(self.get_initials(message.user_name)),
                    color=ft.Colors.WHITE,
                    bgcolor=self.get_avatar_color(message.user_name),
                ),
                ft.Column(
                    [
                        ft.Text(message.user_name, weight="bold"),
                        ft.Text(message.text, selectable=True),
                    ],
                    tight=True,
                    spacing=2,
                ),
            ]

    def get_initials(self, user_name: str):
        if user_name:
            return user_name[:1].capitalize()
        else:
            return "Unknown"  # or any default value you prefer

    def get_avatar_color(self, user_name: str):
        if user_name == "Me":
            return ft.Colors.BLUE
        elif user_name == "DBR":
            return ft.Colors.ORANGE
        else:
            return ft.Colors.RED


image_path = None
barcode_text = None


def main(page: ft.Page):
    page.horizontal_alignment = "stretch"
    page.rtl = "True"
    page.title = "Gemini Chatbot"
    page.theme = ft.Theme(color_scheme_seed=ft.Colors.GREEN)
    page.dark_theme = ft.Theme(color_scheme_seed=ft.Colors.BLACK)

    def pick_files_result(e:ft.FilePickerResultEvent):
        global image_path, barcode_text
        barcode_text = None
        image_path = None
        if e.files != None:
            image_path = e.files[0].path
            print("\n\n\n",e.files,e.path,"\n\n\n")
            # page.pubsub.send_all(
            m = Message("Me", image_path, message_type="chat_message", is_image=True)
            on_message(m)


            text_results = None
            # try:
            #     text_results = reader.decode_file(image_path)

            #     # if text_results != None:
            #     #     for text_result in text_results:
            #     #         print("Barcode Format : ")
            #     #         print(text_result.barcode_format_string)
            #     #         print("Barcode Text : ")
            #     #         print(text_result.barcode_text)
            #     #         print("Localization Points : ")
            #     #         print(text_result.localization_result.localization_points)
            #     #         print("Exception : ")
            #     #         print(text_result.exception)
            #     #         print("-------------")
            # except BarcodeReaderError as bre:
            #     print(bre)

            # if text_results != None:
            #     barcode_text = text_results[0].barcode_text
            #     page.pubsub.send_all(
            #         Message("DBR", barcode_text, message_type="chat_message"))

    pick_files_dialog = ft.FilePicker(on_result=pick_files_result)
    page.overlay.append(pick_files_dialog)

    def pick_file(e):
        pick_files_dialog.pick_files()

    def clear_message(e):
        global image_path
        image_path = None
        chat.controls.clear()
        page.update()

    def send_message_click(e):
        global image_path
        if new_message.value != "":
            # page.pubsub.send_all()
            m = Message("Me", new_message.value, message_type="chat_message")
            on_message(m)

            question = new_message.value

            new_message.value = ""
            new_message.focus()
            page.update()

            # page.pubsub.send_all(
            m = Message("Gemini", "Thinking...", message_type="chat_message")
            on_message(m)
            instruction = "Suppose you are an Iranian Shia Muslim psychologist and you want to solve your audience's psychological and social problems based on your religious teachings, using examples from the lives of the Prophet and Shia Muslim imams."
            if image_path == None:
                response = client.models.generate_content(model="gemini-2.5-pro-exp-03-25",config=types.GenerateContentConfig(system_instruction=instruction), contents=question)
            else:
                image = PIL.Image.open(image_path)
                response = client.models.generate_content(model="gemini-2.5-pro-exp-03-25",config=types.GenerateContentConfig(system_instruction=instruction),contents=[question, image])


            # page.pubsub.send_all(
            m=Message("Gemini", response.text, message_type="chat_message")
            on_message(m)

    def on_message(message: Message):
        if message.message_type == "chat_message":
            m = ChatMessage(message)
        elif message.message_type == "login_message":
            m = ft.Text(message.text, italic=True,
                        color=ft.Colors.BLACK45, size=12)
        chat.controls.append(m)
        print(m)
        print(chat.controls)
        page.update()

    # page.pubsub.subscribe(on_message)

    # Chat messages
    chat = ft.ListView(
        expand=True,
        spacing=10,
        auto_scroll=True,
    )

    # A new message entry form
    new_message = ft.TextField(
        hint_text="Write a message...",
        autofocus=True,
        shift_enter=True,
        min_lines=1,
        max_lines=5,
        filled=True,
        expand=True,
        on_submit=send_message_click,
    )

    # Add everything to the page
    page.add(
        ft.Container(
            content=chat,
            border=ft.border.all(1, ft.Colors.OUTLINE),
            border_radius=5,
            padding=20,
            expand=True,
            margin=10,

        ),
        ft.Row(
            [
                ft.IconButton(
                    icon=ft.icons.UPLOAD_FILE,
                    tooltip="Pick an image",
                    on_click=pick_file,
                ),
                new_message,
                ft.IconButton(
                    icon=ft.icons.SEND_ROUNDED,
                    tooltip="Send message",
                    on_click=send_message_click,
                ),
                ft.IconButton(
                    icon=ft.icons.CLEAR_ALL,
                    tooltip="Clear all messages",
                    on_click=clear_message,
                ),
            ]
        ),
    )


ft.app(main, )#view=ft.AppView.WEB_BROWSER)
