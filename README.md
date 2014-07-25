BlueBox
-------

BlueBox is a simple graphics library powered by libtcod for simulating the appearance and interface of the Buttech "Blue Box", an educational computer custom developed for the Butte County Board of Education in the 1980s.

BlueBox presents a simple object interface which emulates the basic routines of the BB hardware, primarily its graphics capabilities, in order to write Python code which interacts with the user in a manner consistent with the Blue Box's appearance and interface.

On initialization, the BlueBox object sets up the interface, and subsequent object function calls control that interface. 

BlueBox is not a true emulator or virtual machine. The Blue Box's hardware was never fully documented and most of the hardware was destroyed or recycled after a tax use scandal regarding the BlueBox's chief advocate with the BCBoE. Rather, BlueBox merely aims to simplify the process of creating work-alike software in Python.

Sample Python applications that make use of the BlueBox library will be provided, including reconstructions of some common tools such as the built-in VIOLET programming language as well as other available software.

### Contents

libbluebox.py contains the BlueBox object.

violet.py is the VIOLET interactive editor.

runviolet.py is the interpreter runtime that violet.py calls to execute VIOLET programs. 

Additional documentation for the VIOLET language is available in LyX, PDF, and xHTML formats. 

### Documentation

The current specification for VIOLET can be found here: http://jarcane.github.io/BlueBox/violet.html

### Licensing

All code except where otherwise indicated is released under the GPL v3.

Copyright 2014 by John S. Berry III.

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.
