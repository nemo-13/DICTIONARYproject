# coding: utf8

import sys
from PyQt5 import uic
from PyQt5.QtWidgets import *
import sqlite3
import random

res_of_combobox2 = 5
res_of_combobox3 = 'РУССКИЙ'

connection = sqlite3.connect('dictionary.db')
cursor = connection.cursor()
cursor.execute('''CREATE TABLE IF NOT EXISTS dictionary
                (id integer primary key autoincrement, in_russian TEXT, in_english TEXT)''')


class Dictionary(QMainWindow, QDialog):
    def __init__(self):
        super().__init__()
        uic.loadUi('MAIN_WINDOW.ui', self)
        self.setWindowTitle('Англо-Русский словарь')

        self.pushButton.clicked.connect(self.click_pushbutton)
        self.pushButton_4.clicked.connect(self.click_on_button_open_dictionary)
        self.pushButton_3.clicked.connect(self.click_on_translate)
        self.radioButton.setChecked(True)
        self.radioButton_2.setChecked(False)
        self.plainTextEdit_2.setEnabled(False)
        self.radioButton.country = "Russia"
        self.radioButton_2.country = "England"
        self.radioButton.toggled.connect(self.click_on_radioButton)
        self.radioButton_2.toggled.connect(self.click_on_radioButton)
        self.res = self.radioButton.country
        self.pushButton_2.clicked.connect(self.click_on_start_test)

    def click_on_radioButton(self):
        if self.radioButton.isChecked():
            self.res = self.radioButton.country
        if self.radioButton_2.isChecked():
            self.res = self.radioButton_2.country

    def click_on_translate(self):
        check_on_mistake = self.lineEdit_4.text()

        if self.res == self.radioButton.country:
            if not self.check_Russian(check_on_mistake):
                miss = Mistake(self)
                miss.show()
            else:
                result = cursor.execute("SELECT * FROM dictionary WHERE in_russian=?",
                                        (item_in_russian := self.lineEdit_4.text(),)).fetchall()
                connection.commit()
                if not result:
                    self.plainTextEdit_2.setPlainText('Ничего не нашлось')
                else:
                    self.plainTextEdit_2.setPlainText \
                        (f"Найден перевод с русского на английский слова {item_in_russian}")
                    self.tableWidget.setRowCount(len(result))
                    self.tableWidget.setColumnCount(len(result[0]))
                    self.titles = [description[0] for description in cursor.description]
                    for i, elem in enumerate(result):
                        for j, val in enumerate(elem):
                            self.tableWidget.setItem(i, j, QTableWidgetItem(str(val)))
        elif self.res == self.radioButton_2.country:
            if not self.check_English(check_on_mistake):
                miss = Mistake(self)
                miss.show()
            else:
                result = cursor.execute("SELECT * FROM dictionary WHERE in_english=?",
                                        (item_in_english := self.lineEdit_4.text(),)).fetchall()
                connection.commit()
                if not result:
                    self.plainTextEdit_2.setPlainText('Ничего не нашлось')
                else:
                    self.plainTextEdit_2.setPlainText \
                        (f"Найден перевод с английского на русский слова {item_in_english}")
                    self.tableWidget.setRowCount(len(result))
                    self.tableWidget.setColumnCount(len(result[0]))
                    self.titles = [description[0] for description in cursor.description]
                    for i, elem in enumerate(result):
                        for j, val in enumerate(elem):
                            self.tableWidget.setItem(i, j, QTableWidgetItem(str(val)))

    def click_on_start_test(self):
        start_test = StartOfTheTest(self)
        start_test.show()

    def click_on_button_open_dictionary(self):
        dict = OpenDictionary(self)
        dict.show()

    def click_pushbutton(self):
        text_in_russian = self.lineEdit.text()
        text_in_english = self.lineEdit_2.text()
        if not self.check_Russian(text_in_russian):
            miss = Mistake(self)
            miss.show()
        if not self.check_English(text_in_english):
            miss = Mistake(self)
            miss.show()
        else:
            cursor.execute("INSERT INTO dictionary (in_russian, in_english) VALUES (?, ?)",
                           (text_in_russian, text_in_english))
            connection.commit()

    def check_Russian(self, text):
        cyrillic = 'ёйцукенгшщзхъфывапролджэячсмитьбю-'
        for i in text:
            i = i.lower()
            if i not in cyrillic:
                return False
        return True

    def check_English(self, text):
        english = 'qwertyuiopasdfghjklzxcvbnm-'
        for i in text:
            i = i.lower()
            if i not in english:
                return False
        return True


class Mistake(QDialog):
    def __init__(self, flags, *args, **kwargs):
        super().__init__(flags, *args, **kwargs)
        uic.loadUi('MISTAKE.ui', self)
        self.setWindowTitle('Ошибка')
        self.setEnabled(False)
        self.plainTextEdit.setPlainText('ВВЕДЕНОЕ СЛОВО СОДЕРЖИТ НЕДОПУСТИМЫЕ СИМВОЛЫ')


class OpenDictionary(QDialog):
    def __init__(self, flags, *args, **kwargs):
        super().__init__(flags, *args, **kwargs)
        uic.loadUi('OPEN_DICTIONARY.ui', self)
        result = cursor.execute("SELECT * FROM dictionary WHERE id").fetchall()
        self.tableWidget.setRowCount(len(result))
        self.tableWidget.setColumnCount(len(result[0]))
        self.titles = [description[0] for description in cursor.description]
        for i, elem in enumerate(result):
            for j, val in enumerate(elem):
                self.tableWidget.setItem(i, j, QTableWidgetItem(str(val)))


class StartOfTheTest(QDialog):
    def __init__(self, flags, *args, **kwargs):
        super().__init__(flags, *args, **kwargs)
        uic.loadUi('START OF THE TEST.ui', self)
        self.comboBox.activated[str].connect(self.onActivated)
        self.comboBox_2.activated[str].connect(self.onActivated)
        self.comboBox_3.activated[str].connect(self.onActivated2)
        self.pushButton.clicked.connect(self.click_on_open_test)
        self.res_of_combobox = 2
        self.res_of_combobox2 = 5

    def onActivated(self, number):
        global res_of_combobox2
        if int(number) == 2:
            self.res_of_combobox = 2
        elif int(number) == 4:
            self.res_of_combobox = 4

        elif int(number) == 5:
            self.res_of_combobox2 = 5

        elif int(number) == 10:
            res_of_combobox2 = 10

    def onActivated2(self, language):
        global res_of_combobox3
        res_of_combobox3 = language
        # print(res_of_combobox3)

    def click_on_open_test(self):
        if self.res_of_combobox == 2:
            test_with_two_options = TestWithTwoOptions(self)
            test_with_two_options.show()
        elif self.res_of_combobox == 4:
            test_with_four_options = TestWithFourOptions(self)
            test_with_four_options.show()


number_of_correct_answer = 0


class TestWithTwoOptions(QDialog):
    def __init__(self, flags, *args, **kwargs):
        super().__init__(flags, *args, **kwargs)
        uic.loadUi('TEST WITH TWO OPTIONS.ui', self)
        self.questions_in_the_test = 2
        self.res_of_radiobutton = 1
        self.radioButton.setChecked(True)
        global res_of_combobox2, res_of_combobox3
        self.radioButton.toggled.connect(self.click_on_radioButton)
        self.radioButton_2.toggled.connect(self.click_on_radioButton)
        self.lineEdit.setEnabled(False)
        self.lineEdit_2.setEnabled(False)
        self.lineEdit_3.setEnabled(False)
        self.setWindowTitle(f'Тест из {res_of_combobox2} вопросов')
        self.plainTextEdit_2.setEnabled(False)
        self.plainTextEdit.setEnabled(False)
        self.result = cursor.execute("SELECT * FROM dictionary WHERE id").fetchall()
        self.questions = random.sample(self.result, res_of_combobox2)
        self.number_of_question = 1
        self.plainTextEdit.setPlainText(f'Вопрос {self.number_of_question}')
        self.current_issue = random.choice(self.questions)
        self.questions.pop(self.questions.index(self.current_issue))
        self.wrong_answer = (random.choice(self.result))
        global number_of_correct_answer
        number_of_correct_answer = 0
        self.pushButton.clicked.connect(self.click_on_next_question)

        self.random_number = random.choice([1, 2, 1, 2, 1, 2])

        self.res_of_radiobutton = 1
        self.radioButton.number = 1
        self.radioButton_2.number = 2
        self.a = 1
        self.b = 2
        if res_of_combobox3 == 'РУССКИЙ':

            self.in_english = self.current_issue[self.b]
            self.plainTextEdit_2.setPlainText(f'С английского на русский слово {self.in_english} переводится как:')
            if self.random_number == 1:
                self.lineEdit_2.setText(self.wrong_answer[1])
                self.lineEdit.setText(self.current_issue[self.a])
            else:
                self.lineEdit_2.setText(self.current_issue[self.a])
                self.lineEdit.setText(self.wrong_answer[1])

        elif res_of_combobox3 == 'АНГЛИЙСКИЙ':
            self.wrong_answer = (random.choice(self.result))
            self.in_english = self.current_issue[self.a]
            self.plainTextEdit_2.setPlainText(f'С русского на английский слово {self.in_english} переводится как:')
            if self.random_number == 1:
                self.lineEdit_2.setText(self.wrong_answer[2])
                self.lineEdit.setText(self.current_issue[2])
            else:
                self.lineEdit_2.setText(self.current_issue[2])
                self.lineEdit.setText(self.wrong_answer[2])

    def click_on_radioButton(self):
        if self.radioButton.isChecked():
            self.res_of_radiobutton = self.radioButton.number
        elif self.radioButton_2.isChecked():
            self.res_of_radiobutton = self.radioButton_2.number

    def click_on_next_question(self):
        global number_of_correct_answer, res_of_combobox2
        self.number_of_question += 1
        self.plainTextEdit.setPlainText(f'Вопрос {self.number_of_question}')
        if int(self.res_of_radiobutton) == self.random_number:
            self.lineEdit_3.setText('НА ПРЕДЫДУЩИЙ ВОПРОС ВЫ ОТВЕТИЛИ ПРАВИЛЬНО')
            number_of_correct_answer += 1
        elif int(self.res_of_radiobutton) != self.random_number:
            self.lineEdit_3.setText('НА ПРЕДЫДУЩИЙ ВОПРОС ВЫ ОТВЕТИЛИ НЕПРАВИЛЬНО')

        if self.number_of_question > res_of_combobox2:
            res_of_test = EndOfTest(self)
            res_of_test.show()

        else:
            if res_of_combobox3 == 'РУССКИЙ':
                self.wrong_answer = (random.choice(self.result))
                self.current_issue = random.choice(self.questions)
                self.questions.pop(self.questions.index(self.current_issue))
                self.in_english = self.current_issue[self.b]
                self.plainTextEdit_2.setPlainText(f'С английского на русский слово {self.in_english} переводится как:')
                self.random_number = random.choice([1, 2])
                if self.random_number == 1:
                    self.lineEdit_2.setText(self.wrong_answer[1])
                    self.lineEdit.setText(self.current_issue[self.a])
                else:
                    self.lineEdit_2.setText(self.current_issue[self.a])
                    self.lineEdit.setText(self.wrong_answer[1])
            elif res_of_combobox3 == 'АНГЛИЙСКИЙ':
                self.current_issue = random.choice(self.questions)
                self.wrong_answer = random.choice(self.result)
                self.questions.pop(self.questions.index(self.current_issue))
                self.in_english = self.current_issue[self.a]
                self.plainTextEdit_2.setPlainText(f'С русского на английский слово {self.in_english} переводится как:')
                self.random_number = random.choice([1, 2])
                if self.random_number == 1:
                    self.lineEdit_2.setText(self.wrong_answer[2])
                    self.lineEdit.setText(self.current_issue[2])
                elif self.random_number == 2:
                    self.lineEdit_2.setText(self.current_issue[2])
                    self.lineEdit.setText(self.wrong_answer[2])
        self.radioButton.setChecked(True)


class TestWithFourOptions(QDialog):
    def __init__(self, flags, *args, **kwargs):
        super().__init__(flags, *args, **kwargs)
        uic.loadUi('TEST WITH FOUR OPTIONS.ui', self)
        self.questions_in_the_test = 4
        global res_of_combobox2, res_of_combobox3
        self.setWindowTitle(f'Тест из {res_of_combobox2} вопросов')
        self.result = cursor.execute("SELECT * FROM dictionary WHERE id").fetchall()
        self.questions = random.sample(self.result, res_of_combobox2)
        self.setWindowTitle(f'Тест из {res_of_combobox2} вопросов')
        self.plainTextEdit.setEnabled(False)
        self.plainTextEdit_2.setEnabled(False)
        self.lineEdit.setEnabled(False)
        self.lineEdit_2.setEnabled(False)
        self.lineEdit_3.setEnabled(False)
        self.lineEdit_4.setEnabled(False)
        self.lineEdit_5.setEnabled(False)

        self.radioButton.toggled.connect(self.click_on_radioButton)
        self.radioButton_2.toggled.connect(self.click_on_radioButton)
        self.radioButton_3.toggled.connect(self.click_on_radioButton)
        self.radioButton_4.toggled.connect(self.click_on_radioButton)
        self.res_of_radiobutton = 1
        self.radioButton.number = 1
        self.radioButton_2.number = 2
        self.radioButton_3.number = 3
        self.radioButton_4.number = 4

        self.number_of_question = 1
        self.plainTextEdit.setPlainText(f'Вопрос {self.number_of_question}')
        self.current_issue = random.choice(self.questions)
        self.questions.pop(self.questions.index(self.current_issue))

        self.wrong_answer1 = (random.choice(self.result))
        self.wrong_answer2 = (random.choice(self.result))
        self.wrong_answer3 = (random.choice(self.result))

        global number_of_correct_answer
        number_of_correct_answer = 0
        self.pushButton.clicked.connect(self.click_on_next_question)

        self.random_number = random.choice([1, 2, 3, 4, 1, 2, 3, 4, 1, 2, 3, 4])

        if res_of_combobox3 == 'РУССКИЙ':

            self.in_english = self.current_issue[2]
            self.plainTextEdit_2.setPlainText(f'С английского на русский слово {self.in_english} переводится как:')
            if self.random_number == 1:
                self.lineEdit.setText(self.current_issue[1])
                self.lineEdit_2.setText(self.wrong_answer1[1])
                self.lineEdit_3.setText(self.wrong_answer2[1])
                self.lineEdit_4.setText(self.wrong_answer3[1])
            elif self.random_number == 2:
                self.lineEdit_2.setText(self.current_issue[1])
                self.lineEdit.setText(self.wrong_answer1[1])
                self.lineEdit_3.setText(self.wrong_answer2[1])
                self.lineEdit_4.setText(self.wrong_answer3[1])
            elif self.random_number == 3:
                self.lineEdit_3.setText(self.current_issue[1])
                self.lineEdit_2.setText(self.wrong_answer1[1])
                self.lineEdit.setText(self.wrong_answer2[1])
                self.lineEdit_4.setText(self.wrong_answer3[1])
            elif self.random_number == 4:
                self.lineEdit_4.setText(self.current_issue[1])
                self.lineEdit_2.setText(self.wrong_answer1[1])
                self.lineEdit_3.setText(self.wrong_answer2[1])
                self.lineEdit.setText(self.wrong_answer3[1])

        elif res_of_combobox3 == 'АНГЛИЙСКИЙ':
            self.in_english = self.current_issue[1]
            self.plainTextEdit_2.setPlainText(f'С русского на английский слово {self.in_english} переводится как:')
            if self.random_number == 1:
                self.lineEdit.setText(self.current_issue[2])
                self.lineEdit_2.setText(self.wrong_answer1[2])
                self.lineEdit_3.setText(self.wrong_answer2[2])
                self.lineEdit_4.setText(self.wrong_answer3[2])
            elif self.random_number == 2:
                self.lineEdit_2.setText(self.current_issue[2])
                self.lineEdit.setText(self.wrong_answer1[2])
                self.lineEdit_3.setText(self.wrong_answer2[2])
                self.lineEdit_4.setText(self.wrong_answer3[2])
            elif self.random_number == 3:
                self.lineEdit_3.setText(self.current_issue[2])
                self.lineEdit_2.setText(self.wrong_answer1[2])
                self.lineEdit.setText(self.wrong_answer2[2])
                self.lineEdit_4.setText(self.wrong_answer3[2])
            elif self.random_number == 4:
                self.lineEdit_4.setText(self.current_issue[2])
                self.lineEdit_2.setText(self.wrong_answer1[2])
                self.lineEdit_3.setText(self.wrong_answer2[2])
                self.lineEdit.setText(self.wrong_answer3[2])

    def click_on_radioButton(self):
        if self.radioButton.isChecked():
            self.res_of_radiobutton = self.radioButton.number
        elif self.radioButton_2.isChecked():
            self.res_of_radiobutton = self.radioButton_2.number
        elif self.radioButton_3.isChecked():
            self.res_of_radiobutton = self.radioButton_3.number
        elif self.radioButton_4.isChecked():
            self.res_of_radiobutton = self.radioButton_4.number

    def click_on_next_question(self):
        global number_of_correct_answer, res_of_combobox2
        self.number_of_question += 1
        self.plainTextEdit.setPlainText(f'Вопрос {self.number_of_question}')
        if int(self.res_of_radiobutton) == self.random_number:
            self.lineEdit_5.setText('НА ПРЕДЫДУЩИЙ ВОПРОС ВЫ ОТВЕТИЛИ ПРАВИЛЬНО')
            number_of_correct_answer += 1
        elif int(self.res_of_radiobutton) != self.random_number:
            self.lineEdit_5.setText('НА ПРЕДЫДУЩИЙ ВОПРОС ВЫ ОТВЕТИЛИ НЕПРАВИЛЬНО')

        if self.number_of_question > res_of_combobox2:
            res_of_test = EndOfTest(self)
            res_of_test.show()

        else:
            if res_of_combobox3 == 'РУССКИЙ':
                self.wrong_answer1 = (random.choice(self.result))
                self.wrong_answer2 = (random.choice(self.result))
                self.wrong_answer3 = (random.choice(self.result))

                self.random_number = random.choice([1, 2, 3, 4, 1, 2, 3, 4, 1, 2, 3, 4])
                self.wrong_answer = (random.choice(self.result))
                self.current_issue = random.choice(self.questions)
                self.questions.pop(self.questions.index(self.current_issue))
                self.in_english = self.current_issue[2]
                self.plainTextEdit_2.setPlainText(f'С английского на русский слово {self.in_english} переводится как:')
                if self.random_number == 1:
                    self.lineEdit.setText(self.current_issue[1])
                    self.lineEdit_2.setText(self.wrong_answer1[1])
                    self.lineEdit_3.setText(self.wrong_answer2[1])
                    self.lineEdit_4.setText(self.wrong_answer3[1])
                elif self.random_number == 2:
                    self.lineEdit_2.setText(self.current_issue[1])
                    self.lineEdit.setText(self.wrong_answer1[1])
                    self.lineEdit_3.setText(self.wrong_answer2[1])
                    self.lineEdit_4.setText(self.wrong_answer3[1])
                elif self.random_number == 3:
                    self.lineEdit_3.setText(self.current_issue[1])
                    self.lineEdit_2.setText(self.wrong_answer1[1])
                    self.lineEdit.setText(self.wrong_answer2[1])
                    self.lineEdit_4.setText(self.wrong_answer3[1])
                elif self.random_number == 4:
                    self.lineEdit_4.setText(self.current_issue[1])
                    self.lineEdit_2.setText(self.wrong_answer1[1])
                    self.lineEdit_3.setText(self.wrong_answer2[1])
                    self.lineEdit.setText(self.wrong_answer3[1])
            elif res_of_combobox3 == 'АНГЛИЙСКИЙ':
                self.wrong_answer1 = (random.choice(self.result))
                self.wrong_answer2 = (random.choice(self.result))
                self.wrong_answer3 = (random.choice(self.result))
                self.random_number = random.choice([1, 2, 3, 4, 1, 2, 3, 4, 1, 2, 3, 4])
                self.wrong_answer = (random.choice(self.result))
                self.current_issue = random.choice(self.questions)
                self.questions.pop(self.questions.index(self.current_issue))
                self.in_english = self.current_issue[1]
                self.plainTextEdit_2.setPlainText(f'С русского на английский слово {self.in_english} переводится как:')
                if self.random_number == 1:
                    self.lineEdit.setText(self.current_issue[2])
                    self.lineEdit_2.setText(self.wrong_answer1[2])
                    self.lineEdit_3.setText(self.wrong_answer2[2])
                    self.lineEdit_4.setText(self.wrong_answer3[2])
                elif self.random_number == 2:
                    self.lineEdit_2.setText(self.current_issue[2])
                    self.lineEdit.setText(self.wrong_answer1[2])
                    self.lineEdit_3.setText(self.wrong_answer2[2])
                    self.lineEdit_4.setText(self.wrong_answer3[2])
                elif self.random_number == 3:
                    self.lineEdit_3.setText(self.current_issue[2])
                    self.lineEdit_2.setText(self.wrong_answer1[2])
                    self.lineEdit.setText(self.wrong_answer2[2])
                    self.lineEdit_4.setText(self.wrong_answer3[2])
                elif self.random_number == 4:
                    self.lineEdit_4.setText(self.current_issue[2])
                    self.lineEdit_2.setText(self.wrong_answer1[2])
                    self.lineEdit_3.setText(self.wrong_answer2[2])
                    self.lineEdit.setText(self.wrong_answer3[2])
        self.radioButton.setChecked(True)


class EndOfTest(QDialog):
    def __init__(self, flags, *args, **kwargs):
        super().__init__(flags, *args, **kwargs)
        uic.loadUi('END OF TEST.ui', self)
        global number_of_correct_answer, res_of_combobox2
        self.lineEdit.setText(
            f'В тесте из {res_of_combobox2} вопросов вы ответили правильно на {number_of_correct_answer}')
        self.lineEdit.setEnabled(False)
        self.setWindowTitle('РЕЗУЛЬТАТЫ')


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Dictionary()
    ex.show()
    sys.exit(app.exec())
