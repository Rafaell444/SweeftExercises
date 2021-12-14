# გამოვიყენე ლექსოგრაფიული ალგორითმის ახნის რესურსი -
# https://www.quora.com/How-would-you-explain-an-algorithm-that-generates-permutations-using-lexicographic-ordering


def bigger_is_greater(n):  # პირველ რიგში ვიღებთ მნიშვნელობებს
    for _ in range(n):
        a = input()
        counter = 0
        for word in range(len(a) - 1, 0, -1):  # ვკითხულობთ სიტყვას მარჯვნიდან მარცხნივ
            if a[word - 1] < a[
                word]:  # თუ წინა რიცხვი ნაკლებია მომდევნოზე,ვწყვეტთ გამოთვლას და გამოვყოფთ ამოხსნას რიცხვში 1იანის დამატებით
                counter += 1
                break
        if not counter:  # იმ შემთხვევაში თუ წინა რიცხვი მომდევნოზე ნაკლები არ აღმოჩნდა მაშინ გამოდის რომ ამ რიცხვზე მეტი (ლექსოგრაფიულად დაჯგუფებული რიცხვი) არ არსებობს
            print("no answer")
        else:
            k = word - 1  # მესამე შემთხვევაში როდესაც წინა მეტია მომდევნოზე ვითვლით დაახლობით იგივე ფორმულით რათა გავარკვიოთ უკვე მომდევნო მეტი არის თუ არა მომდევნოზე
            for each in range(len(a) - 1, k, -1):
                if a[each] > a[k]:
                    counter2 = each
                    break

            a_array = list(a)

            x = a_array[k]

            a_array[k] = a_array[counter2]
            a_array[counter2] = x

            first = a_array[0:k + 1]
            second = a_array[k + 1:]

            temp = ""

            for each2 in range(len(first)):
                temp += first[each2]
            for each3 in range(len(second)):
                temp += second[each3]

            print(temp)


print(bigger_is_greater(int(input())))

