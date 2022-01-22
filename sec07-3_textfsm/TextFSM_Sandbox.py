#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import textfsm
import os


# In[ ]:


ls


# In[ ]:


def open_file(file_path):
    """
    Given a file path, this function verifies that the file path is valid
    and points to a file and then attempts to open the file and read
    in its contents as a string.
    
    file_path: File path to file.
    
    return: file_data_string: Function will retur the contents of the file
    in a string if sucessful, otherwise it will return an empty string.
    
    """
    print(f"Attempting to open file {file_path}")
    if os.path.isfile(file_path):
        with open(file_path) as f:
            file_data_string = f.read()
    else:
        print(f"File path provided is invalid. Verify that the file exists in the path provided.\nFailed to open {file_path}")
        file_data_string = ""
          
    return file_data_string


# In[ ]:


open_file("TestFailure.txt")


# In[ ]:


my_data = open_file("arista_sw01_show_ip_int_br_output.txt")


# In[ ]:


my_data


# In[ ]:


def textfsm_parser(template_fp, data_to_parse):

    """
    This function uses the provided template file path, template_fp, to parse the provided string of data, 
    data_to_parse.
    
    template_fp: The full file path to the template file or a template file in the local directory with this script.
    
    data_to_parse: String of data to parse. Typically the output of the show command which corresponds to the 
    TextFMS template being used.
    
    returns: fsm: The resulting parsed TextFSM object.
    
    Tip:  
    fsm.header provides the column headers for each "column" of data (positional element in the list)
    fsm._results provides the resulting list (same value as the variable result below)
    fsm.values provides the template values to parse out of the data (the regex for each column header)
    
    """
    
    if os.path.isfile(template_fp):
        print(f"Using TextFSM Template {template_fp}")
        with open(template_fp) as template_fh:
            # TextFSM method needs a file handle which is why we are not using our open_file function
            fsm = textfsm.TextFSM(template_fh)
            result = fsm.ParseText(my_data)
    else:
        print(f"ERROR! {template_fp} is not a valid file or not in the given path!")
        fsm = ""

    print(f"FSM Object fsm (basically the parsing template to use):\n{fsm}\n")
    print(f"FSM Object fsm.header:\n{fsm.header}\n")
    print(f"FSM Object fsm.values:\n{fsm.values}\n")
    print(f"FSM Object fsm._result:\n{fsm._result}\n")
    print(f"The contents of the result variable (same as fsm._result): \n{result}\n")
    print(f"FSM Object fsm.value_map:\n{fsm.value_map}\n")
    print("\ndir of fsm dir(fsm) to look at available methods from the TextFSM Object.")
    print(dir(fsm))
    
    # Returning the fsm object.  We could return result but that does not have a header.
    # The fsm object has the header in fsm.header and the results in fsm._result
    return fsm


# ### Lets parse our Arista show ip int brief output with the *arista_eos_show_ip_interface_brief.textfsm* TextFMS template

# In[ ]:


ip_table = textfsm_parser("arista_eos_show_ip_interface_brief.textfsm", my_data)


# In[ ]:


dir(ip_table)


# In[ ]:


help(ip_table)


# In[ ]:


ip_table.header


# In[ ]:


ip_table._result


# In[ ]:


ip_table.values


# In[ ]:


my_list = ip_table.values


# In[ ]:


len(my_list)


# In[ ]:


for line in my_list:
    print(line)


# ---
# ### Lets look at the ParseTextToDicts Method

# In[ ]:


with open("arista_eos_show_ip_interface_brief.textfsm") as template_fh:
    # TextFSM method needs a file handle which is why we are not using our open_file function
    fsm = textfsm.TextFSM(template_fh)
    result_dict = fsm.ParseTextToDicts(my_data)


# In[ ]:


result_dict


# In[ ]:


result_dict[0].keys()


# In[ ]:




