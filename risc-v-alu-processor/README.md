# 32-bit RISC-V ALU and Processor Design

## Overview

This project implements a versatile 32-bit Arithmetic Logic Unit (ALU) and a simplified RISC-V processor in SystemVerilog. The design supports various operations, including ADD, SUB, AND, OR, XOR, SLT, SLL, SRL, SRA, NOR, and SGE

I worked on this project from 9/10/2024 - 11/05/2024

This project can be used by IEEE Penn State or any penn state campus as a workshop series to teach students how to build an simple ALU & simplified RISC-V processor in SystemVerilog.

What I learned while making this project was how to design a testbench, ALU, simplified RISC-V processor, and how to automate testing by creating a Makefile. I also learned how to properly comment code to make it easier to refer back to what I did and as you can see from the two ALU's I made the extended and nonextended version. Before this project I only made testbenches at my internship @arm. This helped me develop and hone my skills in designing and verifing. 

## Features

- **ALU Operations:** Addition, Subtraction, Bitwise AND/OR/XOR/NOR, Set Less Than (SLT), Shift Left Logical (SLL), Shift Right Logical (SRL), Shift Right Arithmetic (SRA), Set Greater or Equal (SGE)
- **Pipelined Design:** Two-stage pipelined ALU for enhanced performance
- **Processor Components:** Program Counter (PC), Instruction Memory, Register File, Control Unit, and ALU integration
- **Testbenches:** Comprehensive testbenches using Icarus Verilog and GTKWave for simulation and waveform analysis
- **Automation:** Makefile for compiling, simulating, and viewing waveforms

## Getting Started

### Prerequisites

- **Icarus Verilog:** [Installation Guide](http://iverilog.icarus.com/)
- **GTKWave:** [Installation Guide](http://gtkwave.sourceforge.net/)
- **Make:** Ensure `make` is installed on your system

### Setup Instructions

1. **Clone the Repository:**

   ```bash
   git clone https://github.com/jeremiah781/risc-v-alu-processor.git
   cd risc-v-alu-processor
