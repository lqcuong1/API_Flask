# # https://rapidapi.com/HiBrainy/api/text-to-speech5/endpoints
# import requests
# url = "https://text-to-speech5.p.rapidapi.com/api/tts"
# text = """
# About 30% of all the food we eat in the UK comes from the European Union, according to the British Retail Consortium (BRC) industry group.
# Britain imports nearly half of its fresh vegetables and the majority of its fruit, both mainly from the EU - and that's where the potential problem was.
# """
# payload = "tech=deep&text=" + text + "&language=en"
# headers = {
#     'content-type': "application/x-www-form-urlencoded",
#     'x-rapidapi-key': "269f38f00emshbddd98e513945e9p1efae6jsne54fced8b127",
#     'x-rapidapi-host': "text-to-speech5.p.rapidapi.com"
#     }
# response = requests.request("POST", url, data=payload, headers=headers)
# #download and save mp3 file on disk
# with open("test.mp3", "wb") as f:
#     f.write(response.content)

