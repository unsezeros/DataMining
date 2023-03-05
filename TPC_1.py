#Import de bibliotecas
import os
import numpy as np
#Limpar a consola
os.system('cls' if os.name == 'nt' else 'clear')

class Dataset:
    #Initialization
    def __init__(self):
        self.x = None
        self.y = None
        self.feature_name = None
        self.label_name = None
    
    #Setters
    def setter_x(self,x):
        self.x = x
    def setter_y(self,y):
        self.y = y
    def setter_feature_name(self,feature_name):
        self.feature_name = feature_name  
    def setter_label_name(self,label_name):
        self.label_name = label_name
    
    #Getters
    def getter_x(self):
        return self.x
    def getter_y(self):
        return self.y
    def getter_feature_name(self):
        return self.feature_name  
    def getter_label_name(self):
        return self.label_name
    
    #CSV READER
    def csv_read(self, path_file):
        with open(path_file, 'r', encoding='UTF-8') as f:
            file_lines = f.readlines()
            #Importar a linha das labels dos atributos
            self.feature_name = file_lines[0].strip().split(',')
            #Remover a linha das labels dos atributos
            file_lines = file_lines[1:]
            #Importar os dados para depois dar ao numpy
            data=[]
            for line in file_lines:
                line = line.strip().split(',')
                data.append(line)
            #Como o ficheiro de teste não tem vetor de saida, y=None e considera-se todo o data
            if self.y is None:
                self.x = np.array(data)
            else:
                self.x = np.array(data)[:, :-1]
                self.y = np.array(data)[:, -1]
    
    #Estatísticas sobre as variáveis (tipo describe) ---> To be done
    def statistics(self):
        pass
    
    #Contagens de valores nulos ---> To be done
    def null(self):
        pass
    
    #substituição e valores nulos por uma constante (valor mais comum, média) ---> To be done
    def subs_null():
        pass
    
    #Estatísticas sobre as variáveis
    def describe(self):
        print(f'x corresponds to:\n{str(self.x)}\n<--------------------------->\n')
        print(f'y corresponds to:\n{str(self.y)}\n<--------------------------->\n' if str(self.y)!='None' else 'y is not present\n<--------------------------->\n')
        ftname = '\n'.join(self.getter_feature_name())
        print(f'Feature names are:\n{ftname}\n<--------------------------->\n')
        print(f'Label name is:\n{self.getter_label_name()}\n<--------------------------->\n')

#Starter
pathfile = 'notas.csv'
dataset_script = Dataset()
dataset_script.csv_read(pathfile)
dataset_script.describe()