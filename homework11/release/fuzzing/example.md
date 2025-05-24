Vulnerability 1: The PoC `src/id:000031,sig:11,src:000001,op:flip2,pos:13` triggers **Buffer Overflow** in the given program. In order to analyze the location of vulnerable code, I decided to use AddressSanitizer to work with. The following steps set up AddressSanitizer:
<Describe how do you setup AddressSanitizer>
According to the output of AddressSanitizer which is shown in the figure <attach the figure>, the PoC triggered **stack buffer overflow** in the function <function name> at `fuzz-me.c:1919`. It seems that the program didn't validate the value of the variable <variable_name> defined at `fuzz-me.c:810` properly, which allows the variable <variable_name> to be larger than the size of the buffer <variable_name> defined at `fuzz-me.c:1145`, resulting in a stack buffer overflow in the buffer at `fuzz-me.c:1919`.

Vulnerability 2: The PoC `src/id:000071,sig:11,src:000058,op:flip2,pos:12` triggers **Format String Vulnerability** in the given program. 
<explain how you analysis>
<explain the result of your analysis>

Vulnerability 3: The PoC `src/id:000029,src:000000,op:havoc,rep:2` triggers **Infinite Loops (Hangs)** in the given program. 
<explain how you analysis>
<explain the result of your analysis>