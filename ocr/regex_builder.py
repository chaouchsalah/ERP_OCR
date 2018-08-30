import re

# Compile all regex expressions needed for postprocessing
class RegexBuilder:
    def __init__(self):
        self.compile_num_regex()
        self.correct_numbers()
        self.check_net()
        self.main_component()
        self.numbers()
        self.find_dot()
        self.white_space()
        self.abrv_dot_extraction()
        self.date_format()
    
    # Generalise the n° format
    def compile_num_regex(self):
        facture_types = ['facture','de la facture']
        bon_types = ['bon de livraison','bon livraison']
        page_types = ['page']
        commande_types = ['commande']
        numeros = ['110','N\'','n0','NO','NO.','#','Na','NC']
        clients = ['client']
        combined_factures = []
        combined_bons = []
        combined_pages = []
        combined_commandes = []
        combined_clients = []
        for numero in numeros:
            for facture_type in facture_types:
                combined_factures.append(self.generate_expression(facture_type,numero))
            for bon_type in bon_types:
                combined_bons.append(self.generate_expression(bon_type,numero))
            for client in clients:
                combined_clients.append(self.generate_expression(client,numero))
            for page_type in page_types:
                combined_pages.append(self.generate_expression(page_type,numero))
            for commande_type in commande_types:
                combined_commandes.append(self.generate_expression(commande_type,numero))
        self.compiled_factures = re.compile(r'|'.join(combined_factures))
        self.compiled_bons = re.compile(r'|'.join(combined_bons))
        self.compiled_pages = re.compile(r'|'.join(combined_pages))
        self.compiled_commandes = re.compile(r'|'.join(combined_commandes))
        self.compiled_clients = re.compile(r'|'.join(combined_clients))
    # Generate needed regular expressions
    def generate_expression(self,item_type,numero):
        expressions = [r'(?i){0}[\s]{1}\s'.format(item_type,numero),
                        r'(?i){0}[\s]N[0-9]\s'.format(item_type),
                        r'(?i){0}[\s]+{1}'.format(item_type,numero),
                        r'(?i){0}{1}\s'.format(item_type,numero),
                        r'(?i){0}[\s]+{1}'.format(numero,item_type),
                        r'(?i){0}[\s]+{1}\s'.format(numero,item_type)]
        return r'|'.join(expressions)
    # Correct some numbers mistakes
    def correct_numbers(self):
        # Numbers with zero at the end separated
        expression = r'[0-9]+[\s]{1,2}[Oo0][\s]'
        self.zero_end = re.compile(expression)
    def generate_components(self,component):
        expressions = [r'(?i)[\s]*{0}[\s]+'.format(component)]
        return expressions
    def generate_abrv_components(self,component):
        expressions = [r'(?i)[\s]*{0}[\s]+'.format(component),
                        r'(?i)[\s]*{0}[\s]*'.format(r'\.'.join(list(component))),
                        r'(?i)total[\s]*{0}'.format(component),
                        r'(?i)total[\s]*{0}'.format(r'\.'.join(list(component)))]
        return expressions
    def main_component(self):
        abrv_tva = ['tva']
        tva = ['taux']
        abrv_ttc = ['ttc']
        ttc = ['toute taxe comprise']
        abrv_ht = ['ht']
        ht = ['hors taxe','base']
        self.expressions_tva = []
        self.expressions_ttc = []
        self.expressions_ht = []
        for component in abrv_tva:
            self.expressions_tva += self.generate_abrv_components(component)
        for component in tva:
            self.expressions_tva += self.generate_components(component)
        for component in abrv_ttc:
            self.expressions_ttc += self.generate_abrv_components(component)
        for component in ttc:
            self.expressions_ttc += self.generate_components(component)
        for component in abrv_ht:
            self.expressions_ht += self.generate_abrv_components(component)
        for component in ht:
            self.expressions_ht += self.generate_components(component)
        self.expressions_tva = r'|'.join(self.expressions_tva)
        self.expressions_tva = re.compile(self.expressions_tva)
        self.expressions_ttc = r'|'.join(self.expressions_ttc)
        self.expressions_ttc = re.compile(self.expressions_ttc)
        self.expressions_ht = r'|'.join(self.expressions_ht)
        self.expressions_ht = re.compile(self.expressions_ht)
    # Regex for field 'net a payer'
    def check_net(self):
        expressions = [r'(?i)net [a-zA-Z0-9]+ payer',
                    r'(?i)net\s[a-zA-Z0-9]+\sPa[\s]+et']
        combined_expression = r'|'.join(expressions)
        self.net_payer = re.compile(combined_expression) 
    # Possible numbers regex
    def numbers(self):
        expressions = [ r'[0-9]+',
                        r'[0-9]+.[0-9]+']
        combined_expression = r'|'.join(expressions)
        self.number_format = re.compile(combined_expression)
        self.number = re.compile(r'[0-9]+')
        self.format_number = re.compile(r'[0-9]+[\s]{1,2}[0-9]+')
    # Search for . or : at the end of a word
    def find_dot(self):
        self.dot_end = re.compile(r'[.:]\B')
    # Regex for whitespace
    def white_space(self):
        self.whitespace = re.compile(r'[\s]+')
    def abrv_possible(self,term):
        possibility = r'(?i)[\s]*'
        for letter in term:
            possibility += letter+r'[\s]?[.]?'
        return possibility + r'[\s]+'
    # Remove dots from abreviations
    def abrv_dot_extraction(self):
        terms = ['ht','tva','ttc','if','ice','cnss','rc','tp']
        expressions = []
        for term in terms:
            expressions.append(self.abrv_possible(term))
        expressions = r'|'.join(expressions)
        self.abrv_dot = re.compile(expressions)
    # Regex for date
    def date_format(self):
        expressions = [r'[^\s][0-9]{2}[/\'][0-9]{2}[/\'][0-9]{4}[^\s]',
                        r'[^\s][0-9]{4}[/][0-9]{4}[%]']
        expressions = r'|'.join(expressions)
        self.date = re.compile(expressions)
        expressions = [r'[0-9]{2}[\s]*[/][\s]*[0-9]{2}[\s]*[/][\s]*[0-9]{4}']
        expressions = r'|'.join(expressions)
        self.date_spaces = re.compile(expressions)