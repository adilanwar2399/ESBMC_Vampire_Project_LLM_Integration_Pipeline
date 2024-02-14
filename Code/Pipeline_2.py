##################################################################################
###################### Code By Muhammad Pirzada ##################################
##################################################################################

import openai
import os
import subprocess 
import time

# Set your OpenAI GPT-3.5 Turbo API key (Unique to the user account)
key_for_the_API = 'Your API Key'
openai.api_key = key_for_the_API

# Path to the C files that will be experimented with.
c_benchmarks = '<PATH to Benchmarks>'

# Check to see i nthe directory which files are C files.
for name_of_the_c_benchmark_file in os.listdir(c_benchmarks):
    if name_of_the_c_benchmark_file.endswith('.c'):
        # Number of generated invariant(s) iterations from the LLM (GPT-3 Turbo Instruct).
        invariant_generation_iteration = 1; 
        while True:
            # Check the specific file name in the specific directory and read it.
            with open(os.path.join(c_benchmarks, name_of_the_c_benchmark_file), 'r') as benchmark_read:
                c_benchmark = benchmark_read.read()

            # Here the respective C benchmark gets split into a line array 
            # via splitting the respective string on the new line operator.
            line_numbered_code = c_benchmark.split('\n') 

            # Here for each line checks if line.stripwhitespace.startswith(while or for) 
            # and store the line number (index into line array).
            for position_index, line in enumerate(line_numbered_code):
                if line.strip().startswith(('while', 'for')): 
                    # Insert a new index into the array at the line number and 
                    # populate it with the string "// Line A"
                    line_numbered_code.insert(position_index, "// Line A")
                    break

            # Here the line array respectively turns back into a string to use in the prompt.
            unmodified_code = '\n'.join(line_numbered_code)
            print (unmodified_code)

            # Here the Definition of the prompt occurs using, Stanford LEMUR Teams SVCOMP Benchmark Example + their Prompt for understanding
            # seen in paper: https://arxiv.org/pdf/2310.04870v2.pdf:

            # Here two prompts are utilised one for potential position the invariants 
            # in the place where they should be going i.e. before the loops 
            # (so that eventually if they are valid and they do hold then they can replace the loops).
            # Note: the second prompt is for the actual code generation of the loop invariants,
            # respective to their benchmark(s).
            # prompt= "Modify this following C code and place the invariants before the while(...) or the for(...) loop in the code that will be verified using ESBMC: \n\n"
            code_modifying_prompt = """
            "
            extern void abort(void);
            extern void __assert_fail(const char *, const char *, unsigned int, const char *) __attribute__ ((__nothrow__ , __leaf__)) __attribute__ ((__noreturn__));
            void reach_error() { __assert_fail("0", "vnew2.c", 3, "reach_error"); }
            extern void abort(void);
            void assume_abort_if_not(int cond) {
              if(!cond) {abort();}
            }
            void __VERIFIER_assert(int cond) {
              if (!(cond)) {
                ERROR: {reach_error();abort();}
              }
              return;
            }

            #define FORALL(Var, Type, Cond)       \
              Type Var;                           \
              __invariant(__forall(Var, Cond));   \

            #define EXISTS(Var, Type, Cond)       \
              Type Var;                           \
              __invariant(__exists(Var, Cond));   \

            int __VERIFIER_nondet_int();

            int main()
            {
                int x = 0;
                int y = __VERIFIER_nondet_int();
                int z = __VERIFIER_nondet_int();

                __invariant(x == 0 || z >= y);

                while(x < 5) {
                   x += 1;
                   if( z <= y) {
                      y = z;
                   }
                }

                __VERIFIER_assert (z >= y);
            }

            "

            The invariant, __invariant(x==0 || z>=y);, holds in this while loop because of the following step by step explanation,
            "
                The Initialization:
                    At the beginning of the loop:
                        x is initialized to 0.
                        y and z are assigned nondeterministic integer values.
                    Invariant holds:
                        x == 0 is true initially.
                        Since y and z are arbitrary, z >= y may or may not hold initially.

                The Base Case (Inductive Base):
                    Assumption:
                        Assume the invariant x == 0 || z >= y holds at the start of an arbitrary iteration.

                The Inductive Step comprises of the following:
                    Analysis within the Iteration:
                        x increments by 1.
                        If z <= y, y is updated to z.
                        Thus, x increases monotonically, and y either decreases or remains the same.
                    The End of Iteration:
                        The loop terminates when x reaches 5.
                        If x is now 5, it satisfies x == 0.
                        If x is not 5, the loop continues, and the invariant is still maintained.
                        If z >= y held initially, it's either maintained or strengthened due to the loop's logic. If z <= y, y is updated to z, implying z >= y.
                    The Conclusion:
                        The invariant holds at the end of the iteration if it holds at the beginning.

                The Termination:
                    The loop terminates when x becomes 5.
                    At loop termination, either x == 0 or z >= y holds.
                    Therefore, the invariant x == 0 || z >= y holds upon loop termination.

                The Overall Conclusion:
                    The loop invariant x == 0 || z >= y is maintained throughout the loop execution.
                    This ensures that the assertion __VERIFIER_assert(z >= y) is valid as it aligns with the loop invariant.

            In summary, the step-by-step explanation clarifies how the loop invariant holds true from initialization through each iteration until termination, ensuring the correctness of the assertion in relation to the loop's behavior
            “. 

            Based on the example provided above can you generate an C invariant for the following code,
            "
            \n""" + c_benchmark + """\n

            "
            Print an invariant for this loop that holds in the form '__invariant(...);' . 
            They should help prove the assertions. You can utilise '&&' or '||' if required. 
            No explanation. Your answer should be in the form '__invariant(…);'

            """
            #print(code_modifying_prompt)

            # Here is the use of the OpenAI GPT-3.5 Turbo API to generate code unspecified completion and randomness.
            response = openai.Completion.create(
                engine="gpt-3.5-turbo-instruct",
                prompt=code_modifying_prompt,
                max_tokens=1000,
                # temperature=0.5, # To determine the randomness of the solution generated.
            )

            # Here the generated modified code will be obtained.
            generated_modified_code = response['choices'][0]['text'].strip()
            print (generated_modified_code)

            # Here the insertion of the LLM Gpt-3.5 Turbo generated invariant(s) will take place.
            invariant_insertion = unmodified_code.split('\n')

            # LLM produced the invariants and they get inserted 
            # in the appropriate line number of the the respective line array.
            for insertion_index, line in enumerate(invariant_insertion):
                if '// Line' in line:
                    invariant_insertion.insert(insertion_index+1, generated_modified_code)
                    break

            # New modified program is ready to be used by ESBMC and Vampire after C file conversion.
            new_modified_code  = '\n'.join(invariant_insertion)

            print(new_modified_code)

            # Here the respective generated C code will be saved as a new file.
            # Note: w is for the respective write mode.
            with open("new_modified_code.c", "w") as file:
                file.write(new_modified_code)

            # Here the specific pathway to the respective ESBMC executable is used.
            esbmc_executable_path = "<PATH to ESBMC>"  

            # Here is the respective command to ensure that  the esbmc executable,
            # and the respective newly generated modified code are linked and so that they 
            # can be processed together when ran with ESBMC + Automated Theorem Prover Vampire too.
            esbmc_command = [esbmc_executable_path, "new_modified_code.c"]

            # Below is the vampire executable path addition of the output file too - this is stored as an array.
            vampire_executable_path_addition = "<PATH to VAMPIRE>".split(" ")

            # Below is the vampire executable command to allow esbmc and vampire to run together with each other on the c file.
            vampire_executable_command = [*esbmc_command, *vampire_executable_path_addition]

            # Now, here is the subprocess allows the subprocess to call esbmc on the modified C code file.
            run_esbmc_with_script = subprocess.run(vampire_executable_command, capture_output=True, text=True)

            # These will respectively output either verification successful or unsuccessful, 
            # depending on whether or not ESBMC successfully runs.
            if run_esbmc_with_script.returncode !=0: 
                print("ESMBC + Vampire execution has encountered an error")
                print(run_esbmc_with_script.stderr)
                print("Code Generation is occurring again")
                print("Generated Invariant Number: ", invariant_generation_iteration)
                invariant_generation_iteration+=1
                time.sleep(1)
            else: 
                print("ESBMC + Vampire ran SUCCESSFULLY")
                print("Generated Successful Invariant on Iteration Number: ", invariant_generation_iteration)
                print(run_esbmc_with_script.stdout)
                break

