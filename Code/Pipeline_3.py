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


c_benchmarks = '<PATH to Benchmarks>'

#Loop over all the Benchmarks - file by file.
for name_of_the_c_benchmark_file in os.listdir(c_benchmarks):
    if name_of_the_c_benchmark_file.endswith('.c'):
        invariant_generation_iteration = 1; 
        while True:

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

            if invariant_generation_iteration <2:

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

                    int main() {
                      // variable declarations
                      int i;
                      int size = __VERIFIER_nondet_int();
                      int sn;
                      // pre-conditions
                      (sn = 0);
                      (i = 1);
                      // loop body
                      __invariant(sn == i - 1);
                      __invariant(sn == 0  || size >= 0);
                      __invariant(size < 0 || i <= size + 1);
                      while ((i <= size)) {
                        {
                        (i  = (i + 1));
                        (sn  = (sn + 1));
                        }

                      }
                      // post-condition
                    if ( (sn != 0) )
                    __VERIFIER_assert( (sn == size) );

                    }
                    "
                    Below is a step by step explanation of why these invariants holds in the loop provided:

                    1. `__invariant(sn == i - 1);`

                       This invariant asserts that the variable `sn` is always equal to the variable `i - 1`. In other words, it ensures that the value of `sn` is always one less than the value of `i`. 

                       Step-by-step explanation:
                       - Initially, before entering the loop, `sn` is initialized to 0 and `i` is initialized to 1. So, `sn` is indeed one less than `i`.
                       - Inside the loop, both `i` and `sn` are incremented by 1 in each iteration. Since `sn` is always assigned the value of `i - 1`, this relationship is maintained throughout the loop.
                       - Therefore, this invariant holds true throughout the execution of the loop.

                    2. `__invariant(sn == 0 || size >= 0);`

                       This invariant asserts that either `sn` is equal to 0 or `size` is greater than or equal to 0. In other words, it ensures that either `sn` is 0 or `size` is non-negative.

                       Step-by-step explanation:
                       - Initially, before entering the loop, `sn` is initialized to 0. Since `sn` is 0, this part of the invariant holds true.
                       - Regarding the second part, `size` is assigned a non-deterministic value using `__VERIFIER_nondet_int()`, which means it could be any integer value including negative, zero, or positive.
                       - Since `size` is assigned a non-negative value, `size >= 0` holds true.
                       - Therefore, this invariant holds true throughout the execution of the loop.

                    3. `__invariant(size < 0 || i <= size + 1);`

                       This invariant asserts that either `size` is negative or `i` is less than or equal to `size + 1`. In other words, it ensures that either `size` is negative or `i` doesn't exceed `size + 1`.

                       Step-by-step explanation:
                       - Initially, before entering the loop, `i` is initialized to 1, and `size` is assigned a non-deterministic value. Since we have no information about the value of `size`, this invariant holds trivially before the loop.
                       - Inside the loop, `i` is incremented by 1 in each iteration, and `size` remains constant. Therefore, if `size` is negative, `size < 0` holds true, which satisfies the invariant. If `size` is non-negative, `i` is guaranteed to be less than or equal to `size + 1` because the loop condition ensures that `i` doesn't exceed `size`. Hence, this part of the invariant also holds true.
                       - Therefore, this invariant holds true throughout the execution of the loop.

                        In summary, the step-by-step explanation clarifies how each loop invariant holds true from initialization through each iteration until termination, ensuring the correctness of the assertion in relation to the loop's behaviour.
                        “. 

                    Based on the example provided above can you generate an C invariant for the following code,
                    “
                    \n""" + c_benchmark + """\n
                    "
                    Print an invariant for this loop that hold in the form '__invariant(...);' . 
                    They should help prove the assertions. You can utilise '&&' or '||' if required. 
                    No explanation. Your answer should be in the form '__invariant(…);'

                    """

                #print(code_modifying_prompt)
            elif invariant_generation_iteration == 2 and invariant_generation_iteration<4: 
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

                int main() {
                  // variable declarations
                  int i;
                  int size = __VERIFIER_nondet_int();
                  int sn;
                  // pre-conditions
                  (sn = 0);
                  (i = 1);
                  // loop body
                  __invariant(sn == i - 1);
                  __invariant(sn == 0  || size >= 0);
                  __invariant(size < 0 || i <= size + 1);
                  while ((i <= size)) {
                    {
                    (i  = (i + 1));
                    (sn  = (sn + 1));
                    }

                  }
                  // post-condition
                if ( (sn != 0) )
                __VERIFIER_assert( (sn == size) );

                }
                "
                Below is a step by step explanation of why these invariants holds in the loop provided:

                1. `__invariant(sn == i - 1);`

                   This invariant asserts that the variable `sn` is always equal to the variable `i - 1`. In other words, it ensures that the value of `sn` is always one less than the value of `i`. 

                   Step-by-step explanation:
                   - Initially, before entering the loop, `sn` is initialized to 0 and `i` is initialized to 1. So, `sn` is indeed one less than `i`.
                   - Inside the loop, both `i` and `sn` are incremented by 1 in each iteration. Since `sn` is always assigned the value of `i - 1`, this relationship is maintained throughout the loop.
                   - Therefore, this invariant holds true throughout the execution of the loop.

                2. `__invariant(sn == 0 || size >= 0);`

                   This invariant asserts that either `sn` is equal to 0 or `size` is greater than or equal to 0. In other words, it ensures that either `sn` is 0 or `size` is non-negative.

                   Step-by-step explanation:
                   - Initially, before entering the loop, `sn` is initialized to 0. Since `sn` is 0, this part of the invariant holds true.
                   - Regarding the second part, `size` is assigned a non-deterministic value using `__VERIFIER_nondet_int()`, which means it could be any integer value including negative, zero, or positive.
                   - Since `size` is assigned a non-negative value, `size >= 0` holds true.
                   - Therefore, this invariant holds true throughout the execution of the loop.

                3. `__invariant(size < 0 || i <= size + 1);`

                   This invariant asserts that either `size` is negative or `i` is less than or equal to `size + 1`. In other words, it ensures that either `size` is negative or `i` doesn't exceed `size + 1`.

                   Step-by-step explanation:
                   - Initially, before entering the loop, `i` is initialized to 1, and `size` is assigned a non-deterministic value. Since we have no information about the value of `size`, this invariant holds trivially before the loop.
                   - Inside the loop, `i` is incremented by 1 in each iteration, and `size` remains constant. Therefore, if `size` is negative, `size < 0` holds true, which satisfies the invariant. If `size` is non-negative, `i` is guaranteed to be less than or equal to `size + 1` because the loop condition ensures that `i` doesn't exceed `size`. Hence, this part of the invariant also holds true.
                   - Therefore, this invariant holds true throughout the execution of the loop.

                    In summary, the step-by-step explanation clarifies how each loop invariant holds true from initialization through each iteration until termination, ensuring the correctness of the assertion in relation to the loop's behaviour.
                    “. 

                Based on the example provided above can you generate an C invariant for the following code,
                “
                \n""" + c_benchmark + """\n
                "
                Print two invariants for this loop that all hold in the form '__invariant(...);' . 
                They should help prove the assertions. You can utilise '&&' or '||' if required. 
                No explanation. Your answer should be in the form '__invariant(…);'

                """

            elif invariant_generation_iteration == 4:
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

                    int main() {
                      // variable declarations
                      int i;
                      int size = __VERIFIER_nondet_int();
                      int sn;
                      // pre-conditions
                      (sn = 0);
                      (i = 1);
                      // loop body
                      __invariant(sn == i - 1);
                      __invariant(sn == 0  || size >= 0);
                      __invariant(size < 0 || i <= size + 1);
                      while ((i <= size)) {
                        {
                        (i  = (i + 1));
                        (sn  = (sn + 1));
                        }

                      }
                      // post-condition
                    if ( (sn != 0) )
                    __VERIFIER_assert( (sn == size) );

                    }
                    "
                    Below is a step by step explanation of why these invariants holds in the loop provided:

                    1. `__invariant(sn == i - 1);`

                       This invariant asserts that the variable `sn` is always equal to the variable `i - 1`. In other words, it ensures that the value of `sn` is always one less than the value of `i`. 

                       Step-by-step explanation:
                       - Initially, before entering the loop, `sn` is initialized to 0 and `i` is initialized to 1. So, `sn` is indeed one less than `i`.
                       - Inside the loop, both `i` and `sn` are incremented by 1 in each iteration. Since `sn` is always assigned the value of `i - 1`, this relationship is maintained throughout the loop.
                       - Therefore, this invariant holds true throughout the execution of the loop.

                    2. `__invariant(sn == 0 || size >= 0);`

                       This invariant asserts that either `sn` is equal to 0 or `size` is greater than or equal to 0. In other words, it ensures that either `sn` is 0 or `size` is non-negative.

                       Step-by-step explanation:
                       - Initially, before entering the loop, `sn` is initialized to 0. Since `sn` is 0, this part of the invariant holds true.
                       - Regarding the second part, `size` is assigned a non-deterministic value using `__VERIFIER_nondet_int()`, which means it could be any integer value including negative, zero, or positive.
                       - Since `size` is assigned a non-negative value, `size >= 0` holds true.
                       - Therefore, this invariant holds true throughout the execution of the loop.

                    3. `__invariant(size < 0 || i <= size + 1);`

                       This invariant asserts that either `size` is negative or `i` is less than or equal to `size + 1`. In other words, it ensures that either `size` is negative or `i` doesn't exceed `size + 1`.

                       Step-by-step explanation:
                       - Initially, before entering the loop, `i` is initialized to 1, and `size` is assigned a non-deterministic value. Since we have no information about the value of `size`, this invariant holds trivially before the loop.
                       - Inside the loop, `i` is incremented by 1 in each iteration, and `size` remains constant. Therefore, if `size` is negative, `size < 0` holds true, which satisfies the invariant. If `size` is non-negative, `i` is guaranteed to be less than or equal to `size + 1` because the loop condition ensures that `i` doesn't exceed `size`. Hence, this part of the invariant also holds true.
                       - Therefore, this invariant holds true throughout the execution of the loop.

                        In summary, the step-by-step explanation clarifies how each loop invariant holds true from initialization through each iteration until termination, ensuring the correctness of the assertion in relation to the loop's behaviour.
                        “. 

                    Based on the example provided above can you generate an C invariant for the following code,
                    “
                    \n""" + c_benchmark + """\n
                    "
                    Print three invariants for this loop that all hold in the form '__invariant(...);' . 
                    They should help prove the assertions. You can utilise '&&' or '||' if required. 
                    No explanation. Your answer should be in the form '__invariant(…);'

                    """

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
            vampire_executable_path_addition = "<PATH to Vampire>".split(" ")

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
                history_of_responses = []
                break
            

