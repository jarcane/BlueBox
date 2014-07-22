BlueBox
--------------

BlueBox is a simple graphics library powered by libtcod for simulating the appearance and interface of the Buttech "Blue Box", an educational computer custom developed for the Butte County Board of Education in the 1980s.

BlueBox presents a simple object interface which emulates the basic routines of the BB hardware, primarily its graphics capabilities, in order to write Python code which interacts with the user in a manner consistent with the Blue Box's appearance and interface.

On initialization, the BlueBox object sets up the interface, and subsequent object function calls control that interface. 

BlueBox is not a true emulator or virtual machine. The Blue Box's hardware was never fully documented and most of the hardware was destroyed or recycled after a tax use scandal regarding the BlueBox's chief advocate with the BCBoE. Rather, BlueBox merely aims to simplify the process of creating work-alike software in Python.

Sample Python applications that make use of the BlueBox library will be provided, including reconstructions of some common tools such as the built-in VIOLET programming language as well as other available software.