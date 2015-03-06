MATH 221
Homework 5
Due: 3/4/15

OVERVIEW
========

This folder contains two collections of sample x86_64 GAS assembly
programs.  The subfolder 'only_regs' gives examples and solutions
related to the last homework (#4), where all the calculations 
ocurred within a single, 'main' procedure.  The only procedures
used are 'print' and 'output'.

For this homework (#5) I'd like you to write assembly code that
calls a wider variety of procedures and where you write some of
your own procedures (more than just a 'main' procedure).  I would
like you to use our 'stack discipline' where intermediate 
calculations and passed parameters are stored within a procedure's
stack frame.  This convention avoids the issue of "callee save"
versus "caller saved" conventions since we are saving everything.

Briefly, here's the convention.  Each function you write has four
parts:

	1. STACK FRAME SET UP
	2. VARIABLE INITIALIZATION
	3. (the code itself)
	4. STACK FRAME TAKE DOWN

I'll describe each of these briefly below.

WHAT TO HAND-IN
===============

I'd like you to hand in your work electronically and on paper.  You should
provide two things:

* A README.txt file that tells me the status of the work (what works,
  what doesn't) and which exercises you solved.  It should also contain 
  transcripts of sample interactions with your code's programs.  If there 
  are compiler errors because some code doesn't compile, include that
  output instead.

* The source code, named ex1.s, ex2.s, etc. (or bex1.s, etc. if you solve
  a BONUS exercise.

Print these out and hand them to me in class (stapled! and with your name 
and login name somewhere on it!).  You can hand in just the relevant code
with additional description if you like.  The code should, however, be in
a fixed width (i.e. typewriter) font.

Also, put all your source code, the README.txt file, and lib.s in a folder
named hw5jfix.  I want you to ZIP this up and put it in a folder on AFS
(accessible at files.reed.edu/courses/math/math221/folio/jfix).  Here,
when I say 'jfix' I really mean *your* username.  You can zip it up by
clicking on the folder and choosing the "compress..." option.  Or you
can do the following in Terminal:

  cd the_folder_that_contains_the_folder_hw5jfix
  zip hw5jfix.zip hw5jfix hw5jfix/*.s hw5jfix/README.txt
  kinit
  aklog
  cp hw5jfix.zip /afs/reed.edu/courses/math/math221/folio/jfix

These last three steps are the Terminal equivalent to logging into
files.reed.edu and uploading the ZIP file onto a place in the 
AFS@Reed courses folder.


PROGRAM COMPONENTS; THE STACK DISCIPLINE
========================================

1. Set up.

Here, we need to recognize that our procedure has been called by 
some other procedure.  That 'calling' procedure has made space for 
its data in an area between the address in register %rbp and the
address in register %rsp.  Our procedure nees to do the same, but
preserve the contents of %rbp and %rsp in order to restore them
later, just before returning to the caller.  So the procedure
(a) saves %rbp, (b) moves %rbp, and then (c) moves %rsp so as
to make space for its local variables.  So it starts off with

   pushq %rbp 	  
   movq %rsp, %rbp
   subq -$V, %rsp

For that last step, V has to be a multiple of 16 and a value large
enough to hold the parameters and local variables of the procedure.
If there are 3 integer values that need to be kept, that's 12 bytes
of space, and so V should be 16. If that's 5 integer values, that's
20 bytes of space, and V should be 32.


2. Variable initialization. 

Here we move the parameters passed in the registers (%edi, %esi, %ecx,
%edx) onto the first parts of the stack frame, and we load 'immediate'
values into the beginning of the stack frame.  The code will look 
something like

   movl %edi, -4(%rbp)  # put parameter 1 onto the stack
   movl %esi, -8(%rbp)  # put parameter 2 onto the stack
   movl $0, -12(%rbp)   # initialize a local variable to 0


4. Take down and return.

After we've done the work of the procedure, we need to undo the
stack frame set up and give back a return value.  The return value
has to be placed in %eax.  The undoing looks something like this

   movl -12(%rbp), %eax    # put a variable's value into %rax
   movl %rbp, %rsp       
   popq %rbp
   retq


For the code itself, you'll load values from the stack into registers,
perform calculations on them, then save results onto the stack.  This
means that, with any call to a procedure since those values are safely
kept on the stack, the work of that called procedure will be preserved
so that our procedure can continue to work on those values when that
other procedure returns.

You can see this style of code writing in the 'stack_and_funcs'
folder.  Mimic this style for the following exercises.

You'll notice (in their header comments) that each of these examples
gets compiled with a library of functions in lib.s.  For example, my
recursive Fibonacci calculator gets compiled with

	 gcc -o fib fib.s lib.s

as the file lib.s contains, among other definitions, the description
of functions 'print' and 'output'.  Your code should use these and
maybe some of the other functions to do their work.


EXERCISES: 
==========

Exercise 1. Write a program that, when given an integer n, outputs 
the first n integer squares.  For example, entering 5 should lead
to the output

1
4
9
16
25

You can use the 'product' function in lib.s to perform multiplication
should you feel the need to do so.


Exercise 2. Write a program that, when given an integer n, outputs
the prime numbers up to and including n.  For example, entering 10
should lead to the output

2
3
5
7

You can use the 'div" and 'mod' functions in lib.s if need be.


Exercise 3. Write a recursive function to compute the integer power
and a main procedure that tests its.  It should be the assembly version
of this Python definition

  def power(x,n):
    if n == 0:
      return 1
    if n % 2 == 1:
      return x * power(x,n-1)
    else:
      z = power(x, n // 2)
      return z * z


Exercise 4. Write a program that plays the "high / low" game.  It should
pick a random integer (see 'randint' in lib.s) then ask the user for
a series of guesses.  With each guess, it should output (with an integer)
whether the guess was too high or too low and ask for another guess. The
program should stop when the correct number is guessed.

Exercise 5. A binomial coefficient is an integer of the form

               n!
C(n,k) :=  ---------
           k! (n-k)!

where ! denotes the factorial function (e.g.  n! = 1*2*...*(n-1)*n).  These
have use in computer reasoning.  For example, the number of binary sequences
of length 5 that have three 1s is C(5,3) = (5*4)/(2*1) = 10.  And there are
ten such sequences 11100, 11010, 11001, 10110, 10101, 10011, 01110, 01101,
01011, and 00111.

Write a program that, on input of n and k, outputs C(n,k).


BONUS EXERCISES: 
================

You can substitute any of the following for the exercises above.  

Exercise B1. Write a program that sorts an array of numbers.  Choose any
sorting algorithm you like.  Test it on an array of integers that's built 
in the stack frame of main.  You can use 'randin' to generate random
contents of that array of integers.

Exercise B2. Write a program that performs binary search on an array of
integers.  Test it on an array that's built in the stack frame of main.
