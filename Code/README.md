Here the generic pipeline code for the LLM Integration of this Project. 


Pipeline_1.py is the Latest Basic one.


Pipeline_2.py is the Latest Iterative one - withe the LLM Prompt responsible for Single Invariant Benchmarks.


Pipeline_3.py is the is the Latest Iterative one - with the LLM Prompts dealing with Multiple Invariants or (Unknown Number of Invariants).


Pipeline_4.py is the is the Latest Iterative and Universal one - with the LLM Prompts dealing with Multiple Invariants or (Unknown Number of Invariants), Single Invariant, Absolute Invariant and Quantifiable Invariants.


Constrained_Universal_Pipeline.py is the Latest Iterative and Universal one but is Constrained by the Limited number of iterations per benchmark and without the removal of Parsing Errors. 


Universal_Pipeline_Double_Prompt_Regex.py is the Latest Iterative and Universal one that uses Regex alongside both Prompt types (constrained and unconstrained) with 1200s time limit per benchmark and 60 iterations limit per benchmark (30 for each benchmark). The Regex addition allows the Parsing errors to be removed/reduced and it increases the number of useful iterations per benchmark.


Prompt_Examples.py is the file containing four types of benchmark examples and how they are solved in a step by step explanation manner and approach.


Constrained_Prompts.py (in the code it is used as Prompt_Examples_2.py) is the file containing 3 types of Prompt Examples that will used when experimenting with the Code2Inv Benchmarks - contains Example + Output in the Chain of Thought Manner.


Stages of the Project: 

1. Detect For loops iteratively.
2. Ask the LLM to generate an invariant for each loop. 
3. Requirements:


   a. Good Selection of LLMs - for the sake of this prototype GPT 3.5 Turbo Instruct is being used (OpenAI).



   b. Good Prompting for LLMs (Reading the Prompt Engineering Paper(s) for further insight) - this is under development at the moment.
   
5. Ask the respective LLM to generate only loop invariants that are going to be placed before each loop.
6. Check whether the generated loop invariant can be parsed (implementation is done via using regular expressions); if the generated responses match the pattern defined through the regular expression then the rest of the pipeline will execute - otherwise it will regenerate and re-match until the match is successful) - this reduces the parsing errors and increases the number of useful iterations per benchmark.
7. Repeat for the next loop (multiple loops check is under development so current pipeline skips this step).
8. Once done, call ESBMC-Vampire.

---------------------------------------------------------------------------------------------------------------------------------------
Prompt Engineering: Chain of Thought Approach.

Give a Solved Example Benchmark to the LLM 

{
 C code with loop ...
} 

Correct Loop invariant is e.g. x>y

(Important Note: The following Step-by-step explanation is not used for Constrained Prompts; this is only for Unconstrained Prompts)

Explain in sequential steps as to why the invariant x>y is successful. 

(Note: Here you can ask the LLM to generate a sequential break down in order to understand and break down in steps why the invariant is correct - as the way it will break down and tell the user how and why this invariant is correct will work in the same way by feeding it that same information in that same style - as a prompt.) 

Then utilise the Benchmark that you need to generate the correct invariant(s) for:

{
   C code with loop ...
}

Then specify the conditions of the output and the form that the output will appear in plus any constraints or extra contextual information may help as well.



---------------------------------------------------------------------------------------------------------------------------------------

References: 

1. https://platform.openai.com/docs/api-reference
2. https://platform.openai.com/docs/guides/text-generation
3. https://platform.openai.com/docs/guides/prompt-engineering/strategy-write-clear-instructions
4. https://github.com/FrontAnalyticsInc/data-winners/blob/main/generation-api-openai/openai-text-generation-examples-in-python.ipynb
5. https://stackoverflow.com/questions/31126596/saving-response-from-requests-to-file
6. http://www.java2s.com/Code/Python/File/AddingLineNumberstoaPythonScript.htm
7. https://chat.openai.com/
8. https://stackoverflow.com/questions/48797580/how-to-add-line-numbers-in-a-list
9. https://docs.python.org/3/c-api/index.html
10. https://www.geeksforgeeks.org/python-os-path-join-method/
11. https://stackoverflow.com/questions/10377998/how-can-i-iterate-over-files-in-a-given-directory
12. https://mathai2023.github.io/papers/28.pdf
13. https://arxiv.org/pdf/2302.11382.pdf
14. https://stackoverflow.com/questions/19389490/how-do-pythons-any-and-all-functions-work
15. https://www.w3schools.com/python/ref_func_map.asp
16. https://stackoverflow.com/questions/65333658/how-to-join-values-of-map-in-python
17. https://docs.python.org/3/library/re.html
18. https://stackoverflow.com/questions/64173161/python-regular-expression-substitution-function-using-lambda-in-the-replacement
