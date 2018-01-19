import sqlite3
from pprint import pprint
from random import randint, shuffle

from django.shortcuts import render
from django.views import View

intrebari = []
raspunsuri = []
variante_rasp = []
raspunsuri_test2 = []
DB_PATH = ".\\db.sqlite3"


def intrebare():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    i = 0
    while i < 10:
        '''
            type = 1 -> va fi formulata o intrebare la care raspunsul va fi "Adevarat"
            type = 2,3,4 -> va fi formulata o intrebare la care raspunsul va fi "Fals"
        '''
        type = randint(1, 4)
        if type == 1:
            c.execute("SELECT * FROM generator_ontologie ORDER BY RANDOM() LIMIT 1")
            row = c.fetchone()
            #print(row)
            question = row[1][0].upper() + row[1][1:] + " " + row[3] + " " + row[2] + "?"
            '''
            while question in intrebari:  # daca intrebarea exista deja in fisier vom crea alta
                c.execute("SELECT * FROM generator_ontologie ORDER BY RANDOM() LIMIT 1")
                row = c.fetchone()
                question = row[1][0].upper() + row[1][1:] + " " + row[3] + " " + row[2] + "?"
            '''
            intrebari.append(question)
            raspunsuri.append("adevarat")
            i += 1
        else:
            question = ""
            type2 = True
            try:
                c.execute("SELECT * FROM generator_ontologie ORDER BY RANDOM() LIMIT 1")
                row = c.fetchone()

                d = conn.cursor()
                d.execute("SELECT * FROM generator_ontologie where relatie=(?) and id !=(?) ", (row[3], row[0],))
                row2 = d.fetchall()
                #print(row2)

                #print("aaaaaaaa ", len(row2))

                # intrebarea nu poate fi facuta falsa, deci o facem adevarata
                if len(row2) == 0:
                    question = row[1][0].upper() + row[1][1:] + " " + row[3] + " " + row[2] + "?"
                    type2 = False
                else:
                    care_parinte = randint(0, len(row2)-1)
                    question = row[1][0].upper() + row[1][1:] + " " + row[3] + " " + row2[care_parinte][2] + "?"

            except Exception as error:
                pass
            '''
                In unele cazuri e posibil sa nu aiba o intrebare, nu-i problema, tratam exceptia cu un simplu pass si va incerca din nou
            '''

            while question in intrebari or len(question) == 0:  # daca intrebarea exista deja in fisier vom crea alta
                try:
                    c.execute("SELECT * FROM generator_ontologie ORDER BY RANDOM() LIMIT 1")
                    row = c.fetchone()

                    d = conn.cursor()
                    d.execute("SELECT * FROM generator_ontologie where relatie=(?) and id !=(?) ", (row[3], row[0],))
                    row2 = d.fetchall()
                    # print(row2)

                    # print("aaaaaaaa ", len(row2))
                    # intrebarea nu poate fi facuta falsa, deci o facem adevarata
                    if len(row2) == 0:
                        question = row[1][0].upper() + row[1][1:] + " " + row[3] + " " + row[2] + "?"
                        type2 = False
                    else:
                        care_parinte = randint(0, len(row2) - 1)
                        question = row[1][0].upper() + row[1][1:] + " " + row[3] + " " + row2[care_parinte][2] + "?"
                except Exception as error:
                    pass
            intrebari.append(question)
            if not type2:
                raspunsuri.append("adevarat")
            else:
                raspunsuri.append("fals")
            i += 1
    '''
    while i < 15:
        variante_raspuns = []
        c.execute("SELECT * FROM generator_ontologie ORDER BY RANDOM() LIMIT 1")
        random_row = c.fetchone()
        parinte = random_row[2]
        question = "Care din urmatoarele sunt " + parinte + "?"
        try:
            d = conn.cursor()
            d.execute("SELECT * FROM generator_ontologie where termen=(?)", (parinte,))
            bunic = d.fetchone()

            c.execute("SELECT * FROM generator_ontologie where parinte=(?) and not termen=(?)", (bunic[2], bunic[1]))
            frati = c.fetchall()
            shuffle(frati)
        except Exception as error:
            pass
        else:
            i += 1
            intrebari.append(question)


            nr_variante = 4
            variante_corecte = randint(1, 3)
            c.execute("SELECT * FROM generator_ontologie where parinte=(?)", (parinte,))
            rasp_corect = c.fetchmany(variante_corecte)
                # pprint(data)
            for j in rasp_corect:
                  variante_raspuns.append(j[1])

            variante_aditionale = nr_variante - variante_corecte
            iteratie = 0
            while variante_aditionale > 0:
                nr_variante = randint(1, variante_aditionale)
                try:
                    c.execute("SELECT * FROM generator_ontologie where parinte=(?)", (frati[iteratie][1],))
                    data = c.fetchmany(nr_variante)
                    for j in data:
                         variante_raspuns.append(j[1])
                         variante_aditionale -= 1
                except Exception as error:
                    pass
                iteratie += 1
            shuffle(variante_raspuns)
            litere = ["a", "b", "c", "d"]

            variante_rasp.append(variante_raspuns[0])
            variante_rasp.append(variante_raspuns[1])
            variante_rasp.append(variante_raspuns[2])
            variante_rasp.append(variante_raspuns[3])

            answer = ""
            for j in range(0, len(rasp_corect)):
                for x in range(0, len(variante_raspuns)):
                      if variante_raspuns[x] == rasp_corect[j][1]:
                         answer += litere[x] + " "
            raspunsuri_test2.append(answer)
    '''
    c.close()

intrebare()
print("intrebari")

for i in range(0, len(intrebari)):
    intrebari[i] = str(i + 1) + ". " + intrebari[i]

pprint(intrebari)
pprint(raspunsuri)
points = 0
question_number = 0


class Test(View):
    template_test1 = 'generator/index.html'
    template_test2 = 'generator/test2.html'
    finish_template = 'generator/finish.html'

    def get(self, request):
        try:
            print("aici")
            numbers = [i for i in range(1, 11)]
            context = {
                'index': numbers,
                'intrebari': intrebari[0],
            }
            intrebari.remove(intrebari[0])
            return render(request, self.template_test1, context)
        except Exception as error:
            pass

    def post(self, request):
        global points
        global question_number
        question_number += 1
        if question_number < 11:
            raspuns = request.POST.get('raspuns')
            try:
                if raspuns == raspunsuri[0]:
                    points += 1
                raspunsuri.remove(raspunsuri[0])
            except IndexError:
                pass
        else:
            try:
                a = request.POST.get('a')
                b = request.POST.get('b')
                c = request.POST.get('c')
                d = request.POST.get('d')
                punct = True
                if a == 'a':
                    if 'a' in raspunsuri_test2[0]:
                        raspunsuri_test2[0] = raspunsuri_test2[0].replace(a, "")
                    else:
                        punct = False
                if b == 'b':
                    if 'b' in raspunsuri_test2[0]:
                        raspunsuri_test2[0] = raspunsuri_test2[0].replace(b, "")
                    else:
                        punct = False
                if c == 'c':
                    if 'c' in raspunsuri_test2[0]:
                        raspunsuri_test2[0] = raspunsuri_test2[0].replace(c, "")
                    else:
                        punct = False
                if d == 'd':
                    if 'd' in raspunsuri_test2[0]:
                        raspunsuri_test2[0] = raspunsuri_test2[0].replace(d, "")
                    else:
                        punct = False
                for i in raspunsuri_test2[0]:
                    if i != ' ':
                        punct = False

                if punct:
                    points += 1
                raspunsuri_test2.remove(raspunsuri_test2[0])
            except Exception as error:
                pass
        try:
            context = {
                'intrebari': intrebari[0],
            }
            intrebari.remove(intrebari[0])
            if question_number < 10:
                return render(request, self.template_test1, context)
            else:
                for i in range(1, 5):
                    variante_rasp.remove(variante_rasp[0])
                return render(request, self.template_test2, context)
        except Exception as error:
            context = {
                'points': points,
            }
            return render(request, self.finish_template, context)
