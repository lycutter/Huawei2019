list1 = [1, 2, 3, 4, 5, 6, 7]
for listInstance in list1:
    if listInstance % 2 == 0:
        list1.remove(listInstance)
print(list1)