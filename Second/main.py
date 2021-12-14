# გამოვიყენე ლექსოგრაფიული ალგორითმის ახნის რესურსი -
# https://www.quora.com/How-would-you-explain-an-algorithm-that-generates-permutations-using-lexicographic-ordering

n = int(input())  # პირველ რიგში ვიღებთ მნიშვნელობებს
for _ in range(n):
    a = input()
    counter = 0
    for word in range(len(a) - 1, 0, -1): #ვკითხულობთ სიტყვას მარჯვნიდან მარცხნივ
        if a[word - 1] < a[word]: #თუ წინა რიცხვი ნაკლებია მომდევნოზე,ვწყვეტთ გამოთვლას და გამოვყოფთ ამოხსნას რიცხვში 1იანის დამატებით
            counter += 1
            break
    if not counter:   #იმ შემთხვევაში თუ წინა რიცხვი მომდევნოზე ნაკლები არ აღმოჩნდა მაშინ გამოდის რომ ამ რიცხვზე მეტი (ლექსოგრაფიულად დაჯგუფებული რიცხვი) არ არსებობს
        print("no answer")
    else:
        k = word - 1 #მესამე შემთხვევაში როდესაც წინა მეტია მომდევნოზე ვითვლით დაახლობით იგივე ფორმულით რათა გავარკვიოთ უკვე მომდევნო მეტი არის თუ არა მომდევნოზე
        for each in range(len(a) - 1, k, -1):
            if a[each] > a[k]:
                counter2 = each
                break

