# citirea si initializarea dictionarului pentru productii

def read_productions(productions):
    f = open("input.txt")

    for line in f:
        mid = line.split("->")
        productions[mid[0].strip()] = [x.strip() for x in mid[1].split("|")]

    f.close()
    print('Start: ', productions)


#PASUL 1: eliminam productiile lambda

def lambda_production_removal(productions):

    ok = 1
    while ok:

        ok = 0
        current = None                  # current este membrul stang al productiei care contine lambda
        for i in productions:
            if "$" in productions[i]:
                current = i
                ok = 1
                break

        if current:
            #cazul 1: daca membrul stang nu mai are si alte productii
            if len(productions[current]) == 1:

                del productions[current]

                for i in productions:
                    if current in productions[i]:
                        if len(productions[i]) == 1:
                            productions[i].remove(current)
                            productions[i].push("$")
                        else:
                            for j in productions[i]:
                                j = j.replace(current, "")

            #cazul 2: daca membrul stang mai are si alte productii
            else:

                productions[current].remove("$")

                for i in productions:
                    for j in productions[i]:
                        if current in j:
                            nr = j.count(current)
                            for k in range(nr):
                                aux = ""
                                eliminat = False
                                copy = j
                                for chr in copy:
                                    if not eliminat:
                                        if chr == current:
                                            eliminat = True
                                            copy.replace(current, "", 1)
                                        else:
                                            aux += chr
                                    else:
                                        aux += chr
                                productions[i].append(aux)
                                productions[i] = list(set(productions[i]))

    #print('After step 1: ', productions)


#PASUL NR. 2: eliminim redenumirile


def renamed_production_removal(productions):

    for i in productions:
        if i in productions[i]:
            productions[i].remove(i)

    # A -> B si B -> expresie, devine A -> expresie
    ok = 1

    while ok:

        ok = 0
        for i in productions:
            for j in productions[i]:
                if len(j) == 1 and j.istitle():
                    ok = 1
                    productions[i].remove(j)
                    productions[i].extend(productions[j])

            productions[i] = list(set(productions[i]))  # elimin duplicatele

    #print('After step 2: ', productions)




#PASUL nr. 3: adaugarea de neterminale pentru terminalele din productii


def add_nonterminals_productions(chr, productions):

    terminal = []
    for i in productions:
        for j in productions[i]:
            l = False
            u = False
            aux = []
            if len(j) > 1:
                for k in j:
                    if k.islower():
                        l = True
                        aux.append(k)
                    else:
                        u = True
            if l and u:
                terminal.extend(aux)

    terminal = list(set(terminal))

    for ter in terminal:
        while chr in productions:                               # ma asigur ca nu exista deja litera in productii
            chr = chr(ord(chr) + 1)

        for i in productions:
            for j in range(len(productions[i])):
                if len(productions[i][j]) > 1:
                    productions[i][j] = productions[i][j].replace(ter, chr)

        productions[chr] = [ter]

    #print('After step 3: ', productions)



#PASUL NR. 4: modificarea productiilor cu mai mult de doua neterminale


def add_more_productions(next_letter, productions):

    done = False

    while not done:

        done = True
        non_terminal = ''
        for key in productions:
            for production in productions[key]:
                if len(production) > 2:
                    done = False
                    non_terminal = production[1:]
                    break
            if not done:
                break

        if done:
            break

        while next_letter in productions:
            next_letter = chr(ord(next_letter) + 1)

        for key in productions:
            for i in range(len(productions[key])):
                if len(productions[key][i]) > 2:
                    productions[key][i] = productions[key][i].replace(non_terminal, next_letter)
        productions[next_letter] = [non_terminal]
    print('Final: ', productions)


def transform(productions):
    lambda_production_removal(productions)
    renamed_production_removal(productions)
    letter = 'A'
    add_nonterminals_productions(letter, productions)
    add_more_productions(letter, productions)


productions = {}
read_productions(productions)

transform(productions)
