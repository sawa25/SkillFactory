from operator import itemgetter
def iswin(l_,razmernost):

    isis=False
    while True:#группа проверок на выигрыш по строке, столбцу или диагонали
        for direction in [[0,1],[1,0]]:#по строке или по столбцу
            #предварительная сортировка пар индексов, чтобы индексы выигрышной строки или столбца втали подряд среди всех пар заполненных ячеек
            l_ = sorted(l_, key=itemgetter(direction[1], direction[0]))
            if len(l_)<razmernost: #если нет минимального количества ходов, то не проверять выигрыш
                continue
            #print(direction,l_)
            count_rowORcol=1 #счетчик количества ячеек, удовлетворяющих условию выигрыша(должно быть равно размерности)
            #индексы предыдущей ячейки
            itemprev_ind=l_[0][direction[0]]
            itemprev_Alt_ind = l_[0][direction[1]]
            result=[l_[0]]#набирать список ячеек выигрышной линии, сразу внести первый элемент
            for item in l_[1:]:
                #индексы выигрышной строки или столбца ожидаются встретиться в общем списке подряд
                if item[direction[0]]-itemprev_ind==1 and item[direction[1]]==itemprev_Alt_ind:
                    count_rowORcol+=1 #считать, сколько подряд есть занятых ячеек с одинаковым столбцом или строкой
                    result.append(item)#очередная ячейка в том же столбце или в той же строке-забрать в набор
                    if count_rowORcol == razmernost:  # если заполнена целая строка или столбец, значит -выигрыш
                        isis = True
                        break
                else:#подряд встретилась ячейка с неудовлетворительным условием(не в той же строке или не в том же столбце)
                    count_rowORcol=1 #сбросить счетчик и начать снова наблюдение
                    result = [item]
                # индексы предыдущей ячейки
                itemprev_ind=item[direction[0]]
                itemprev_Alt_ind = item[direction[1]]
            if isis:
                break
        if isis:
            break

        #выигрыш по диагонали из левого верхнего в правый нижний угол -условие равенства одного и другого индекса,
        #выигрыш по диагонали из левого нижнего в правый верхний угол -равенство одного и инвертированного другого индекса
        funcs=[lambda item: item[0] == item[1],lambda item: item[0] == razmernost - item[1] + 1]
        for func in funcs:
            result = list(filter(func, l_)) #выбрать только индексы по условию
            if len(result) == razmernost:#если заполнена вся диагональ - значит выигрыш
                result.sort(key=itemgetter(1, 0))
                isis = True
                break

        break #выход из бесконечного while

    if isis:
        pass
        #print("выигрыш", result)
    return  isis

# razmernost=4
#
#
# l_kr=[[2,1],[2,2],[2,3],[1,2],[2,4]]
# print("исх", l_kr)
# iswin(l_kr,razmernost)
#
# l_kr=[[3,3],[1,3],[3,2],[2,3],[4,3]]
# print("исх", l_kr)
# iswin(l_kr,razmernost)
#
# l_kr=[[1,3],[2,1],[3,3],[2,2],[1,1],[4,4]]
# print("исх", l_kr)
# iswin(l_kr,razmernost)
#
# l_kr=[[4,1],[3,2],[2,3],[1,4],[3,1]]
# print("исх", l_kr)
# iswin(l_kr,razmernost)
