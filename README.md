# MemeBot
![](https://img.shields.io/badge/running-true-lightgreen)
[![Code Grade](https://www.code-inspector.com/project/20039/status/svg)](https://www.code-inspector.com)
## Use this bot
[MemeBot](https://t.me/make_meme_bot)  
Language Support: English and Traditional Chinese  
### Commands
`/help` show help.  
`/template {template_id}` show template usage, you can visit https://siriuskoan.github.io/MemeBot to see all available templates.  
`/make {template_id},{text1},{text2},...`  make a meme, and you can also press the button to store the meme and publish it to get the id of the meme which allows others to get access to your meme.
`/publish {meme_id}` get a published meme by its id.  
`/rank` get the rank of every template.  

### Get started
1. Visit https://siriuskoan.github.io/MemeBot to choose a template you want to use.
2. Type `/template {template_id}` to get the template usage.
3. Type `/make {template_id},{text1},{text2},...` to make your own meme, and you can publish it if you want.
4. Store the meme photo to your device or share it to others.
5. If you want others to use your meme, tell them the meme id which will be shown when you press 'Sore and publish' button.

## Add a new template
1. Add the **png file** to templates folder, and the filename should be an integer that hasn't been used. The integer will be the **template ID**.
2. Add the **template ID** to templates which is a dictionary in `templates.py`. The key `position` indicates the coordinates of the center of the words that user inputs, and the key `color` means the font color which basically depends on the background color of the template.
3. Add the template to `index.html`, which allows users to see this template.
4. Check everything works fine and create a PR!