from funcs2 import iswin
def addr(aa,razmernost):#получить адреса клеток игрового поля в формате буква=столбец, цифра=строка
    bb = [str(i) for i in range(1, razmernost + 1)]
    qq = []
    for i in bb:
        for j in aa:
            qq.append(j + i)
    return qq

def gener(addr,razmernost):#для печати:получать отдельно по строкам массив игрового поля
    count = 0
    tmpaddr=addr
    while tmpaddr:
        yield tmpaddr[0:razmernost]
        yield from gener(tmpaddr[razmernost:],razmernost)
        break
def s_cellsfromdict(l_addr,d_cells):#для печати:заполнить строку-игровое поле пустыми или занятыми ячейками
    s=""
    for i in l_addr:
        tmp_cell=d_cells.get(i)
        s=s+ (tmp_cell if tmp_cell else "-")
    return s

# d_cells["C3"]="O" #выполнить чей-то ход-запомнить изменение на игровом поле
# d_cells["C1"]="O" #выполнить чей-то ход-запомнить изменение на игровом поле
# print("словарь адресов и значений ячеек игрового поля",d_cells)

def indind(l_togrow,celladdr,s_col_indexes):#для буквенноцифровой координаты celladdr получить список из двух индексов(1-базированных):
    # номер строки, номер столбца
    tmp=[]
    tmp.append(int(celladdr[1]))
    tmp.append(int(s_col_indexes.find(celladdr[0])+1))
    l_togrow.append(tmp)
    return tmp
#print("индексы одной из занятых ячеек на поле",indind("C2"))

def krestikiORnoliki(d_cells,charXO):#вернуть адреса , занятые крестиками или ноликами
    tmp=list({k: v for k,v in d_cells.items() if v[0] == charXO}.keys())
    #print("tmp",tmp)
    return tmp
# print("noliki",noliki())
# print("krestiki",krestiki())



def printfield(d_cells,razmernost,s_col_indexes,l_addr):#вывести актуальное изображение игрового хода со сделанными ходами
    s = s_cellsfromdict(l_addr,d_cells)
    l_row_indexes = [i for i in range(1, razmernost + 1)]
    #print("индексы столбцов", l_row_indexes)
    print("********"*10)
    print("   {0}".format(s_col_indexes))
    for i in map(lambda ii,a,b:"{0}  {1}  {2}".format(ii,a,"".join(b)),l_row_indexes,gener(s,razmernost),gener(l_addr,razmernost)):
        print(i)

def CellIsPossibleToWin(emptycells,num_cellsXorO,s_col_indexes,razmernost):#?есть ли ход, приводящий к выигрышу
    # перебрать все свободные клетки, добавляя к существующему набору одного из игроков еще ход
    # и проверить на выигрыш
    for Addr in emptycells:
        Ind = indind(num_cellsXorO, Addr, s_col_indexes)  # пополнить список индексов виртуальным следующим ходом
        IsWin = iswin(num_cellsXorO, razmernost)  # проверить на выигрыш
        num_cellsXorO.remove(Ind)  # вернуть список к первоначальному виду
        if IsWin:
            return Addr
    return None

def doubleMove(virtualCell,emptycells_deep,num_cellsXorO,s_col_indexes,razmernost,goalForself):
    #два варианта использования этой функции:
    # для очередного своего хода найти "двойной" ход goalForself=True
    # или проверить,
    # что после очередного своего хода не существует "двойного" хода противника goalForself=False
    IsExist=None #такая клетка есть или нет?
    for Addr_deep in ([virtualCell] if virtualCell else emptycells_deep):  # для оставшихся клеток проанализировать:
        Ind_deep = indind(num_cellsXorO, Addr_deep, s_col_indexes)
        # если после этого хода появляется сразу две клетки, любая из которых приводит к выигрышу игрока
        countwins = 0
        copynum_cellsXO1 = num_cellsXorO.copy()
        for Addr_deep2 in emptycells_deep:
            if Addr_deep2 == Addr_deep:
                continue  # просто пропустить эту клетку, (из-за одной этой клетки не модифицировать исходный список)
            Ind_deep2 = indind(copynum_cellsXO1, Addr_deep2, s_col_indexes)
            countwins += 1 if iswin(copynum_cellsXO1, razmernost) else 0
            if countwins > 1:
                IsExist=Addr_deep #есть двойной ход
                break
            else:  #убрать и проверять далее все варианты
                copynum_cellsXO1.remove(Ind_deep2)
        num_cellsXorO.remove(Ind_deep)
        if goalForself and IsExist:
            return IsExist #найден двойной ход для себя
        if not goalForself and IsExist:
            return IsExist  # проверено, что противник может сделать двойной ход
    if IsExist: print("такого не может быть")
    return IsExist  #двойного хода не предвидится
