class WordChainBot:
    def __init__(self):
        self.words = [] # 存储已经使用过的词语

    def start_game(self):
        print("Welcome to the Word Chain Game! Please enter a word to start the game:")
        while True:
            user_input = input("Please enter the word (enter 'exit' to end the game):")
            if user_input.lower() == 'exit':
                print("The game is over, thank you for participating!")
                break
            if not self.check_word_valid(user_input):
                print("The input is not a valid word, please re-enter.")
                continue
            if not self.check_word_chain(user_input):
                print("Failed to connect the chain! Please re-enter to connect the chain.")
                continue
            self.words.append(user_input)
            print(f"Successfully connected! Current word chain:{' -> '.join(self.words)}")

    def check_word_valid(self, word):
        # 这里可以根据具体的成语库或规则进行检查
        # 简单起见，这里假设任何非空字符串都是有效的词语
        return len(word) > 0

    def check_word_chain(self, word):
        # 检查输入词语是否符合接龙规则
        if len(self.words) == 0:
            return True # 第一个词语，直接通过
        last_word = self.words[-1]
        return last_word[-1] == word[0]

# 创建词语接龙机器人实例
word_bot = WordChainBot()
# 开始游戏
word_bot.start_game()
