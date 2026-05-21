import random

class BaseQuestion:
    def __init__(self, hint: str, answer: str, choices: list[str]) -> None:
        self.hint: str = hint
        self.answer: str = answer
        self.choices: list[str] = choices
    
    def display_quiz(self) -> None:
        pass

    def check_answer(self, player_input: str) -> bool:
        return player_input.replace(" ", "") == self.answer.replace(" ", "")

# Text Mode
class TextProverQuestion(BaseQuestion):
    def __init__(self, hint: str, answer: str, blank: str, choices: list[str]) -> None:
        super().__init__(hint, answer, choices)
        self.blank: str = blank

    def display_quiz(self) -> None:
        print("กรุณาพิมพ์คำศัพท์ที่ถูกต้อง")
        print(f"คำใบ้: {self.hint}")
        print(f"โจทย์: {self.blank}")
        shuffled = self.choices.copy()
        random.shuffle(shuffled)
        print("คลังคำศัพท์:", " ".join(shuffled))
        print("-" * 30)

# Choice Mode 1-4
class ChoiceProverbQuestion(BaseQuestion):
    def display_quiz(self) -> None:
        print("กรุณาเลือกคำตอบที่ถูกต้อง")
        print(f"คำใบ้: {self.hint}")
        print("โจทย์: สำนวนใดตรงกับคำใบ้ด้านบน?")

        for idx, choice in enumerate(self.choices):
            print(f" {idx + 1}. {choice}")
        print("-" * 30)

    def check_answer(self, player_input: str) -> bool:
        try:
            choice_index = int(player_input) - 1
            selected_choice = self.choices[choice_index].replace(" ", "")
            correct_answer = self.answer.replace(" ", "")
            return selected_choice == correct_answer
        except:
            return False
    
class ProverbGame:
    def __init__(self, question_list: list[BaseQuestion]) -> None:
        self.lives: int = 3
        self.score: int = 0
        self.questions: list[BaseQuestion] = question_list

    def start(self) -> None:
        print("-" * 45)
        print("ยินดีต้อนรับสู่เกมทายสำนวนไทย")
        print("-" * 45)

        for i, question in enumerate(self.questions):
            print(f"\nข้อที่ {i+1}/{len(self.questions)}")
            question.display_quiz()

            if isinstance(question, TextProverQuestion):
                num_blanks = question.blank.count("...")
                selected = [input(f"ตอบช่องที่ {slot+1}: ").strip() for slot in range(num_blanks)]

                full_ans = question.blank
                for word in selected:
                    full_ans = full_ans.replace("...", word, 1)
                user_input = full_ans
            else:
                user_input = input("เลือกข้อที่ถูกต้อง (1-4): ").strip()

            if question.check_answer(user_input):
                print("✅ ถูกต้อง! +10 คะแนน")
                self.score += 10
            else:
                self.lives -= 1
                print(f"❌ ผิด! คำตอบคือ: {question.answer}")
                print(f"❤️ ชีวิตที่เหลือ: {self.lives}")
            
            if self.lives == 0:
                print("\n💀 หมดชีวิตแล้ว! Game Over!")
                break
    
        print(f"\n🏆 จบเกม! คะแนนสุดท้ายของคุณคือ: {self.score} คะแนน")

from game_data_nw1t import raw_questions

list_of_questions: list[BaseQuestion] = []
for q in raw_questions:
    if q["type"] == "text":
        obj = TextProverQuestion(q["hint"], q["answer"], q["blank"], q["choices"])
    elif q["type"] == "choice":
        obj = ChoiceProverbQuestion(q["hint"], q["answer"], q["choices"])
    list_of_questions.append(obj)

game = ProverbGame(list_of_questions)
game.start()