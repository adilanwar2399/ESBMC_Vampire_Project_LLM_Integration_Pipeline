Here the generic pipeline code for the LLM Integration of this Project will be. 


Prompt_Eng_Pipeline.py is the Latest one.


Stages of the Project: 

1. Detect For loops iteratively.
2. Ask the LLM to generate an invariant for each loop. 
3. Requirements:


   a. Good Selection of LLMs - for the sake of this prototype GPT 3.5 Turbo is being used OpenAI.



   b. Good Prompting for LLMs (Reading the Prompt Engineering Paper(s) for further insight) - this is under development at the moment.
   
5. Ask the respective LLM to generate only loop invariants that are going to be placed before each loop.
6. Repeat for the next loop.
7. Once done, call ESBMC-Vampire.

---------------------------------------------------------------------------------------------------------------------------------------

References: 

1. https://platform.openai.com/docs/api-reference
2. https://stackoverflow.com/questions/31126596/saving-response-from-requests-to-file
3. http://www.java2s.com/Code/Python/File/AddingLineNumberstoaPythonScript.htm
4. https://chat.openai.com/
5. https://stackoverflow.com/questions/48797580/how-to-add-line-numbers-in-a-list
6. https://docs.python.org/3/c-api/index.html
