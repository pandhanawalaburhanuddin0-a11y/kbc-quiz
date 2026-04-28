from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.core.window import Window
from kivy.uix.popup import Popup

Window.size = (400, 800)

questions = [
    ["Which of these is the largest planet in our Solar System?", "Mars", "Jupiter", "Earth", "Saturn", 2],
    ["Who was the first Indian to travel in space?", "Kalpana Chawla", "Sunita Williams", "Rakesh Sharma", "Ravish Malhotra", 3],
    ["Which city is famously known as the 'Pink City' of India?", "Jaipur", "Udaipur", "Jodhpur", "Bikaner", 1],
    ["How many seconds are there in one hour?", "60", "360", "3600", "36000", 3],
    ["In the game of Chess, which piece can move only diagonally?", "Rook", "Knight", "Bishop", "King", 3],
    ["Which organ in the human body is responsible for pumping blood?", "Lungs", "Liver", "Heart", "Kidney", 3],
    ["According to the Ramayana, who was the wife of Lord Rama?", "Urmila", "Sita", "Mandavi", "Shrutakirti", 2],
    ["Which of these is the national bird of India?", "Parrot", "Sparrow", "Peacock", "Eagle", 3],
    ["Who is known as the 'Father of the Indian Constitution'?", "Mahatma Gandhi", "Jawaharlal Nehru", "B.R. Ambedkar", "Sardar Patel", 3],
    ["Which of these elements is represented by the chemical symbol 'Au'?", "Silver", "Aluminium", "Gold", "Copper", 3],
    ["Which Indian state is the world's largest producer of Saffron?", "Himachal Pradesh", "Jammu and Kashmir", "Sikkim", "Uttarakhand", 2],
    ["What color is the blood of an octopus?", "Red", "Blue", "Green", "White", 2],
    ["In which year did India gain independence from British rule?", "1945", "1946", "1947", "1948", 3],
    ["Which of these is the longest river in the world?", "Amazon", "Nile", "Ganga", "Mississippi", 2],
    ["Who was the first woman to win an Olympic medal for India?", "P.T. Usha", "Karnam Malleswari", "Saina Nehwal", "Mary Kom", 2],
    ["Which monument was built by the Mughal Emperor Akbar in Agra?", "Taj Mahal", "Red Fort", "Buland Darwaza", "Humayun's Tomb", 2],
]

levels = [5000, 10000, 15000, 20000, 25000, 50000, 100000, 200000, 300000, 500000, 750000, 1250000, 2500000, 5000000, 10000000, 70000000]

class QuizApp(App):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.current_question = 0
        self.money = 0
        self.answered = False

    def build(self):
        self.main_layout = BoxLayout(orientation='vertical', padding=10, spacing=10)
        
        # Title
        title = Label(text='[b]KBC Quiz[/b]', markup=True, size_hint_y=0.1, font_size='24sp')
        self.main_layout.add_widget(title)
        
        # Question number and prize money
        self.info_label = Label(text='', size_hint_y=0.1, font_size='14sp')
        self.main_layout.add_widget(self.info_label)
        
        # Question
        self.question_label = Label(text='', size_hint_y=0.15, font_size='16sp', markup=True)
        self.main_layout.add_widget(self.question_label)
        
        # Options (Grid)
        self.options_layout = GridLayout(cols=2, spacing=10, size_hint_y=0.5)
        self.main_layout.add_widget(self.options_layout)
        
        # Result message
        self.result_label = Label(text='', size_hint_y=0.1, font_size='14sp', color=(0, 1, 0, 1))
        self.main_layout.add_widget(self.result_label)
        
        # Buttons (Next, Quit)
        button_layout = BoxLayout(size_hint_y=0.1, spacing=10)
        next_btn = Button(text='Next', background_color=(0.2, 0.6, 1, 1))
        next_btn.bind(on_press=self.next_question)
        quit_btn = Button(text='Quit', background_color=(1, 0.2, 0.2, 1))
        quit_btn.bind(on_press=self.quit_game)
        button_layout.add_widget(next_btn)
        button_layout.add_widget(quit_btn)
        self.main_layout.add_widget(button_layout)
        
        self.load_question()
        return self.main_layout

    def load_question(self):
        if self.current_question >= len(questions):
            self.show_final_result()
            return
        
        question = questions[self.current_question]
        self.info_label.text = f'Question {self.current_question + 1} | Prize: Rs. {levels[self.current_question]:,}'
        self.question_label.text = f'[b]{question[0]}[/b]'
        
        self.options_layout.clear_widgets()
        self.selected_answer = None
        
        for i in range(1, 5):
            btn = Button(text=question[i], background_color=(0.3, 0.3, 0.3, 1), color=(1, 1, 1, 1))
            btn.answer_index = i
            btn.bind(on_press=self.select_answer)
            self.options_layout.add_widget(btn)
        
        self.result_label.text = ''
        self.answered = False

    def select_answer(self, instance):
        if self.answered:
            return
        
        self.selected_answer = instance.answer_index
        question = questions[self.current_question]
        
        if self.selected_answer == question[-1]:
            self.result_label.text = '[color=00ff00]✓ Correct Answer![/color]'
            self.result_label.color = (0, 1, 0, 1)
            instance.background_color = (0, 1, 0, 1)
            
            self.money = levels[self.current_question]
            
            if self.current_question == 4:
                self.money = 25000
            elif self.current_question == 9:
                self.money = 500000
            elif self.current_question == 15:
                self.money = 70000000
        else:
            self.result_label.text = '[color=ff0000]✗ Wrong Answer![/color]'
            self.result_label.color = (1, 0, 0, 1)
            instance.background_color = (1, 0, 0, 1)
        
        self.answered = True

    def next_question(self, instance):
        if not self.answered:
            self.result_label.text = '[color=ffff00]Please select an answer first![/color]'
            return
        
        if self.result_label.text.startswith('[color=ff0000]'):  # Wrong answer
            self.show_final_result()
            return
        
        self.current_question += 1
        self.load_question()

    def quit_game(self, instance):
        if self.current_question > 0:
            self.money = levels[self.current_question - 1]
        self.show_final_result()

    def show_final_result(self):
        content = BoxLayout(orientation='vertical', padding=10, spacing=10)
        content.add_widget(Label(text=f'[b]Game Over![/b]\n\nYour Prize: Rs. {self.money:,}', markup=True, size_hint_y=0.8))
        
        btn = Button(text='Restart', size_hint_y=0.2, background_color=(0.2, 0.6, 1, 1))
        content.add_widget(btn)
        
        popup = Popup(title='Quiz Result', content=content, size_hint=(0.9, 0.6))
        btn.bind(on_press=self.restart_game)
        btn.bind(on_press=popup.dismiss)
        popup.open()

    def restart_game(self, instance):
        self.current_question = 0
        self.money = 0
        self.load_question()

if __name__ == '__main__':
    QuizApp().run()
