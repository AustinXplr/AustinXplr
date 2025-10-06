import nltk
import json
from nltk.chat.util import Chat, reflections

# 读取聊天机器人的响应规则从 JSON 文件
def load_chat_pairs(filename='The_path_to_the_folder/Chat Python/Chat Python training files/chat_pairs.json'):
    with open(filename, 'r', encoding='utf-8') as file:
        data = json.load(file)
        pairs = []
        
        for item in data['pairs']:
            patterns = item.get('patterns', [])
            responses = item.get('responses', [])
            
            for pattern in patterns:
                pairs.append((pattern, responses))  # 创建 (模式, 响应) 的元组
        
        return pairs

# 创建聊天机器人
def chatbot():
    # 加载聊天对话语料
    pairs = load_chat_pairs()

    print("   @@@@@@@@@@@@@@@@@    ")
    print("@                                                                        @")
    print("@                                                                        @")
    print("@            @@@@@@@@@@                 @")
    print("@        @                                       @                 @")
    print("@        @                                       @                 @")
    print("@        @                                       @                 @")
    print("@        @                                       @                 @")
    print("@        @                                       @                 @")
    print("@        @                                       @                 @")
    print("@        @                                        @                @")
    print("@         @@@@@@@@@@@@@@@@")
    print("")
    print("Chat Python")
    print('Hello! I am Chat Python the ChatBot. Enter "quit" to exit Chat Python. ')
    chat = Chat(pairs, reflections)  # 这里使用处理后的 pairs 变量
    username = input("Please enter your username first: ")
    
    while True:
        user_input = input(f"{username}: ")  # 使用格式化字符串传递用户名作为提示信息
        if user_input == "quit":
            break
        
        response = chat.respond(user_input)
        print("Chat Python: ", response)

if __name__ == "__main__":
    chatbot()
