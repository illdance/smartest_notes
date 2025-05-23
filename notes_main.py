from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QTextEdit, QLineEdit, QPushButton, QLabel, QListWidget, QApplication, QWidget, QHBoxLayout, QVBoxLayout
from PyQt5.QtWidgets import QInputDialog
import json

def search_tag():
    tag = tagovka.text()
    if tag != '' and bution5.text() == 'Искать заметки по тегу':
        notes_filtered = dict()
        for key in notes:
            if tag in notes[key]['теги']:
                notes_filtered[key] = notes[key]
        bution5.setText('Сбросить поиск')
        notsi.clear()
        tagi.clear()
        text_edidor.clear()
        notsi.addItems(notes_filtered)
    else:
        notsi.clear()
        notsi.addItems(notes)
        tagovka.clear()
        bution5.setText('Искать заметки по тегу')

def del_tag():
    if tagi.selectedItems():
        key = notsi.selectedItems()[0].text()
        tag = tagi.selectedItems()[0].text()
        notes[key]['теги'].remove(tag)
        tagi.clear()
        tagi.addItems(notes[key]['теги'])
        with open('notes_data.json', 'w') as file:
            json.dump(notes, file, sort_keys = True, ensure_ascii = False)

def add_tag():
    if notsi.selectedItems():
        key = notsi.selectedItems()[0].text()
        tag =tagovka.text()
        if tag != '' and not tag in notes[key]['теги']:
            notes[key]['теги'].append(tag)
            tagi.addItem(tag)
            tagovka.clear()
            with open('notes_data.json', 'w') as file:
                json.dump(notes, file, sort_keys = True, ensure_ascii = False)

def save_note():
    if notsi.selectedItems():
        key = notsi.selectedItems()[0].text()
        notes[key]['текст'] = text_edidor.toPlainText()
        with open('notes_data.json', 'w') as file:
            json.dump(notes, file, sort_keys = True, ensure_ascii = False)

def del_note():
    if notsi.selectedItems():
        key = notsi.selectedItems()[0].text()
        del notes[key]
        text_edidor.clear()
        notsi.clear()
        tagi.clear()
        notsi.addItems(notes)
        with open('notes_data.json', 'w') as file:
            json.dump(notes, file, sort_keys = True, ensure_ascii = False)

def show_note():
    key = notsi.selectedItems()[0].text()
    text_edidor.setText(notes[key]['текст'])
    tagi.clear()
    tagi.addItems(notes[key]['теги'])

def add_note():
    notes_name, ok = QInputDialog.getText(windov, 'Добавить заметку', 'Название заметки:')
    if ok:
        notes[notes_name] = {
            'текст': '',
            'теги': []
        }
    notsi.clear()
    notsi.addItems(notes)
    with open('notes_data.json', 'w') as file:
        json.dump(notes, file)

app = QApplication([])

windov = QWidget()
windov.setWindowTitle('Умнешие заметки')
windov.resize(600, 300)

glavLineiya = QHBoxLayout()
vertLineya1 = QVBoxLayout()
vertLineya2 = QVBoxLayout()
gorLineya1 = QHBoxLayout()
gorLineya2 = QHBoxLayout()

text_edidor = QTextEdit()
listing_name = QLabel('Список заметок')
tagger_name = QLabel('Список тегов')
bution = QPushButton('Создать заметку')
bution1 = QPushButton('Удалить заметку')
bution2 = QPushButton('Сохранить заметку')
bution3 = QPushButton('Добавить к заметке')
bution4 = QPushButton('Открепить от заметки')
bution5 = QPushButton('Искать заметки по тегу')
notsi = QListWidget()
tagi = QListWidget()
tagovka = QLineEdit()

gorLineya1.addWidget(bution)
gorLineya1.addWidget(bution1)
gorLineya2.addWidget(bution3)
gorLineya2.addWidget(bution4)

vertLineya1.addWidget(text_edidor)
vertLineya2.addWidget(listing_name)
vertLineya2.addWidget(notsi)
vertLineya2.addLayout(gorLineya1)
vertLineya2.addWidget(bution2)
vertLineya2.addWidget(tagger_name)
vertLineya2.addWidget(tagi)
vertLineya2.addWidget(tagovka)
vertLineya2.addLayout(gorLineya2)
vertLineya2.addWidget(bution5)

vertLineya2.addLayout(gorLineya2)
glavLineiya.addLayout(vertLineya1)
glavLineiya.addLayout(vertLineya2)

tagovka.setPlaceholderText('Введите тег:')

windov.setLayout(glavLineiya)

with open('notes_data.json', 'r') as file:
    notes = json.load(file)

notsi.addItems(notes)
notsi.itemClicked.connect(show_note)
bution.clicked.connect(add_note)
bution1.clicked.connect(del_note)
bution2.clicked.connect(save_note)
bution3.clicked.connect(add_tag)
bution4.clicked.connect(del_tag)
bution5.clicked.connect(search_tag)

windov.show()
app.exec()