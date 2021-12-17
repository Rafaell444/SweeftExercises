import time

grid = ['.......', '...O...', '....O..', '.......', 'OO.....', 'OO.....']

n = input("input sec num: ")
time.sleep(int(n))
print("")
print("Bomberman Placed the Bombs")
print(" ")
[print(lines) for lines in grid]  # გამომაქვს თავდაპირველი გრიდი
print(" ")
print("grid has been replaced")
print(" ")
time.sleep(1)

for line in grid:  # წერტილს ვანაცვლებ 0იანით რომ გრიდი შეივსოს

    print(str(line).replace(".", "O"))

    for each in line:
        if each == ".":
            line.replace(each, "0")
print(" ")
time.sleep(1)

for each_line in grid:  # ვპოულობ თავდაპირველად დადებული ბომბის ინდექსს
    print(list(each_line))
    my_dict = dict(enumerate(each_line))


    for key, value in my_dict.items():  # ბომბის აფეთქების დროს გვერდებში ვაფეთქებ 2 უჯრას
        if value == "O":
            if (key - 1 or key - 2) < 0:  # გამოთვლის დროს თუ რიცხვი უარყოფითი გახდა ანუ ნულს გადაცდა და გვერდით არ აქვს უკრა ასერომ ვჩერდებით
                break
            elif (key - 1 and key - 2) == 0:  # თუ ნულს უდრის ორივე გამოთვლილი მაშინ გამოგვაქვს ნული და ბომბის მახლობელი უჯრები
                print(0, key, key + 1, key + 2)
            else:  # ყველა სხვა შემთხვევაში ითვლება გვერდითა ორი უჯრების ინდექსები
                print(key + 1, key + 2, key - 1, key - 2)




                # შეცდომა-რატომღაც ვერ მითვლის ბოლო ლისტში ბომბის გვერდით უჯრების რაოდენობას








                # 1
                #
                # .......
                # ...
                # O...
                # ....O..
                # .......
                # OO.....
                # OO.....
                #
                # OOOOOOO
                # OOOOOOO
                # OOOOOOO
                # OOOOOOO
                # OOOOOOO
                # OOOOOOO
                # ['.', '.', '.', '.', '.', '.', '.']
                # ['.', '.', '.', 'O', '.', '.', '.']
                # 4
                # 5
                # 2
                # 1
                # ['.', '.', '.', '.', 'O', '.', '.']
                # 5
                # 6
                # 3
                # 2
                # ['.', '.', '.', '.', '.', '.', '.']
                # ['O', 'O', '.', '.', '.', '.', '.']
                # ['O', 'O', '.', '.', '.', '.', '.']
