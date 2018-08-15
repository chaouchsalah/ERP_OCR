import re
import glob
from regex_extraction import RegexExtractor

extract = RegexExtractor()
# Extract the values(text,start,end) from the object re.match
def extract_match(result,line):
    # The tuple that stores the start and finish of the match
    span = result.span()
    start = span[0]
    end = span[1]
    # The text that was matched
    text = line[start:end]
    return text,start,end
# Extract the numbers of a facture
def extract_numbers_facture(text):
    numbers = re.search(extract.numbers_facture,text)
    # If there is a match
    if numbers is not None:
        text,_,_ = extract_match(numbers,text)
        return text
    return None
# Extract the date from the text
def extract_date(text):
    date = re.search(extract.date,text)
    if date is not None:
        text,_,_ = extract_match(date,text)
        return text
    return None
# Extract the numbers from text
def extract_numbers(text,last=True):
    numbers = re.findall(extract.numbers,text)
    # If there is no match
    if len(numbers)>0:
        if last:
            number = numbers[len(numbers)-1]
        else :
            number = numbers[0]
        # if there is only one number it probably is wrong
        if len(number)>1:
            return number
    return None
# Extract the numbers with percent from text
def extract_percent(text):
    percent = re.findall(extract.percent,text)
    # If there is no match
    if len(percent)>0:
        percent = percent[len(percent)-1]
        return percent
    return None
# Extract the value of teh field "mode de reglement"
def extract_mode(line):
    result = re.search(extract.mode,line)
    if result is not None:
        start = result.span()[1]
        line = line[start:].strip()
        end = line.find(' ')
        return line[:end].strip()
    return None
def extract_disway(line):
    result = re.search(extract.disway,line)
    if result is not None:
        text,_,_ = extract_match(result,line)
        text = text.split()
        extracted_data['date_facture'] = text[0]
        extracted_data['client'] = text[1]
# Extract the value of the field "ttc"
def extract_ttc(line):
    result = re.search(extract.expressions_ttc,line)
    if result is not None:
        text,_,end = extract_match(result,line)
        ht = re.search(extract.expressions_ht,line)
        # Check if the value found is not an ht value
        if ht is not None :
            _,_,end2 = extract_match(ht,line)
            # If they end at the same position they are probably the same value
            if end == end2:
                return None
        number = extract_numbers(text)
        if number is not None:
            return number
    return None
# Extract the value of the field "tva"
# The tva can be:
#   case 1 : [0-9].[0-9]%
#   case 2 : [0-9].[0-9]
def extract_tva(line):
    result = re.search(extract.expressions_tva,line)
    if result is not None:
        text,_,end = extract_match(result,line)
        percent = extract_percent(text)
        # case 1
        if percent is not None:
            result = re.search(extract.numbers,line[end:])
            if result is not None:
                text,_,_ = extract_match(result,line[end:])
                number = extract_numbers(text)
                extracted_data['montant tva'] = number
            return percent
        number = extract_numbers(text)
        # case 2
        if number is not None:
            return number
    return None
# Extract the value of the field "ht"
def extract_ht(line):
    results = re.finditer(extract.expressions_ht,line)
    results = tuple(results)
    if len(results)>0:
        for result in results:
            text,_,_ = extract_match(result,line)
            number = extract_numbers(text)
            if number is not None:
                return number
    return None
# Extract the fields at the bottom of the page 'rc, if, ice, patente and cnss
def extract_bottom(line,component):
    expression = {
        'rc':extract.expressions_rc,
        'if':extract.expressions_if,
        'ice':extract.expressions_ice,
        'patente':extract.expressions_patente,
        'cnss':extract.expressions_cnss
    }
    result = re.search(expression[component],line)
    if result is not None:
        text,_,_ = extract_match(result,line)
        number = extract_numbers(text)
        if number is not None:
            return number
    return None
def inline_component(line,component):
    if component=='ht':
        return extract_ht(line)
    elif component=='tva':
        return extract_tva(line)
    elif component=='ttc':
        return extract_ttc(line)
    elif component=='mode_reglement':
        return extract_mode(line)
    elif component=='rc':
        return extract_bottom(line,component)
    elif component=='if':
        return extract_bottom(line,component)
    elif component=='ice':
        return extract_bottom(line,component)
    elif component=='patente':
        return extract_bottom(line,component)
    elif component=='cnss':
        return extract_bottom(line,component)
# Extract the value of one of the fields "ht,tva,ttc" if it's not on the same line
def multilines_component(lines,component):
    keywords = {
        'ht':extract.keywords_ht,
        'tva':extract.keywords_tva,
        'ttc':extract.keywords_ttc
    }
    start = None
    end = None
    numbers = None
    for line in lines:
        if start is None and end is None:
            result = re.search(keywords[component],line)
            if result is not None:
                _,start,end = extract_match(result,line)
        elif len(line.strip())>0:
            start = start - 10 if start - 10 > 0 else 0
            numbers = extract_numbers(line[start:],False)
            start = None
            end = None
    if numbers is not None:
        return numbers
    return None 
# Extract the number of facture if inline
def extract_facture(lines):
    result = re.search(extract.facture,lines)
    if result is not None:
        text,start,_ = extract_match(result,lines)
        numbers = extract_numbers_facture(text)
        if numbers is not None:
            # Extract the date if found on the same line
            result = re.search(r'[\s]du[\s]',lines[start:])
            if result is not None:
                span = result.span()
                start = span[0]+start
                result = re.search(r'[0-9]{2}[/][0-9]{2}[/][0-9]{4}',lines[start:])
                if result is not None:
                    span = result.span()
                    start = span[0]+start
                    end = span[1]
                    extracted_data['date_facture'] = lines[start:start+end]
            return numbers
    return None
# Extract the number of facture if it's not on the same line
def extract_facture_multilines(lines):
    found = False
    date = False
    start = 0
    for line in lines:
        if not found:
            result = re.search(extract.facture_multilines,line)
            if result is not None:
                _,start,_ = extract_match(result,line)
                result = re.search(r'[\s]*date[\s]*',line)
                if result is not None:
                    date = True
                found = True
        else:
            if len(line.strip())>0:
                if start-5<0:
                    start = 0
                values = line[start:].split(' ')
                if len(values[0])>1:
                    if date:
                        extracted_data['date'] = values[1]
                        if len(values)==3:
                            extracted_data['client'] = values[2]
                        return values[0]
                found = False
    return None
# Extract the number of the client
def extract_client(lines):
    result = re.search(extract.client,lines)
    if result is not None:
        _,_,end = extract_match(result,lines)
        result = re.search(r'[\s]',lines[end-1:])
        if result is not None:
            _,start,_ = extract_match(result,lines[end-1:])
            return lines[end-1:end+start-1]
    return None
# Extract the field of 'date limite de paiement'
def extract_date_limite(line,field):
    result = re.search(extract.date_limite,line)
    if result is not None:
        text,_,_ = extract_match(result,line)
        date = extract_date(text)
        if date is not None:
            return date
    return None
# Extract the field of 'date limite de paiement'
def extract_date_facture(line,field):
    result = re.search(extract.date_facture,line)
    if result is not None:
        text,_,_ = extract_match(result,line)
        date = extract_date(text)
        if date is not None:
            return date
    return None
# Extract the field 'telephone'
# Return Telephone if found
# Else return None
def extract_tel(line,field):
    result = re.search(extract.expressions_tel,line)
    if result is not None:
        _,_,end = extract_match(result,line)
        # Regex for the end of the field 'telephone'
        result = re.search(r'[\s]{2,}|[\n]|[\s][^0-9]',line[end:])
        if result is not None:
            _,start,_ = extract_match(result,line[end:])
            return line[end:end+start]
            """text = line[:start+end]
            # Regex for the start of the field 'telephone'
            result = re.search(r'[0-9]{3,}|[(][0-9]|[+][0-9]',text)
            if result is not None:
                _,start,_ = extract_match(result,text)
                return text[start:]"""
    return None
# Extract the field 'adresse' if number of line == 1
def extract_adresse_inline(line,field):
    result = re.search(extract.adresse_inline,line)
    if result is not None:
        _,_,end = extract_match(result,line)
        # Ignore field adresse ip
        if line[end:end+2] != 'ip':
            return line[end:]
    return None
def nthline_adresse(line):
    # Format of an adresse line
    result = re.search(extract.nthline_adresse,line)
    _,start,_ = extract_match(result,line)
    if result is not None:
        found = True
        return [found,line[start:]]
    return None
# Extract the field 'adresse' if number of lines > 1
def extract_adresse_multilines(lines,field):
    found = False
    adresse = ''
    for line in lines:
        if not found:
            result = re.search(extract.adresse_multilines,line)
            if result is not None:
                result = nthline_adresse(line)
                if result is not None:
                    found = result[0]
                    adresse += result[1]
        else:
            if len(line.strip())>0:
                result = nthline_adresse(line)
                if result is not None:
                    found = result[0]
                    adresse += result[1]
                found = False
        if adresse != '' and not found:
            return adresse
    return None
infos = ['rc','if','ice','patente','cnss']
# Check if field has not been already extracted
# Check if field is in text
def verify(field,extraction,text):
    if field not in extracted_data or field in infos:
        variable = extraction(text,field)
        if variable is not None:
            if field=='tva' and '%' not in variable:
                extracted_data['montant tva'] = variable
            else:
                extracted_data[field] = variable
# TVA 2 cases : 'montant' or 'percent'
components = ['ht','tva','ttc','tva']
extracted_data = {}
def run(filename):
    global extracted_data
    extracted_data = {}
    image_name = filename.split('.')
    if len(image_name)==2:
        filename = image_name[0]
    else:
        filename = image_name[0:len(image_name)-2]
    filename += '.txt'
    #print('START '+filename)
    file = open(filename,encoding='utf-8')
    lines = file.readlines()
    temp_lines = '\n'.join(lines)
    facture = extract_facture(temp_lines)
    client = extract_client(temp_lines)
    if client is not None:
        extracted_data['client'] = client
    if facture is not None:
        extracted_data['facture'] = facture
    if 'facture' not in extracted_data:
        facture = extract_facture_multilines(lines)
        if facture is not None:
            extracted_data['facture'] = facture
    for line in lines:
        extract_disway(line)
        verify('date_limite',extract_date_limite,line)
        verify('mode_reglement',inline_component,line)
        verify('tel',extract_tel,line)
        verify('adresse',extract_adresse_inline,line)
        verify('date_facture',extract_date_facture,line)
        for component in components:
            verify(component,inline_component,line)
        for info in infos:
            verify(info,inline_component,line)
    verify('adresse',extract_adresse_multilines,lines)
    for component in components:
        verify(component,multilines_component,lines)
    #print('FINISHED '+filename)
    return extracted_data