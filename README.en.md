[EN](https://github.com/NUAAR/tess_lcd/blob/main/README.en.md) | [UA](https://github.com/NUAAR/tess_lcd/blob/main/README.md)

# Instruction

**We need two files**
* *main.py* – the program with wich the data will be downloaded.
* *requirements.txt* – a list of libraries that must be installed for the program to work.


1. Download files from GitHub:
    a) Press the green *Code* button, then *Download ZIP*
    b) Unzip the downloaded archive.

2. Move *main.py* and *requirements.txt* to the same folder for convenience. In this instruction, we will call this folder *Data*, but you can choose any name.

3. Open the terminal. In the case of Linux, it is called *Terminal*, for Windows it can be *PowerShell* or *cmd*. As a rule, it can be found by entering the corresponding name in the general search on the computer.

4. Go to the Data folder on the terminal:
     a) Right-click on the folder, find the option called Properties (or similar)
     b) Copy the path to the folder. In general, it should look like this: */path/to/folder/Data* (for example, the creator of the instructions, who uses Linux, has the path which looks like this: */home/dell/NUAAR/Data*)
     c) Enter the command in the terminal:
     ```
     cd /path/to/folder/Data
     ```

5. Install the libraries from the requirements.txt file (Note: it is enough to do this only once, it is not necessary to install them every time before using the program). To do this, enter the following command in the terminal:
```
pip install -r requirements.txt
```

6. Open main.py in any text editor and modify as needed:
     a) In the first line, enter the name of the object in the format *TIC XX...X*, for example:
     ```
     OBJECT: str = "TIC 141809359"
     ```
     b) In the second line, select the necessary sectors, for example:
     ```
     SECTORS: list = [1, 3, 66]
     ```
     If you want to load all sectors, leave the list empty, i.e.:
     ```
     SECTORS: list = []
     ```
     c) Save changes!

7. Run the program by entering the command
```
python3 main.py
```
if you use Linux, or
```
python main.py
```
if you use Windows.

The program may take several minutes to complete. As a result, a **mastDownload** folder should appear in the Data folder, in which the downloaded data will be located.
