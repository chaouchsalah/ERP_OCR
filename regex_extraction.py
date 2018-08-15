import re

# Compile all regex expressions needed for extractions
class RegexExtractor:
    terms_ttc = ['total','total de la facture','total ttc','ttc']
    terms_tva = ['taux','tva','total tva','tva port']
    terms_ht = ['sous total','base','total ht','total dh ht','ht']
    terms_rc = ['rc']
    terms_if = ['if','f']
    terms_ice = ['ice','icf']
    terms_patente = ['patente','tp','taxe professionnelle']
    terms_cnss = ['cnss']
    def __init__(self):
        terms = {
            'tva':self.tva,
            'ht':self.ht,
            'ttc':self.ttc,
            'rc':self.rc,
            'if':self.if_component,
            'ice':self.ice,
            'patente':self.patente,
            'cnss':self.cnss
        }
        for term in terms:
            self.expression_factory(term,terms[term])
        self.extract_numbers()
        self.extract_percent()
        self.mode_reglement()
        self.num_facture()
        self.num_client()
        self.format_date()
        self.format_tel()
        self.format_adresse()
        self.format_disway()
    # Factory method to generate expressions for 'ht,tva,ttc'
    def expression_factory(self,component,generate):
        # An alternative to the switch statement
        terms = {
            'ht':self.terms_ht,
            'tva':self.terms_tva,
            'ttc':self.terms_ttc,
            'rc':self.terms_rc,
            'if':self.terms_if,
            'ice':self.terms_ice,
            'patente':self.terms_patente,
            'cnss':self.terms_cnss
        }
        if component in terms:
            expressions = []
            for term in terms[component]:
                expressions += generate(term)
            expressions = r'|'.join(expressions)
            expressions_multilines = []
            for term in terms[component]:
                if component=='ttc':
                    # Regex : ttc term not followed by t or h or n
                    expressions_multilines.append(r'{0}[\s]+[^thn]'.format(term))
                else:
                    expressions_multilines.append(r'{0}'.format(term))
            expressions_multilines = r'|'.join(expressions_multilines)
            if component=='ht':
                self.expressions_ht = re.compile(expressions)
                self.keywords_ht = re.compile(expressions_multilines)
            elif component=='tva':
                self.expressions_tva = re.compile(expressions)
                self.keywords_tva = re.compile(expressions_multilines)
            elif component=='ttc':
                self.expressions_ttc = re.compile(expressions)
                self.keywords_ttc = re.compile(expressions_multilines)
            elif component=='rc':
                self.expressions_rc = re.compile(expressions)
            elif component=='if':
                self.expressions_if = re.compile(expressions)
            elif component=='ice':
                self.expressions_ice = re.compile(expressions)
            elif component=='patente':
                self.expressions_patente = re.compile(expressions)
            elif component=='cnss':
                self.expressions_cnss = re.compile(expressions)
    # All possible ttc regex
    def ttc(self,term):
        # ttc inline format EX: total : 1200.50
        expressions = [r'(?i){0}[\s]*[:.]?[\s]*[0-9]+[.]?[0-9]*'.format(term)]
        return expressions
    # All possible tva regex
    def tva(self,term):
        expressions = [r'(?i){0}[\s]*[:2]?[\s]*[0-9]+[.]?[0-9]*[\s]*[%]?'.format(term),
                        r'(?i){0}[\s]*dh[\s]*[0-9]+[.]?[0-9]*[\s]*[%]?'.format(term)]
        return expressions
    # All possible ht regex
    def ht(self,term):
        expressions = [r'{0}[\s]*[:]?[\s]*[0-9]+[.]?[0-9]*'.format(term)]
        return expressions
    # All possible rc regex
    def rc(self,term):
        expressions = [r'{0}[\s]*[:]?[\s]*[0-9]+'.format(term)]
        return expressions
    # All possible if regex
    def if_component(self,term):
        if len(term)>1:
            expressions = [r'{0}[\s]*[:]?[\s]*[0-9]+'.format(term)]
        else:
            expressions = [r'(?i)[0-9][.]{0}[.][\s]*[0-9]+'.format(term)]
        return expressions
    # All possible ice regex
    def ice(self,term):
        expressions = [r'{0}[\s]*[:]?[\s]*[0-9]+'.format(term)]
        return expressions
    # All possible patente regex
    def patente(self,term):
        expressions = [r'{0}[\s]*[:]?[\s]*[0-9]+'.format(term)]
        return expressions
    # All possible cnss regex
    def cnss(self,term):
        expressions = [r'{0}[\s]*[:]?[\s]*[0-9]+'.format(term)]
        return expressions
    # Regex to extract a number
    def extract_numbers(self):
        expression = r'[0-9]+[.]?[0-9]*'
        self.numbers = re.compile(expression)
        self.numbers_facture = re.compile(r'[0-9]+[.-]?[0-9]*')
    # Regex to extract a number with percent
    def extract_percent(self):
        expression = r'[0-9]+[.]?[0-9]*[\s]*%'
        self.percent = re.compile(expression)
    # Regex to extract the field 'mode de reglement'
    def mode_reglement(self):
        expression = r'(?i)Mode[\s]+[a-zA-Z%]*[\s]+:'
        self.mode = re.compile(expression)
    # Regex to extract the number of the facture
    def num_facture(self):
        expressions = [r'[\s]{2,}facture[\s]*[:]?[\s]*[0-9]+[.-]?[0-9]*',
                        r'[\s]{2,}invoice[\s]*[:]?[\s]*[0-9]+[.-]?[0-9]*']
        expressions = r'|'.join(expressions)
        self.facture = re.compile(expressions)
        expressions = [r'[\s]*facture[\s]*',
                        r'[\s]*invoice[\s]*']
        expressions = r'|'.join(expressions)
        self.facture_multilines = re.compile(expressions)
    # Regex to extract the number of the client
    def num_client(self):
        expressions = [r'client[\s]*[:]?[\s]*[0-9]']
        expressions = r'|'.join(expressions)
        self.client = re.compile(expressions)
    # Regex to extract the limit date to pay
    def format_date(self):
        date_limite = ['date limite de paiement','date limite paiement','date echeance','date d\'echaeance']
        expressions = []
        for date in date_limite:
            expressions.append(r'{0}[\s]*[:]?[\s]*[0-9]+[/][0-9]+[/][0-9]+'.format(date))
        expressions = r'|'.join(expressions)
        self.date = re.compile(r'[0-9]+[/][0-9]+[/][0-9]+')
        self.date_limite = re.compile(expressions)
        date_facture = ['date','date facture','date de facture']
        expressions = []
        for date in date_facture:
            expressions.append(r'{0}[\s]*[:]?[\s]*[0-9]+[/][0-9]+[/][0-9]+'.format(date))
        expressions = r'|'.join(expressions)
        self.date_facture = re.compile(expressions)
    def format_tel(self):
        telephones = ['tel','telephone']
        expressions = []
        for telephone in telephones:
            expressions.append(r'{0}[\s]*[:]?[\s]+'.format(telephone))
        expressions = r'|'.join(expressions)
        self.expressions_tel = re.compile(expressions)
        expressions = [r'[0-9]+',
                        r'([0-9]+)']
        expressions = r'|'.join(expressions)
        self.tel = re.compile(expressions)
    def format_adresse(self):
        adresses = ['adresse']
        expressions = []
        for adresse in adresses:
            expressions.append(r'{0}[\s]*[:]?[\s]*'.format(adresse))
        expressions = r'|'.join(expressions)
        self.adresse_inline = re.compile(expressions)
        expressions = []
        keywords = ['boulevard','quartier','rue','hay']
        for keyword in keywords:
            expressions.append(r'[\s]*{0}[\s]*'.format(keyword))
        expressions = r'|'.join(expressions)
        self.adresse_multilines = re.compile(expressions)
        self.nthline_adresse = re.compile(r'[0-9]+[\s][a-z]+|[a-z]+[\s][a-z]+')
    def format_disway(self):
        expression = r'(?i)[0-9]{2}[/][0-9]{2}[/][0-9]{4}[\s]+[0-9a-z]+[\s]+[0-9]+[\s]+[0-9a-z]+[-][0-9]+'
        self.disway = re.compile(expression)

