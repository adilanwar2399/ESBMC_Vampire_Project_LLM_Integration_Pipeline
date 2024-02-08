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

