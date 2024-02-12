Here the generic pipeline code for the LLM Integration of this Project will be. 


Prompt_Eng_Pipeline.py is the Latest one.


Stages of the Project: 

1. Detect For loops iteratively.
2. Ask the LLM to generate an invariant for each loop. 
3. Requirements:


   a. Good Selection of LLMs - for the sake of this prototype GPT 3.5 Turbo is being used (OpenAI).



   b. Good Prompting for LLMs (Reading the Prompt Engineering Paper(s) for further insight) - this is under development at the moment.
   
5. Ask the respective LLM to generate only loop invariants that are going to be placed before each loop.
6. Repeat for the next loop.
7. Once done, call ESBMC-Vampire.

---------------------------------------------------------------------------------------------------------------------------------------
Prompt Engineering: Chain of Thought Approach.

Give a Solved Example Benchmark to the LLM 

{
 C code with loop ...
} 

Correct Loop invariant is e.g. x>y

Explain in sequential steps as to why the invariant x>y is successful. 

(Note: Here you can ask the LLM to generate a sequential break down in order to understand and break down in steps why the invariant is correct - as the way it will break down and tell the user how and why this invariant is correct will work in the same way by feeding it that same information in that same style - as a prompt.)

Then utilise the Benchmark that you need to generate the correct invariant(s) for:

{
   C code with loop...
}

Then specify the conditions of the output and the form that the output will appear in plus any constraints or extra contextual information may help as well.



---------------------------------------------------------------------------------------------------------------------------------------

References: 

1. https://platform.openai.com/docs/api-reference
2. https://stackoverflow.com/questions/31126596/saving-response-from-requests-to-file
3. http://www.java2s.com/Code/Python/File/AddingLineNumberstoaPythonScript.htm
4. https://chat.openai.com/
5. https://stackoverflow.com/questions/48797580/how-to-add-line-numbers-in-a-list
6. https://docs.python.org/3/c-api/index.html
7. https://www.geeksforgeeks.org/python-os-path-join-method/
8. https://stackoverflow.com/questions/10377998/how-can-i-iterate-over-files-in-a-given-directory
