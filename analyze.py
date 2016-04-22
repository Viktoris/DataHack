import csv
import xlsxwriter
from PIL import Image, ImageDraw
import sys


class Clovek:
    def __init__(self,meno,id,x,y,time):
        self.id = id
        self.meno = meno
        self.time = []
        self.x = []
        self.y = []
        self.x.append(int(x))
        self.y.append(int(y))
        self.time.append(int(time))

def create_workbook(str,vysledok):

    workbook = xlsxwriter.Workbook(str)
    worksheet = workbook.add_worksheet()

    worksheet.write(0, 1, 'cas')
    worksheet.write(0, 2, 'bod x')
    worksheet.write(0, 3, 'bod y')

    print(len(vysledok.x))
    for i in range(1,300,1):
       # worksheet.write(i, 1, vysledok.time[i])
        worksheet.write(i, 2, vysledok.x[i])
        worksheet.write(i, 3, vysledok.y[i])

    workbook.close()


def open_file(str):
    f = open(str, 'rt')
    reader = csv.reader(f,delimiter=';')
    ludia = {}
    count_ludi = -1

    for row in reader:

        #print(row[2])
        if(row[2] != 'GazePointIndex' and int(row[2]) == 1):
            count_ludi += 1
            ludia[count_ludi] = Clovek(row[0],count_ludi,row[3],row[4],row[1])
        else:
            if(count_ludi == -1):
                continue
            id = row[2]
            #print(id)
            if(row[3] == '' or row[4] == ''):
                ludia[count_ludi].x.append(row[3])
                ludia[count_ludi].y.append(row[4])
            else:
                ludia[count_ludi].x.append(int(row[3]))
                ludia[count_ludi].y.append(int(row[4]))
                ludia[count_ludi].time.append(int(row[1]))



    return ludia

'''
vypocita data, ktore nie su dostupne
prida k nimi krok - rozdistribuuje rozdiel najblizsich dostupnych pohladov medzi chybajuce data
'''
def fix_data(ludia):
    pred_x = 0
    za_x = 0
    pred_y = 0
    za_y = 0

    prvy_id = 0
    posledny_id = 0
    pocet = 0

    for id in ludia:
        for i in range(0,len(ludia[id].x),1):

            if(ludia[id].x[i] == ''):
                pred_y = ludia[id].y[i - 1]
                pred_x = ludia[id].x[i-1]
                pred_id = i

                while(ludia[id].x[i] == ''):
                    pocet += 1
                    i +=1

                za_x = ludia[id].x[i]
                za_y = ludia[id].y[i]
                posledny_id = i-1

                if(pocet == 0):
                    pocet = 1

                krokx = abs(int((pred_x-za_x)/ pocet))
                kroky = abs(int((pred_y - za_y) / pocet))
                for j in range(pred_id,posledny_id+1,1):
                    ludia[id].x[j] = ludia[id].x[j-1] + krokx
                    ludia[id].y[j] = ludia[id].y[j - 1] + kroky



    return ludia

def vyrataj_priemer(ludia):
    vysledok = Clovek('priemer',0,0,0,0)
    pocet_ludi = 11
    sumx = 0
    sumy = 0

    #print(len(ludia[0].time))

    for i in range(0,280,1):
        for id in ludia:
            sumx += int(ludia[id].x[i])
            sumy += int(ludia[id].y[i])

        vysledok.x.append(int(sumx / pocet_ludi))
        vysledok.y.append(int(sumy / pocet_ludi))
        sumx = 0
        sumy = 0

    return vysledok


def nakresli(vysledok):
    body = []
    offsetx = (1920-1366)/2
    offsety = (1200-768)/2

    for i in range(1, 280, 1):
        body.append((vysledok.x[i] - offsetx, vysledok.y[i] - offsety))

    im = Image.open("focused tab - first.jpg")

    draw = ImageDraw.Draw(im)
   # draw.line(body, fill=128)
    for i in range(1,30,1):
        draw.ellipse((body[i][0]-20,body[i][1]-20,body[i][0]+20,body[i][1]+20),fill=(255,255,255,128),outline='blue')

    del draw

    # write to stdout
    im.save('focused_first_marian', 'png')


ludia = {}
ludia = open_file('focused_first_sMarianom.csv')
ludia = fix_data(ludia)
vysledok = vyrataj_priemer(ludia)

print(vysledok.x[0], vysledok.y[0])
#nakresli(vysledok)

#workbook = create_workbook('vysledky_focused.xlsx',vysledok)


