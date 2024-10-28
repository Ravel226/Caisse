## Setup

To setup the application locally, you should have a code editor(VS Code) and python installed in your computer (Version 3.9 minimum)

PS: During the installation of python you will need to select "add to path". Be carefull!

#### - Create Virtual Environment

Open the terminal in your code editor (crtl + %)

Enter these commands based on your Operating System

<br>
###### # Mac

```
python3 -m venv venv
source venv/bin/activate
```

###### # Windows (Optionnal if you don't have time)

```
python -m venv venv
venv\Scripts\activate
```

<br>

#### - Install dependencies

```
pip install --upgrade pip
pip install -r requirements.txt
```

<br>

#### - Run application

```
python main.py
```

<br>

Enjoy!

<br>

#### - Advanced steps

How to make an executable: In the terminal, type:

```
pyinstaller --onefile --windowed main.py
```
<br>