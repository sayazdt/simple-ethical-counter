import flet as ft
from google import genai
from google.genai import types

client = genai.Client(api_key='AIzaSyDQnB2xE-NyPBSfukf-uWlcEw42tpwsLuw')

def main(page: ft.Page):
    def btn_click(e):
        if not txt_name.value:
            txt_name.error_text = "Please enter your Question"
            page.update()
        else:
            name = txt_name.value
            page.clean()
            instruction = "You are a muslim shia who wants to invite all people to islam shia with kind language."
            page.add(ft.Text(client.models.generate_content(model="gemini-2.5-pro-exp-03-25",config=types.GenerateContentConfig(system_instruction=instruction), contents=name)))

    txt_name = ft.TextField(label="Your Question")

    page.add(txt_name, ft.ElevatedButton("AI answer!", on_click=btn_click))


ft.app(main)