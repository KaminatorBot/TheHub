import re
import colorama
colorama.init()

VRS = {
}

VRS_CODE = {
    'INPUT_PREFIX': '~ ',
    'COMMAND_PREFIX': '$',
    'COMMANDS': []
}

class Argument:
    def __init__(self, name:str, value:object, type_arg:str):
        self.name:str = name
        self.type_arg:str = type_arg
        self.value:object = value

class MoreArguments(Argument):
    def __init__(self, name:str, type_arg:str):
        super().__init__(name, [], type_arg)

class Command:
    name:str
    args:list[Argument]
    more_args:MoreArguments|bool = False

    @classmethod
    def exec(cls):
        return

def compiler():
    text_re = r'(\'[^\']*\'|(?<!\')\b[a-zA-Z][^\s\']*\b(?!\'))'
    number_re = r'(\-[0-9]+\.[0-9]+|[0-9]+\.[0-9]+|\-[0-9]+|[0-9]+)'
    total_re = r'(\-[0-9]+\.[0-9]+|[0-9]+\.[0-9]+|\-[0-9]+|[0-9]+|\'[^\']*\'|(?<!\')\b[a-zA-Z][^\s\']*\b(?!\'))'

    command = input(VRS_CODE['INPUT_PREFIX'] + colorama.Style.RESET_ALL)

    for k in VRS.keys():
        command = command.replace('{$' + k + '$}', str(VRS[k]))

    if len(command) < 1:
        return 'NOTHING'

    command_split = command.split()
    the_command:Command = None
        
    if command_split[0].startswith(VRS_CODE['COMMAND_PREFIX']):
        a = command_split[0].replace(VRS_CODE['COMMAND_PREFIX'], '')
        for c in VRS_CODE['COMMANDS']:
            if c.name == a:
                the_command = c
        
        if the_command == None:
            return 'COMMAND_NOT_EXIST'
        if len(command_split) == 1 and len(the_command.args) > 0:
            return 'UNKNOWN_ARGUMENT'
    else:
        return 'END_EXECUTE'

    command_split = re.findall(total_re, command.replace(VRS_CODE['COMMAND_PREFIX'] + the_command.name, ''))

    completed_commands = []
    
    for bar in command_split:
        if re.findall(text_re, bar) != []:
            completed_commands.append('text')
        elif re.findall(number_re, bar) != []:
            completed_commands.append('number')
        else:
            return 'UNK_DATA_TYPE'

    all_text = re.findall(text_re, command.replace(VRS_CODE['COMMAND_PREFIX'] + the_command.name, ''))
    all_number = re.findall(number_re, command.replace(VRS_CODE['COMMAND_PREFIX'] + the_command.name, ''))

    j_text = len(all_text)
    j_number = len(all_number)
    complete_args = j_text + j_number

    i_text = 0
    i_number = 0

    saved_original_args = []
    for i in the_command.args:
        saved_original_args.append(i.value)

    for arg in range(0, complete_args):
        try:
            if the_command.args[arg].type_arg == 'any':
                if completed_commands[arg] == 'text':
                    the_command.args[arg].value = all_text[i_text].replace('\'', '')
                    i_text += 1
                else:
                    the_command.args[arg].value = float(all_number[i_number]) if re.search(r'(\-[0-9]+\.[0-9]+|[0-9]+\.[0-9]+)', all_number[i_number]) != None else int(all_number[i_number])
                    i_number += 1
        except:
            if the_command.more_args != False: 
                if the_command.more_args.type_arg == 'any':
                    if completed_commands[arg] == 'text':
                        the_command.more_args.value.append(all_text[i_text].replace('\'', ''))
                        i_text += 1
                    else:
                        the_command.more_args.value.append(float(all_number[i_number] if re.search(r'(\-[0-9]+\.[0-9]+|[0-9]+\.[0-9]+)', all_number[i_number]) != None else int(all_number[i_number])))
        try:
            if the_command.args[arg].type_arg == 'text':
                the_command.args[arg].value = all_text[i_text].replace('\'', '')
                i_text += 1
        except:
            if the_command.more_args != False: 
                if the_command.more_args.type_arg == 'text':
                    the_command.more_args.value.append(all_text[i_text].replace('\'', ''))
                    i_text += 1
        try:
            if the_command.args[arg].type_arg == 'number':
                the_command.args[arg].value = float(all_number[i_number]) if re.search(r'(\-[0-9]+\.[0-9]+|[0-9]+\.[0-9]+)', all_number[i_number]) != None else int(all_number[i_number])
                i_number += 1
        except:
            if the_command.more_args != False:
                if the_command.more_args.type_arg == 'number':
                    the_command.more_args.value.append(float(all_number[i_number]) if re.search(r'(\-[0-9]+\.[0-9]+|[0-9]+\.[0-9]+)', all_number[i_number]) != None else int(all_number[i_number])) 
                    i_number += 1

    for arg_ in the_command.args:
        if arg_.value == None:
            l = len(saved_original_args)
            s = 0
            while s < l:  
                for i in range(0, len(the_command.args)):
                    the_command.args[i].value = saved_original_args[s]
                    s += 1

            if the_command.more_args != False:
                the_command.more_args.value = []
                    
            return f'{arg_.name.upper()}_UNK_VALUE'

    the_command.exec()

    l = len(saved_original_args)
    s = 0
    while s < l:  
        for i in range(0, len(the_command.args)):
            the_command.args[i].value = saved_original_args[s]
            s += 1

    if the_command.more_args != False:
        the_command.more_args.value = []

    return 'END_EXECUTE'