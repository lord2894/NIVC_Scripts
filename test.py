
def main():
    input = open("C:\\Users\\Kir\\Desktop\\text.txt","r", encoding="windows-1251")
    content = input.read()
    input.close()

    output = open("C:\\Users\\Kir\\Desktop\\text2.txt","w", encoding="utf-8")
    output.write(content)
    output.close()

if __name__ == "__main__":
    main()