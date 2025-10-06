print("任意进制数字互化小工具 by 李晨榕")
def convert_base(number, from_base, to_base):
    if not 2 <= from_base <= 36 or not 2 <= to_base <= 36:
        raise ValueError("进制必须在2到36之间")

    if isinstance(number, str):
        number = int(number, from_base)
    elif not isinstance(number, int):
        raise ValueError("输入数字必须是整数或字符串")

    if number == 0:
        return "0" if to_base == 10 else "0"

    alphabet = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    result = ""
    negative = number < 0
    number = abs(number)

    while number > 0:
        remainder = number % to_base
        result = alphabet[remainder] + result
        number = number // to_base

    if negative:
        result = "-" + result

    return result

def main():
    while True:
        try:
            input_number = input("请输入要转换的数字：")
            from_base = int(input("请输入原始进制（2-36）："))
            to_base = int(input("请输入目标进制（2-36）："))

            converted_number = convert_base(input_number, from_base, to_base)
            print(f"转换结果为：{converted_number}")
            
            choice = input("是否退出程序？(Y/N): ")
            if choice.lower() == "Y":
                break
        except ValueError as ve:
            print(f"错误：{ve}")

if __name__ == "__main__":
    main()
