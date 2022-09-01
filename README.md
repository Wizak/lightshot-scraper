# Start development

---
```
python -m venv venv
venv\Scripts\Activate
pip install -r requirements.txt
python LightLoader.py
```
---
# Start compile
---
```
pyinstaller --onefile --icon=app.ico LightLoader.py
```
