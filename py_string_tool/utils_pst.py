from difflib import get_close_matches
from difflib import SequenceMatcher
from thefuzz import fuzz
from typing import Union, Literal
import pandas as pd
from typing import List, Tuple, Literal, Any

# def similar_score(word_in, compare_list, cut_off=0,return_word=True,return_score=False):
#     # Assume that word_in is only string
#     from thefuzz import fuzz
#     outlist = []
#     for text in compare_list:
#         similar_score = fuzz.WRatio(word_in,text)
#         string_similar = (text,similar_score)
#         outlist.append(string_similar)
#     outlist.sort(key = lambda x:x[1],reverse=True)
#     return outlist


def text_between(
        texts: Union[str,List[str]],
        prefixes: Union[str, List[str]],
        suffixes: Union[str, List[str]],
        include_start_delim: bool = False,
        include_end_delim: bool = False,
        return_as_empty: bool = True
    ) -> List[str]:
    # medium tested
    # seems to work when suffix is empty string("") now
    # include_start_delim & include_end_delim True seems to also work

    # still not tested when prefix is empty string("")
    def _text_between_h1(
        text: str,
        prefixes: Union[str, List[str]],
        suffixes: Union[str, List[str]],
        include_start_delim: bool = False,
        include_end_delim: bool = False,
        return_as_empty: bool = True
    ) -> str:
        import re
        """
        Extracts the text between specified prefixes and suffixes.

        Parameters
        ----------
        text : str
            The input text to search within.
        prefixes : Union[str, List[str]]
            A single prefix or a list of prefixes to search for.
        suffixes : Union[str, List[str]]
            A single suffix or a list of suffixes to search for.
        include_start_delim : bool, optional
            If True, include the prefix in the result.
        include_end_delim : bool, optional
            If True, include the suffix in the result.
        return_as_empty : bool, optional
            If True, return an empty string if no match is found.
            If False, return None if no match is found.

        Returns
        -------
        str
            The extracted text between the specified prefixes and suffixes.
        """
        if isinstance(prefixes, str):
            prefixes_in = [prefixes]
        else:
            prefixes_in = list(prefixes)
        if isinstance(suffixes, str):
            suffixes_in = [suffixes]
        else:
            suffixes_in = list(suffixes)

        # sort prefixes and suffixes to make sure that "" is the last option to match
        prefixes_in = sorted(prefixes_in, key=lambda x: x == "")
        suffixes_in = sorted(suffixes_in, key=lambda x: x == "")

        for prefix in prefixes_in:
            for suffix in suffixes_in:
                pattern = re.escape(prefix) + "(.*?)" + re.escape(suffix)
                match = re.search(pattern, text)
                if match:
                    start, end = match.span(1)
                    if include_start_delim:
                        start = match.start(0)
                    if include_end_delim:
                        end = match.end(0)
                    
                    if prefix == "":
                        start = 0
                    if suffix == "":
                        end = len(text)

                    out_str = text[start:end]
                    return out_str

        return "" if return_as_empty else text

    if isinstance(texts, str):
        texts_in = [texts]
    else:
        texts_in = list(texts)

    out_list = []
    for text in texts_in:
        ans_str = _text_between_h1(text, prefixes, suffixes, include_start_delim, include_end_delim, return_as_empty)
        out_list.append(ans_str)
        
    return out_list


def similar_score(
        text:str
        ,compare_list:List[str]
        ,cut_off:float = 0
        ,return_word:bool = True
        ,return_score:bool = False
        ,score_engine:Literal["thefuzz","rapidfuzz"] = "rapidfuzz"
        ):
    # Assume that word_in is only string
    # from thefuzz import fuzz
    import thefuzz.fuzz
    import rapidfuzz.fuzz
    outlist = []
    for text in compare_list:
        similar_score_thefuzz = thefuzz.fuzz.WRatio(text,text)
        similar_score_rapidfuzz = rapidfuzz.fuzz.WRatio(text,text)

        if score_engine in ["thefuzz"]:
            string_similar = (text,similar_score_thefuzz)
        elif score_engine in ["rapidfuzz"]:
            string_similar = (text,similar_score_rapidfuzz)
        else:
            raise ValueError("score_engine should be 'thefuzz' or 'rapidfuzz'")
        
        outlist.append(string_similar)
    outlist.sort(key = lambda x:x[1],reverse=True)
    return outlist



def similar_text(
        texts: str| list[str]
        , compare_list:list[str]
        , cut_off:float = 0
        ,return_word:bool = True
        ,return_score:bool = False):
    score_list = []
    similar_word = []
    if isinstance(texts,str):
        # if word_in is only a string
        word_list = [texts]
    else:
        # if this is a list
        word_list = [word for word in texts]
    
    for word in word_list:
        max_score = 0
        most_similar = ""
        for compare_word in compare_list:
            score = SequenceMatcher(None, str(word), compare_word).ratio()
            if score > max_score:
                max_score = score
                most_similar = compare_word
            if max_score >= cut_off:
                score_list.append(format(max_score,".4f"))
                similar_word.append(most_similar)
            else:
                score_list.append("")
    
    if return_word:
        if return_score:
            # return both word & score

            if isinstance(texts,str):
                out_list = list(zip(similar_word,score_list))[0]
                if len(similar_word) == 0:
                    return ""
            else:
                if len(similar_word) == 0:
                    return []
                out_list = list(zip(similar_word,score_list))
        else:
            # return only word
            out_list = similar_word
            
            if isinstance(texts,str):
                if len(similar_word) == 0:
                    return ""
                out_list = similar_word[0]
            else:
                if len(similar_word) == 0:
                    return []
                out_list = similar_word
    else:
        if return_score:
            # return only score
            
            if isinstance(texts,str):
                out_list = score_list[0]
            else:
                out_list = score_list

        else:
            out_list = "Invalid! return_word & return_score can't be False at the same time"

    return out_list

def split_sentence(text, delimiter, inplace=True):
    """
    Split elements of a list of strings using a specified delimiter and optionally modify the list in place.

    Parameters
    ----------
    text : list of str
        List of strings to be split.
        
    delimiter : str
        The delimiter to use for splitting each string in the list.
        
    inplace : bool, default True
        If True, modifies the original list `text` in place and returns None.
        If False, creates a copy of the list, modifies the copy, and returns the modified list.

    Returns
    -------
    list of str or None
        If `inplace` is False, returns a new list with the split and trimmed strings.
        If `inplace` is True, modifies the original list in place and returns None.

    Notes
    -----
    - The function trims leading and trailing spaces from each string before and after splitting.
    - Empty strings resulting from the split are not included in the final list.
    - If `inplace` is True, the function operates on the original list and does not return a new list.
    - If `inplace` is False, the function operates on a copy of the list and returns the modified copy.

    Examples
    --------
    >>> text = ["Hello, world", "Python is great"]
    >>> St_SplitSentence(text, ",", inplace=False)
    ['Hello', 'world', 'Python is great']
    
    >>> text = ["Hello, world", "Python is great"]
    >>> St_SplitSentence(text, " ", inplace=True)
    >>> text
    ['Hello,', 'world', 'Python', 'is', 'great']
    """
    if not inplace:
        text_in = text.copy()
        
    i = 0
    while i < len(text_in):
        text_in[i] = text_in[i].strip()  # Trim the spaces at both ends
        if delimiter in text_in[i]:
            # Split the string using the delimiter
            split_strings = text_in[i].split(delimiter)
            
            # Remove the original string from the list
            del text_in[i]
            
            # Insert the split strings back into the original list at the same position
            for split_str in reversed(split_strings):
                split_str = split_str.strip()  # Remove leading and trailing spaces
                if split_str:  # Only add non-empty strings
                    text_in.insert(i, split_str)
        else:
            i += 1  # Only increment if no split occurred to handle new inserted strings
            
    return text_in if not inplace else None

def remove_from_list(lst, char="♪"):
    # Function to remove elements that start with a specific character (in this case "♪")
    # can generalize more to 
    # remove_from_list(lst,start_with = None,end_with = None,logic = "or")
    return [element for element in lst if not str(element).startswith(char)]

def text_after(text, prefix_list, return_as_empty=True, include_delimiter=False):
    if isinstance(prefix_list, str):
        prefix_list = [prefix_list]
    
    for prefix in prefix_list:
        index = text.find(prefix)
        if index != -1:
            out_str = text[index + len(prefix):]
            if include_delimiter:
                out_str = prefix + out_str
            return out_str

    if return_as_empty:
        return ""
    else:
        return text

def text_before(text, suffix_list: Union[str, List[str]], return_as_empty=True, include_delimiter=False) -> str:
    if isinstance(suffix_list, str):
        suffix_list = [suffix_list]
    
    for suffix in suffix_list:
        index = text.find(suffix)
        if index != -1:
            out_str = text[:index + len(suffix)]
            if include_delimiter:
                out_str = suffix + out_str
            return out_str

    if return_as_empty:
        return ""
    else:
        return text


def replace(
        text:str,to_replace:Union[str,List[str]],replace_by:str):
    # unit_tested
    new_text: str = text
    for word in to_replace:
        new_text = new_text.replace(word, replace_by)
        
    return new_text

def num_format0(num: float|int, max_num: None|float|int = None, digit: None|int =None):

    """
    Format a number with leading zeros based on the specified maximum number or digit count.
    
    Parameters
    ----------
    num : int or str
        The number to be formatted.
        
    max_num : int or None, optional
        If provided, the number will be zero-padded to match the length of this number.
        
    digit : int or None, optional
        If provided and `max_num` is None, the number will be zero-padded to this digit count.
    
    Returns
    -------
    str
        The formatted number as a string with leading zeros if applicable.
    
    Notes
    -----
    - If both `max_num` and `digit` are None, the number is returned as a string without additional zeros.
    - If `max_num` is provided, it takes precedence over `digit`.
    """
    
    # chatgpt solo
    # tested

    if max_num is not None:
        # Zero-pad `num` to match the length of `max_num`
        num_str = str(num).zfill(len(str(max_num)))
    elif digit is not None:
        # Zero-pad `num` to the specified `digit` count
        num_str = str(num).zfill(digit)
    else:
        # Return `num` as a string without zero-padding
        num_str = str(num)
    
    return num_str

def format_index_num(to_format_num, total_num):
    # imported from C:/Users/Heng2020/OneDrive/D_Code/Python/Python NLP/NLP 02/NLP_2024/NLP 11_Local_TTS
    # tested via pd_split_into_dict_df
    # adding leading 0 to the number
    # Determine the number of digits in the largest number
    total_digits = len(str(total_num))
    
    # Format the number with leading zeros
    formatted_num = f"{to_format_num:0{total_digits}d}"
    
    return formatted_num

def clean_filename(ori_name):
    # update01: deal with '\n' case
    # imported from NLP 01/NLP 03_11LabsBulk
    # EDIT: remove dots from replace_with_empty
    replace_with_empty = ["?",":",'"' , "\\","*", '"', "<", ">", "|" ] 
    replace_with_space = ["\n", "/" ]
    
    new_name = ori_name
    for delimiter in replace_with_empty:
        new_name = new_name.replace(delimiter, "")
        
    for delimiter in replace_with_space:
        new_name = new_name.replace(delimiter, " ")

    return new_name

def replace_backslash(s: str):
    return s.replace('\\','/')

def detect_language(texts: Union[str,list[str],pd.Series], 
                    return_as: Literal["full_name","2_chr_code","3_chr_code","langcodes_obj"] = "full_name"):
    import pandas as pd
    from langdetect import detect
    import langcodes
    # medium tested
    # wrote < 30 min(with testing)
    # imported from C:\Users\Heng2020\OneDrive\D_Code\Python\Python NLP\NLP 02\NLP_2024\NLP 11_Local_TTS
    if isinstance(texts, str):
    # assume only 1d list
        try:
            # Detect the language of the text
            # language_code is 2 character code
            lang_code_2chr = detect(texts)
            language_obj = langcodes.get(lang_code_2chr)
            language_name = language_obj.display_name()
            lang_code_3chr = language_obj.to_alpha3()

            
            if return_as in ["full_name"]:
                ans = language_name
            elif return_as in ["2_chr_code"]:
                ans = lang_code_2chr
            elif return_as in ["3_chr_code"]:
                ans = lang_code_3chr
            elif return_as in ["langcodes_obj"]:
                ans = language_obj

            return ans
        except Exception as e:
            err_str = f"Language detection failed: {str(e)}"
            return False
        
    elif isinstance(texts, list):
        out_list = []
        for text in texts:
            detect_lang = detect_language(text, return_as = return_as)
            out_list.append(detect_lang)
        return out_list
    elif isinstance(texts, pd.Series):
        # not tested this part yet
        unique_text = pd.Series(texts.unique())
        full_text = unique_text.str.cat(sep=' ')
        detect_lang = detect_language(full_text,return_as)
        return detect_lang

def similar_score(text:str, compare_list, cut_off=0,return_word=True,return_score=False):
    # Assume that word_in is only string
    outlist = []
    for text in compare_list:
        similar_score = fuzz.WRatio(text,text)
        string_similar = (text,similar_score)
        outlist.append(string_similar)
    outlist.sort(key = lambda x:x[1],reverse=True)
    return outlist



def similar_string(
        texts: str|list[str]
        , compare_list: list[str]
        , cut_off:float|int = 0
        ,return_word:bool = True
        ,return_score:bool = False):
    score_list = []
    similar_word = []
    if isinstance(texts,str):
        # if word_in is only a string
        word_list = [texts]
    else:
        # if this is a list
        word_list = [word for word in texts]
    
    for word in word_list:
        max_score = 0
        most_similar = ""
        for compare_word in compare_list:
            score = SequenceMatcher(None, str(word), compare_word).ratio()
            if score > max_score:
                max_score = score
                most_similar = compare_word
            if max_score >= cut_off:
                score_list.append(format(max_score,".4f"))
                similar_word.append(most_similar)
            else:
                score_list.append("")
    
    if return_word:
        if return_score:
            # return both word & score

            if isinstance(texts,str):
                out_list = list(zip(similar_word,score_list))[0]
                if len(similar_word) == 0:
                    return ""
            else:
                if len(similar_word) == 0:
                    return []
                out_list = list(zip(similar_word,score_list))
        else:
            # return only word
            out_list = similar_word
            
            if isinstance(texts,str):
                if len(similar_word) == 0:
                    return ""
                out_list = similar_word[0]
            else:
                if len(similar_word) == 0:
                    return []
                out_list = similar_word
    else:
        if return_score:
            # return only score
            
            if isinstance(texts,str):
                out_list = score_list[0]
            else:
                out_list = score_list

        else:
            out_list = "Invalid! return_word & return_score can't be False at the same time"

    return out_list

def contain_num(text: bool|str|int|float|None):
    if isinstance(text,bool) or text is None:
        return False
    if isinstance(text,(int,float)):
        return True
    return any(char.isnumeric() for char in text)

def text_after(texts:str|list[str], prefix_list, return_as_empty=True, include_delimiter=False):
    if isinstance(prefix_list, str):
        prefix_list = [prefix_list]
    
    for prefix in prefix_list:
        index = texts.find(prefix)
        if index != -1:
            out_str = texts[index + len(prefix):]
            if include_delimiter:
                out_str = prefix + out_str
            return out_str

    if return_as_empty:
        return ""
    else:
        return texts

def text_before(texts:str|list[str], suffix_list: Union[str, List[str]], return_as_empty=True, include_delimiter=False) -> str:
    if isinstance(suffix_list, str):
        suffix_list = [suffix_list]
    
    for suffix in suffix_list:
        index = texts.find(suffix)
        if index != -1:
            out_str = texts[:index + len(suffix)]
            if include_delimiter:
                out_str = suffix + out_str
            return out_str

    if return_as_empty:
        return ""
    else:
        return texts



def replace_last(text: str, oldvalue, newvalue):
    last_comma_index = text.rfind(oldvalue)
    if last_comma_index != -1:
        text = text[:last_comma_index] + newvalue + text[last_comma_index + 1:]
    return text

def is_empty_string(text:str):
    # Returns True if the string is empty or whitespace, False otherwise
    # imported from "C:\Users\Heng2020\OneDrive\Python NLP\NLP 08_VocabList\VocatList_func01.py"
    return not text.strip()

def not_empty_string(text):
    # Returns False if the string is empty or whitespace, True otherwise
    # imported from "C:\Users\Heng2020\OneDrive\Python NLP\NLP 08_VocabList\VocatList_func01.py"
    return text.strip()

def get_num(
    texts:str|list[str]
    ,exclude:str|list[str] = "" 
    ,begin_with_num:bool = False 
        ) -> Union[int,float,list[int|float]]:
    
    if isinstance(texts,str):
        return get_num_from_text(texts,exclude,begin_with_num)
    elif isinstance(texts,list):
        return [get_num_from_text(text,exclude,begin_with_num) for text in texts]

def get_num_from_text(
        text:str|float|int    
        ,exclude:str|list[str] = ""
        , begin_with_num:bool = False):
    # little tested
    import re
    
    """
    This function extracts the number part of a string.

    Parameters
    ----------
    string : str
        The input string to extract the number from.

    Returns
    -------
    num : int or float or None
        The extracted number as an integer or a floating-point value, or None if no number is found.
    """
    # Import the regular expression module
    if isinstance(exclude, str):
        if exclude != "":
            exclude_ = [exclude]
        else:
            exclude_ = []
    else:
        exclude_ = exclude
    
    for pattern in exclude_:
        if pattern in text:
            return False
    
    if begin_with_num:
        try:
            num = int(text[0])
        except ValueError:
            return False
    
    
    

    # Find the first occurrence of a number in the string using a regular expression
    # The regular expression allows an optional minus sign before the digits and an optional decimal part
    match = re.search(r'-?\d+(\.\d+)?', text)
    

    # If a match is found, convert it to a float and then to an int if possible
    if match:
        num = float(match.group())
        # Check if the number has a decimal part
        if num.is_integer():
            # Convert to an int and return it
            num = int(num)
            return num
        else:
            # Return the float as it is
            return num

    # If no match is found, return None
    else:
        return False