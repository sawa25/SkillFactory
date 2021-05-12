from funcs1 import *
from funcs2 import *
import random

#сценарий ответов на вопросы ввода от пользователя- может быть пустым или содержать список значений
# в порядке: размерность игры <3,4,5.....>, кто ходит первый<0 или 1>, координаты,координаты,....
#сценарий имеет смысл только если отключена ржндомизация и включена сортировка списка emptycells
#inputlist=[3,'0','a1','c2'] #проигрыш игрока из-за ошибочного хода
inputlist=[]
def Inputs(wellcome):
    if len(inputlist)>0:
        return inputlist.pop(0)
    else:
        return input(wellcome)
razmernost=3 #размерность игрового поля (ширина=высота=razmernost)
def igra(razmernost):
    IsContinue="Y"
    while IsContinue.upper()=="Y":
        d_cells = {}  # словарь ключ-адрес(буквацифра),значение=None,"X" или "O"
        num_cellsXO=[[],[]] #список списков цифровых индексов крестиков,ноликов
        num_cellsO = []  # список цифровых индексов ноликов
        s_col_indexes = "ABCDEFGH"[:razmernost]
        l_addr = addr(s_col_indexes, razmernost)  # все возможные адреса клеток игрового поля
        #print("список адресов всех ячеек игрового поля", l_addr)
        # razmernost=len(s_col_indexes)
        # вывод игрового поля
        printfield(d_cells,razmernost,s_col_indexes,l_addr)
        # кто делает первый ход?
        IsHumanMove=True
        print('Первый всегда играет за крестики.Сделайте выбор:')
        IsHumanMove=Inputs("Первый ход делает человек(1) или компьютер(0) ?")=="1"
        if IsHumanMove:#определение символов для игроков
            CompHuman="OX"
        else:
            CompHuman = "XO"
        theWinner=""
        while True:
            ABCNNN=""
            emptycells = list(set(l_addr).difference(set(d_cells.keys())))  # свободные клетки для следующего хода
            random.shuffle(emptycells)
            # emptycells.sort()
            # emptycells.reverse()
            if len(emptycells) == 0:
                print("все клетки заняты, а никто так и не выиграл")
                break
            if IsHumanMove:
                ABCNNN=Inputs("Человек вводит координаты клетки для очередного хода: (или 'Q' для прерывания текущей игры):")
                ABCNNN=ABCNNN.upper()
                if ABCNNN=="Q":
                    print("Преждевременный выход по желанию игрока. Игра прервана.")
                    break
                if not (ABCNNN in l_addr):
                    print("Неверный ввод.Требуется координата в формате <БукваЦифра>")
                    continue
                if ABCNNN in d_cells:
                    print(f"Неверный ввод.Клетка {ABCNNN} уже занята")
                    continue
                d_cells[ABCNNN] = CompHuman[1]  # выполнить ход-запомнить изменение на игровом поле
                indind(num_cellsXO[1],ABCNNN,s_col_indexes)
                #print("список индексов",num_cellsXO)
            else: #играет компьютер
                IsFoundCell = None  # None или адрес клетки для очередного хода
                #для себя проверка, можно ли выиграть следующим ходом?
                IsPossibleToWin=False
                nowcount=list(d_cells.values()).count(CompHuman[0]) # число сделанных ходов компьютера
                if nowcount>=razmernost-1: #для выигрыша должно быть уже сделано минимально возможное число ходов
                    IsFoundCell=CellIsPossibleToWin(emptycells, num_cellsXO[0], s_col_indexes, razmernost)
                    if IsFoundCell:
                        indind(num_cellsXO[0],IsFoundCell,s_col_indexes)  # сделать ход, ведущий к немедленному выигрышу
                if not IsFoundCell:
                    #если нельзя выиграть компьютеру, то для противника проверить,
                    # может ли он выиграть следующим ходом, чтобы не позволить это сделать
                    nowcount=list(d_cells.values()).count(CompHuman[1]) # число сделанных ходов игрока
                    if nowcount>=razmernost-1: #для выигрыша должно быть уже сделано минимально возможное число ходов
                        IsFoundCell = CellIsPossibleToWin(emptycells, num_cellsXO[1], s_col_indexes, razmernost)
                        if IsFoundCell:
                            # если игрок может выиграть следующим ходом, то сделать ход в эту позицию и
                            # предотвратить возможный выигрыш соперника
                            indind(num_cellsXO[0], IsFoundCell, s_col_indexes)
                if not IsFoundCell:
                    #если никто пока не может выиграть следующим ходом,
                    #выбрать оптимальный ход:
                    #проверить центр и занять, если центр пока свободен
                    rowrow=1+razmernost // 2
                    colcol=rowrow-1
                    newaddr=f"{s_col_indexes[colcol]}{rowrow}"
                    if not (newaddr in d_cells):
                        #сделать ход в центр поля, если не занято
                        #для четной размерности центра 4штуки, это не учитывается
                        IsFoundCell=newaddr
                        indind(num_cellsXO[0], newaddr, s_col_indexes)
                    else:#центр занят, искать другие клетки
                        IsFirstCompMove=len(krestikiORnoliki(d_cells,'X'))==len(krestikiORnoliki(d_cells,'O'))
                        # если первый ходил компьютер, то попытаться найти клетку, ход в которую
                        # обеспечивает двойной вариант, т.е. предотвратить выигрыш следующим ходом будет невозможно
                        if IsFirstCompMove:
                            IsFoundCell=doubleMove(None, emptycells, num_cellsXO[0], s_col_indexes, razmernost, goalForself=True)
                            if IsFoundCell: indind(num_cellsXO[0], IsFoundCell, s_col_indexes)
                        if (IsFirstCompMove and not IsFoundCell) or not IsFirstCompMove:
                            # если первым ходил игрок(или не нашлось оптимального хода
                            # для компьютера), то наоборот, предотвратить такой двойной вариант со стороны игрока
                            for Addr in emptycells:
                                #пробный ход компьютера
                                IsFoundCell = Addr
                                Ind = indind(num_cellsXO[0], Addr, s_col_indexes)
                                #возможные ходы игрока
                                #emptycells_deep = set(l_addr).difference(set(d_cells.keys()))  # свободные клетки для следующего хода
                                emptycells_deep=emptycells.copy()
                                emptycells_deep.remove(Addr) #убрать клетку, занятую только что компьютером
                                emptycells_deep.sort()
                                # сделать виртуальный ход за игрока:
                                # в первую очередь игрок будет делать ход, предотвращающий выигрыш компьютера
                                virtualCell = CellIsPossibleToWin(emptycells_deep, num_cellsXO[0], s_col_indexes, razmernost)
                                #если нет выигрышной клетки, перебрать все варианты для очередного хода игрока,
                                # если есть выигрышная клетка, то перебрать с учетом известного первого хода игрока
                                if doubleMove(virtualCell, emptycells_deep, num_cellsXO[1], s_col_indexes,
                                                         razmernost, goalForself=False):
                                    IsFoundCell=None
                                    # отменить данный ход компьютера, проверять другие ходы из возможных
                                    num_cellsXO[0].remove(Ind)
                                    continue
                                else:
                                    break #ход IsFoundCell относительно безопасен
                                #отменить виртуальный ход и сделать продолжить со следующим
                if IsFoundCell:
                    #найдена удовлетворительная клетка для хода, сделать ход
                    d_cells[IsFoundCell] = CompHuman[0]
                else:
                    print("такого быть наверно не может")

                #проверка выигрыша, кто только что ходил
            IsFinish=iswin(num_cellsXO[int(IsHumanMove)],razmernost)
            printfield(d_cells, razmernost, s_col_indexes, l_addr)
            if IsFinish:
                theWinner=CompHuman[int(IsHumanMove)]
                break
            IsHumanMove= not IsHumanMove #передать ход партнеру
        if theWinner:
            print(f"Победил '{theWinner}'" )
        IsContinue=input("Играть еще? Y/N")

if __name__ == '__main__':
    print('Начинается игра Крестики/Нолики:')
    razmernost=int(Inputs("Задайте размерность игрового поля<3,4,5 и т.д.>(размерность=ширина=высота):"))
    igra(razmernost)
