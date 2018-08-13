import re
from multiprocessing.dummy import Pool as ThreadPool 
from regex_builder import RegexBuilder
import time
from symspell import SymSpell

build_regex = RegexBuilder()
spell = SymSpell()
spell.load_dictionary('new_big.txt')
# Characters to ignore
special_chars = [':','.','\n','%','$','€']
# Extract the values(text,start,end) from the object re.match
def extract_match(result,line):
    # The tuple that stores the start and finish of the match
    span = result.span()
    start = span[0]
    end = span[1]
    # The text that was matched
    text = line[start:end]
    return text,start,end
# Separate date from other numbers
def separate_date(line):
    result = re.search(build_regex.date,line)
    if result is not None:
        _,start,end = extract_match(result,line)
        line = line[:start+1]+' '+line[start+1:end-1]+' '+line[end-1:]
        matches = re.finditer('/',line)
        matches = tuple(matches)
        # If there is less than 2 '/' the date is not formatted correctly
        if len(matches)<2 and len(matches)>0:
            for match in matches:
                _,start,_ = extract_match(match,line)
                line = line[:start-2]+'/'+line[start-2:]
        # OCR edge cases
        line = line.replace('O','0')
        line = line.replace('%','')
        line = line.replace('J','')
    return line
# Remove dots from abreviations
def abrv_rm(line):
    results = re.finditer(build_regex.abrv_dot,line)
    results = tuple(results)
    if len(results)>0:
        new_line = ''
        start_line = 0
        for result in results:
            _,start,end = extract_match(result,line)
            word = line[start:end].replace('.','')
            new_line += line[start_line:start]
            new_line += word
            start_line = end
        new_line += line[start_line:]
        return new_line
    return line
def correct_numbers(line):
    result = re.search(build_regex.zero_end,line)
    if result is not None:
        result = result.span()
        start = result[0]
        end = result[1]
        tmp_line = line[start:]
        line = '{0}{1}0{2}'.format(line[:start],line[start:start+tmp_line.find(' ')],line[end+1:])
    return line
# Generalise the n° format
def check_num(line):
    line = re.sub(build_regex.compiled_factures,'facture :',line)
    line = re.sub(build_regex.compiled_bons,'bon livraison :',line)
    line = re.sub(build_regex.compiled_pages,'page :',line)
    line = re.sub(build_regex.compiled_commandes,'commande :',line)
    line = re.sub(build_regex.compiled_clients,'client ',line)
    return line
# Fix the 'net a payer' field
def check_net(line):
    line = re.sub(build_regex.net_payer,'net a payer:',line)
    return line
# Remove all non alpha-numeric character at the start of a line
def remove_starting_chars(line):
    i=0
    while i<len(line) and not line[i].isalnum():
        i += 1
    return None if line[i:].isspace() else line[i:]
# Check if word got more letters than special chars
def possible_word(word):
    letters = 0
    if re.match(build_regex.expressions_ht,word) \
        or re.match(build_regex.expressions_ttc,word) \
        or re.match(build_regex.expressions_tva,word):
        return True
    for char in word:
        if char.isalpha():
            letters += 1
    return letters >= len(word)-letters or word[:5] == '(212)' # Second condition to check if it's a tel
# Remove lines with a character or less
def remove_empty_line(line):
    return None if len(line.strip())<=1 else line
# Remove words that have 3 letters repeated
def remove_repetition(line):
    new_line = []
    # Split line into words
    line = line.split(' ')
    for word in line:
        if len(word)>0:
            i=0
            # Ignore all characters that aren't numeric
            while i < len(word) and word[i].isnumeric():
                i += 1
            if i < len(word):
                char = word[i]
                i += 1
                repetition = 1
                while i<len(word) and repetition < 3:
                    if word[i]==char:
                        repetition += 1
                    else :
                        # Ignore all characters that aren't numeric
                        while i < len(word) and word[i].isnumeric():
                            i += 1
                        if i < len(word):
                            char = word[i]
                            repetition = 1
                    i += 1
                # Verify if word has repetitive characters
                if repetition != 3:
                    new_line.append(word)
                elif repetition == 3:
                    # Special case for websites
                    if 'www.' in word:
                        new_line.append(word)
            else :
                new_line.append(word)
        else :
            new_line.append(word)
    new_line = ' '.join(new_line)
    return new_line
def remove_unkonwn_word(line):
    if not special_words(line):
        new_line = []
        line = line.split(' ')
        for word in line :
            # Check if word is a number
            if not re.match(build_regex.number_format,word):
                if len(word.strip())>0:
                    if possible_word(word.strip()) or word.strip() in special_chars :
                        new_line.append(word)
                    else :
                        if '\n' in word:
                            new_line.append('\n')
                        elif re.match(r'[:][0-9]',word) is not None:
                            new_line.append(word)
                else:
                    new_line.append(word)
            else:
                new_line.append(word)
        line = ' '.join(new_line)
    return line 
# Remove the words with only 1 letter
def remove_one_letter_word(line):
    new_line = []
    results = re.finditer(build_regex.abrv_dot,line)
    results = tuple(results)
    if len(results)>0:
        for result in results:
            _,start,end = extract_match(result,line)
            match = line[start:end].strip()
            match = match.replace(' ','')
            line = line[:start]+' '+match+' '+line[end:]
    line = line.split(' ')
    for word in line :
        word_test = word.strip()
        single_letters = ['a','m']
        if len(word_test)!=1 or not word_test.isalpha() or word_test.lower() in single_letters or word_test in special_chars:
            new_line.append(word)
    line = ' '.join(new_line)
    return line
# Calling the functions to format a line (the order is important)
def format_line(line):
    line = remove_starting_chars(line)
    if line is None:
        return line
    line = remove_empty_line(line)
    if line is None:
        return line
    line = remove_repetition(line)
    line = remove_empty_line(line)
    if line is None:
        return line
    line = check_num(line)
    line = check_net(line)
    line = correct_numbers(line)
    """if line is not None and 'C .N.S.S.' in line:
        print(line)"""
    line = remove_one_letter_word(line)
    line = remove_empty_line(line)
    if line is None:
        return line
    line = remove_unkonwn_word(line)
    line = remove_empty_line(line)
    if line is None:
        return line
    return line
# Special cases to check
def special_words(line):
    return line.strip()[:2] == 'M.' or 'code client' in line.lower() or re.match(r'M\s',line[:2])
# Checking spelling mistakes against our personal dictionnary
def spell_correction(line):
    # The max distance of number of changes
    DISTANCE = 3
    new_line = []
    if not special_words(line):
        nbr_correction = 0
        corrected_word = ''
        # Split line into words
        line = line.split(' ')
        for word in line:
            if len(word.strip())>1 and not re.match(build_regex.number_format,word):
                word = re.sub(build_regex.dot_end,'',word)
                # If it's not a phone number
                if '(212)' not in word:
                    # Correct spelling mistakes
                    corrected = spell.lookup_compound(word.lower(),DISTANCE)[0].term
                    if corrected != False:
                        nbr_correction += 1
                        corrected_word = corrected
                        if '\n' in word:
                            corrected += '\n'
                        new_line.append(corrected)
                    else :
                        new_line.append(word)
                else :
                    new_line.append(word)
            else:
                new_line.append(word)
        line = ' '.join(new_line)
        if nbr_correction == 1:
            # Remove whitespaces
            new_line = re.sub(build_regex.whitespace,' ',line)
            # Remove special characters
            for char in special_chars:
                new_line = new_line.replace(char,'')
            new_line = re.sub(build_regex.number,'',new_line)
            # The ratio (15%) for a line to be meaningful
            ratio = 0.15
            word_line = len(corrected_word)/len(new_line.strip())
            if word_line<ratio:
                return ''
        elif nbr_correction == 0:
            new_line = re.sub(build_regex.whitespace,' ',line)
            numbers = 0
            for letter in new_line:
                if letter.isnumeric():
                    numbers += 1
            if numbers>len(new_line)-numbers:
                return line
            return ''
    return line
# Join numbers with spaces in between
def format_numbers(line):
    results = re.finditer(build_regex.format_number,line)
    results = tuple(results)
    if len(results)>0:
        new_line = ''
        current_line = 0
        for result in results:
            start = result.span()[0]
            whitespace_pos1 = line[start:].find(' ')
            start = start+whitespace_pos1
            line_start = start
            number = re.search(r'[0-9]',line[start:])
            start = start+number.span()[0]
            line_end = start
            whitespace_pos2 = line[start:].find(' ')
            start = start + whitespace_pos2 + 1
            whitespace_pos = line[start:].find(' ')
            if whitespace_pos==-1:
                whitespace_pos=len(line)-start
            start2 = start + whitespace_pos
            if line[start:start2].strip() == '00':
                return line[:start]+line[start+2:]
            new_line += line[current_line:line_start]
            current_line = line_end
        return new_line+line[current_line:]
    return line
def format_spell(line):
    line = line.replace(',','.')
    line = line.replace('/o','%')
    line = re.sub(r'(?i)p[a-z%]{2}ente','patente',line)
    line = line.replace('hm1te','limite')
    line = format_line(line)
    if line is not None:
        line = spell_correction(line)
        line = remove_empty_line(line)
        if line is not None:
            line = format_numbers(line)
            line = abrv_rm(line)
            line = separate_date(line)
            return '{0}\n'.format(line)
    return ''
def run(filename):
    image_name = filename.split('.')
    if len(image_name)==2:
        filename = image_name[0]
    else:
        filename = image_name[0:len(image_name)-2]
    filename += '.txt'
    print('Post-processing of file : '+filename)
    file = open(filename)
    lines = file.readlines()
    """if filename == 'cropped/4.txt':
        print(lines)"""
    new_file = map(format_spell,lines)
    result_file = open(filename,'w+',encoding='utf8')
    result_file.writelines(new_file)
    result_file.close()
    print('Post-processing finished')