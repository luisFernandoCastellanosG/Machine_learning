#librerias necersarias
import csv
import xml.etree.ElementTree as etree
from sklearn.model_selection import train_test_split

#definición de la clase  
class DatasetHelper:

    #metodo para convertir en corpus GENERAL de XML a una lista
    @staticmethod
    def general_tass_to_list(filename):
        tree = etree.parse(filename)
        root = tree.getroot()
        data = []

        for tweet in root:
            tweetId = tweet.find('tweetid').text
            content = tweet.find('content').text
            polarityValue = tweet.find('sentiments/polarity/value').text
            data.append([tweetId, content.replace('\n',' '), polarityValue])

        return data

    #metodo para convertir en corpus GENERAL de XML a una lista   
    @staticmethod
    def politics_tass_to_list(filename):
        tree = etree.parse(filename)
        root = tree.getroot()
        data = []

        for tweet in root:
            tweetId = tweet.find('tweetid').text
            content = tweet.find('content').text
            aux = next((e for e in tweet.findall('sentiments/polarity') if e.find('entity') == None), None)
            if aux != None:
                polarityValue = aux.find('value').text
                data.append([tweetId, content.replace('\n',' '), polarityValue])

        return data

    #metodo para convertir en corpus INTERNACIONAL (temas diversos) de XML a una lista   
    @staticmethod
    def intertass_tass_to_list(filename, qrel=None):
        tree = etree.parse(filename)
        root = tree.getroot()
        data = []

        for tweet in root:
            tweetId = tweet.find('tweetid').text
            content = tweet.find('content').text
            polarityValue = tweet.find('sentiment/polarity/value').text
            if polarityValue == None:
                polarityValue = qrel[tweetId]

            data.append([tweetId, content.replace('\n',' '), polarityValue])

        return data
     
    #metodo para genera una lista adicional del corpus INTENACIONAL
    @staticmethod
    def gold_standard_to_dict(filename):
        with open(filename, 'r') as csvfile:
            reader = csv.reader(csvfile, delimiter='\t')
            data = {rows[0]: rows[1] for rows in reader}

        return data
    
    #metodo para convertir una lista en un archivo CSV 
    @staticmethod
    def list_to_csv(data, filename):
        with open(filename, 'w', encoding='utf-8') as csvfile:
            writer = csv.writer(csvfile, delimiter=',', lineterminator='\n', quoting=csv.QUOTE_NONNUMERIC)
            writer.writerows(data)

    #metodo para separar la DATA (unión de todos los corpus) en una parte para TRAIN y otra para TEST
    @staticmethod
    def generate_train_test_subsets(data, size):
        codes = [d[0] for d in data]
        labels = [d[2] for d in data]
        codes_train, codes_test, labels_train, labels_test = train_test_split(codes, labels, train_size=size)
        train_data = [d for d in data if d[0] in codes_train]
        test_data = [d for d in data if d[0] in codes_test]
        return train_data, test_data

    #Metodo para convertir CSV a una lista (para hacer todo el preprocesamiento)
    @staticmethod
    def csv_to_lists(filename):
        messages = []
        labels = []
        with open(filename, 'r', encoding='utf-8') as csvfile:
            reader = csv.reader(csvfile, delimiter=',')
            for row in reader:
                messages.append(row[1])
                labels.append(row[2])
        return messages, labels

#tomamos el corpus internacional (test) y generamos una lista del ID del tweet y el sentimiento para agregarlo a la data
qrel = DatasetHelper.gold_standard_to_dict("../datasets/tass_2017/InterTASS/intertass-sentiment.qrel")

#creamos una lista/matriz [tweetId | Message | sentiment ]
data = []
data.extend(DatasetHelper.general_tass_to_list("../datasets/tass_2017/InterTASS/general-test-tagged-3l.xml"))
data.extend(DatasetHelper.general_tass_to_list("../datasets/tass_2017/InterTASS/general-train-tagged-3l.xml"))
data.extend(DatasetHelper.intertass_tass_to_list("../datasets/tass_2017/InterTASS/intertass-development-tagged.xml"))
#como el test del corpus internacional esta sin los sentimientos es necesario agregarlos : qrel
data.extend(DatasetHelper.intertass_tass_to_list("../datasets/tass_2017/InterTASS/intertass-test.xml", qrel))
data.extend(DatasetHelper.intertass_tass_to_list("../datasets/tass_2017/InterTASS/intertass-train-tagged.xml"))
data.extend(DatasetHelper.politics_tass_to_list("../datasets/tass_2017/InterTASS/politics-test-tagged.xml"))

#separamos la data en train = 70%  | test = 30#
train, test = DatasetHelper.generate_train_test_subsets(data, size=0.3)

#para facilidad del trabajo pasamos toda la data a archivos CSV que son más practicos de manejar.
DatasetHelper.list_to_csv(data, '../datasets/global_dataset.csv')
DatasetHelper.list_to_csv(train, '../datasets/train_dataset_30.csv')
DatasetHelper.list_to_csv(test, '../datasets/test_dataset_30.csv')