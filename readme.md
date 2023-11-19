## Description

An alternative to windows classic explorer.

## Installation

If missing librairy, you can install it with command like

```
pip install pygame
```

If you want to change the directory of reading, you have to change the before last line. The default value is a directory named "test" at the same level as the python code.

```
display = Display(Path("./test/"))
```

To change the logo of the tool, you have to look at the variable ICONFILE

# How to make it executable

## 1 - install pyinstaller

```
pip install pyinstaller
```

## 2 - compilate

```
pyinstaller --noconsole explorer2.py
```

It will create a directory named `dist`.
You should take the .exe file in it and the \_internal directory should stay in the same directory as the explorer2.exe file
