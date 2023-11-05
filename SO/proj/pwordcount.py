### Grupo: SO-TI-XX
### Aluno 1: Nome Apelido (fcXXXX)
### Aluno 2: Nome Apelido (fcXXXX)
### Aluno 3: Nome Apelido (fcXXXX)

import sys
import math
from time import perf_counter
from multiprocessing import Process


def getFilesList():
    '''
    Retorna uma lista de strings com os ficheiros dados como argumento
    
    Requires: pelo menos um dos argumentos passados tem de ser um ficheiro .txt,
            sob formato de string, o que é assegurado pela função verifyArgs()
    Ensures: retorno de uma lista de strings com o nome dos ficheiros passados como argumento 
    '''
    files_list = []
    
    c = 0
    while str(sys.argv[c])[-4:] != ".txt":  #índice do argumento do primeiro ficheiro que foi passado
        c += 1
    
    for x in sys.argv[c:]:
        files_list.append(x)
    
    return files_list


def lowerCasing(lines):
    '''
    Transforma letras maiúsculas em minúsculas
    
    Requires: words é uma lista de listas que contêm strings
    Ensures: não existe distinção entre palavras iguais que possam ter letras maiúsculas
    '''
    for line in lines:
        str(line).lower()
    
    return lines



def verifyArgs():
    '''
    Análise dos Argumentos 

    Requires: [-m t|u|o] [-p n] ficheiros…    
              O argumento deve ser idêntico ao exemplificado acima, explicitando qual o modo de utilização (-m), 
              opcionando entre (t, u, o), o nível de paralelização (-p), (n), representado por um número inteiro positivo e quais os ficheiros
              a tratar.  
              Por omissão:
                (-m): -m t
                (-p): -p 1
                ficheiros: erro se nenhum for passado
    Ensures: Retorna um tuplo que indica qual o modo de utilização e o nível de paralelização tendo em conta os argumentos passados, 
             verificando ainda se foi passado algum ficheiro como argumento
             Em caso de não ter sido passado nenhum argumento, a função retorna uma mensagem de erro
    
    '''
    mode = "t"
    num_proc = 1
    
    if sys.argv[1] == "-m" and sys.argv[2] != "t"or"u"or"o" and sys.argv[3] == "-p" and sys.argv[4] == int and str(sys.argv[5])[-4:] == ".txt":
        num_proc = sys.argv[4]
    
    if sys.argv[1] == "-m" and sys.argv[2] == "t"or"u"or"o" and sys.argv[3] == "-p" and sys.argv[4] != int and str(sys.argv[5])[-4:] == ".txt":
        mode = sys.argv[2]
    
    if sys.argv[1] == "-m" and sys.argv[2] == "t"or"u"or"o" and sys.argv[3] == "-p" and str(sys.argv[4])[-4:] == ".txt":
        mode = sys.argv[2]
    
    if sys.argv[1] == "-m" and sys.argv[2] == "-p" and sys.argv[3] == int and str(sys.argv[5])[-4:] == ".txt":
        num_proc = sys.argv[3]
    
    if sys.argv[1] == "-m" and sys.argv[2] == "t"or"u"or"o" and str(sys.argv[3])[-4:] == ".txt":
        mode = sys.argv[2]
    
    if sys.argv[1] == "-p" and sys.argv[2] == int and str(sys.argv[3])[-4:] == ".txt":
        num_proc = sys.argv[2]
    

    return tuple(mode,num_proc)


def tMode(xfile):
    '''
    Contagem do número de palavras 
    
    Requires: um ficheiro .txt
    Ensures: contagem e retorno do número de palavras no ficheiro passado como argumento
    '''
    num_words = 0       #variável de contagem de palavras
    
    #tratamento do ficheiro
    file = open(xfile,"r")
    lines = file.readlines()   #transformação das linhas do ficheiro numa lista em que cada item é uma linha
    lc_lines = lowerCasing(lines)       #transformar as letras todas em minúsculas (lc_lines --> lowercased lines)
    for line in lc_lines:    
        line.split()    #divisão de cada linha numa lista em que cada item é uma palavra

    #contagem das palavras
    for line in lc_lines:      
        num_words += enumerate(line) 
    
    return num_words

def uMode(xfile):
    '''
    Contagem do número de palavras diferentes 
    
    Requires: um ficheiro .txt
    Ensures: retorno de uma lista com cada palavra usada no ficheiro
    '''
    words_list = []
    
    #tratamento do ficheiro
    file = open(xfile,"r")
    lines = file.readlines()    
    lc_lines = lowerCasing(lines)       #transformar as letras todas em minúsculas (lc_lines --> lowercased lines)
    for line in lc_lines:
        line.split()


    #contagem de palavras únicas
    for line in lc_lines:
        for word in line:
            if word not in words_list:      #verificação de ocorrência anterior
                words_list.append(word)
    
    return words_list    #a contagem das palavras é feita na função mode, devido à pluralidade de ficheiros que podem ser passados
    

def oMode(xfile):
    '''
    Contagem do número de ocorrências de cada palavra 
    
    Requires: um ficheiro .txt
    Ensures: contagem e retorno do número de ocorrências de cada palavra única existente no ficheiro passado como argumento
    '''
    words_dict = {}     #lista de tuplos do tipo (palavra, nº de ocorrências)

    #tratamento do ficheiro
    file = open(xfile,"r")
    lines = file.readlines() 
    lc_lines = lowerCasing(lines)        #transformar as letras todas em minúsculas (lc_lines --> lowercased lines)
    for line in lc_lines:
        line.split()

    #contagem das palavras
    for line in lc_lines:
        for word in line:
            if word not in words_dict.keys():      #primeira ocorrência da palavra no ficheiro
                words_dict[word] = 1
            else:                           
                words_dict[word] += 1

    return words_dict


def pwordcount(mode, files):
    '''
    '''
    tMode_words = 0
    uMode_list = []
    oMode_dict = {}
    

    if mode == "t":
        for file in files:
            tMode_words += tMode(file)     
            print(f"{file}, {tMode_words}")     #controlo
        
        print(f"Contagem de palavras final: {tMode_words}") 
    
    elif mode == "u":
        for file in files:
            for word in uMode(file):
                if word not in uMode_list:
                    uMode_list.append(word)
            print(f"{file}, {uMode_list}")      #controlo
        
        print(f"Contagem de palavras únicas: {uMode_list}") 
    
    elif mode == "o":
        for file in files:
            for key in oMode(file).keys():
                if key not in oMode_dict.keys():
                    oMode_dict[key] = oMode(file)[key]
                else:
                    oMode_dict[key] += oMode(file)[key]
            print(f"{file}, {oMode_dict}")      #controlo
        
        print(f"Palavras e respetivas ocorrências: {oMode_dict}")    


def fileDivision(n, files_list):
    '''
    Division of the files 
    Divisão dos ficheiros por processos dado o nível de paralelização.

    Requires: n int > 0 and is the number of processes to count, files_list list not empty 
    '''

    num_files = len(files_list)
    
    if num_files > 1:
        if n >= num_files:  #n for maior ou igual ao nº de ficheiros vai haver um processo por ficheiro
            files_per_process = 1
        else:               #nº de ficheiros for maior que n faz a divisão inteira e o resto desse divisão
            files_per_process = num_files // n
            restantes = num_files % n

        divided_files = []
        i = 0  #variável de incrementação para verificar que o while só termina quando todos os ficheiros
        while i < num_files:    #forem distribuídos
            if restantes > 0:   #se houver ficheiros restantes esses ficheiros são atribuídos
                curr_files = files_list[i:i+files_per_process+1]    #ao processo atual
                i += files_per_process + 1  #o mais +1 serve para contabilizar para os ficheiros atribuídos
                restantes -= 1  #retiramos 1 dos ficheiros restantes porque foi atribuído
            else:
                curr_files = files_list[i:i+files_per_process]
                i += files_per_process

            divided_files.append(curr_files)
    elif num_files == 1:
        file_path = files_list[0]
        with open(file_path, 'r') as file:
            file_lines = sum(1 for line in file)
            files_per_process = math.ceil(file_lines / n)
            
            divided_files = []
            with open(file_path, 'r') as file:
                lines = file.readlines()
                start_line = 0
                for i in range(n):
                    end_line = min(start_line + files_per_process, file_lines)
                    divided_files.append(''.join(lines[start_line:end_line]))
                    start_line = end_line
    
    return divided_files


#TO-DO: Implementar o pwordcount

def main(args):
    '''
    '''
    start = perf_counter()

    mode = verifyArgs()[0]
    n = verifyArgs()[1]
    files_list = getFilesList()

    divided_files = fileDivision(n, files_list)

    lista_processos = []
    for file in divided_files:
        processo = Process(target=pwordcount, args=[mode, file])
        lista_processos.append(processo)
        processo.start()
    for p in lista_processos:
        processo.join()
    finish = perf_counter()
    print(f'It ended in {round(finish-start,2)}s')

    print('Programa: pwordcount.py')
    print('Argumentos: ',args)

if __name__ == "__main__":
    main(sys.argv[1:])

