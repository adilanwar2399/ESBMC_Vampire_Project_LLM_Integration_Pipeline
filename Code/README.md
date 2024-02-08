Here the generic pipeline code for the LLM Integration of this Project will be. 


Prompt_Eng_Pipeline.py is the Latest one.


Stages of the Project: 

1. Detect For loops iteratively - parse the goto language and the parse will replace the loop with the loop invariant like LLVM.
2. Ask the LLM to generate an invariant for each loop. 
3. Requirements:


   a. Good Selection of LLMs



   b. Good Prompting for LLMs (Reading the Prompt Engineering Paper(s) for further insight).
   
5. Ask the respective LLM to generate only loop invariants that are going to be placed before each loop.
6. Repeat for the next loop.
7. Once done, call ESBMC-Vampire.

