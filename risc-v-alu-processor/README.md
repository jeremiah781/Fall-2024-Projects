# 32-bit RISC-V ALU and Processor Design

## Overview

This project implements a versatile 32-bit Arithmetic Logic Unit (ALU) and an enhanced RISC-V processor in SystemVerilog. The design supports a wide range of operations, including ADD, SUB, AND, OR, XOR, SLT, SLL, SRL, SRA, NOR, SGE, and more. Additionally, the processor features:

- **Pipelined Architecture:** Four-stage pipeline (IF/ID, ID/EX, EX/MEM, MEM/WB) for enhanced performance and throughput.
- **Hazard Detection:** Ensures correct instruction execution by managing data hazards and pipeline stalls.
- **Branching and Jump Instructions:** Supports conditional (`BEQ`, `BNE`, etc.) and unconditional (`JAL`, `JALR`) branching.
- **Immediate Values Handling:** Accurate sign-extension for various instruction types (I-Type, S-Type, B-Type, U-Type, J-Type).
- **Memory Hierarchy Integration:** Load (`LW`) and Store (`SW`) instructions through the DataMemory module.
- **Interrupt Handling:** Basic interrupt mechanism that flushes the pipeline and redirects the Program Counter (PC).
- **Power Optimization:** Structural support for clock gating to reduce power consumption without compromising performance.
- **Enhanced ALU Functionality:** Both integer and floating-point operations for comprehensive computational capabilities.
- **Automation:** Makefile for automating compilation, simulation, and waveform viewing.
- **Comprehensive Testbenches:** Utilizes Icarus Verilog and GTKWave for simulation and waveform analysis.

**Duration:** September 10, 2024 – December 16th, 2024

**Usage:** This project is ideal for **IEEE Penn State** or any Penn State campus to use as a workshop series, teaching students how to build a simple ALU and an enhanced RISC-V processor in SystemVerilog. It covers essential computer architecture concepts, hardware design principles, and verification methodologies, providing hands-on experience in developing and testing a functional processor.

## Features

- **ALU Operations:**

  - Addition, Subtraction
  - Bitwise AND, OR, XOR, NOR
  - Set Less Than (SLT), Set Greater or Equal (SGE)
  - Shift Left Logical (SLL), Shift Right Logical (SRL), Shift Right Arithmetic (SRA)
  - Floating-point operations

- **Pipelined Design:**

  - Four-stage pipeline (IF/ID, ID/EX, EX/MEM, MEM/WB)
  - Hazard Detection Unit to manage data hazards and pipeline stalls

- **Processor Components:**

  - Program Counter (PC)
  - Instruction Memory
  - Register File
  - Control Unit
  - ALU Integration

- **Branching and Jump Instructions:**

  - Conditional Branches (`BEQ`, `BNE`, etc.)
  - Unconditional Jumps (`JAL`, `JALR`)

- **Immediate Values Handling:**

  - `sign_extend` function for various instruction formats (I-Type, S-Type, B-Type, U-Type, J-Type)

- **Memory Hierarchy Integration:**

  - DataMemory module for Load (`LW`) and Store (`SW`) instructions

- **Interrupt Handling and Exceptions:**

  - Pipeline flushing and PC redirection upon interrupt signal

- **Power and Performance Optimization:**

  - Structural support for clock gating to reduce power consumption
  - Resource sharing and efficient pipeline management

- **Testbenches:**

  - Comprehensive testbenches using Icarus Verilog and GTKWave for simulation and waveform analysis

- **Automation:**
  - Makefile for automating compilation, simulation, and waveform viewing

## What I Learned

Through this project, I gained extensive experience in designing and verifying complex hardware modules, including:

- **Testbench Design:** Created comprehensive testbenches to validate ALU and processor functionality using Icarus Verilog and GTKWave.
- **ALU and Processor Design:** Developed both extended and non-extended versions of the ALU, implementing a wide range of arithmetic and logical operations. Designed a simplified RISC-V processor with essential components like PC, Instruction Memory, Register File, Control Unit, and ALU integration.
- **Pipelining and Hazard Detection:** Implemented a four-stage pipelined architecture and a Hazard Detection Unit to manage data hazards, ensuring correct instruction execution.
- **Branching and Jump Instructions:** Added support for conditional and unconditional branching instructions, modifying PC based on immediate values and ALU flags.
- **Immediate Values Handling:** Implemented a `sign_extend` function for accurate handling of various instruction formats.
- **Memory Hierarchy Integration:** Integrated a DataMemory module to handle load and store operations, enabling data access beyond the register file.
- **Interrupt Handling and Exceptions:** Developed a basic interrupt handler that flushes the pipeline and redirects PC to an interrupt vector address.
- **Power and Performance Optimization:** Incorporated clock gating and resource sharing to optimize power consumption and performance.
- **Automation:** Created a Makefile to streamline the simulation process, ensuring efficient and repeatable testing workflows.
- **Code Documentation:** Learned the importance of thorough commenting and documentation to enhance code readability and maintainability.

## Timeline

- **Start Date:** September 10, 2024
- **Completion Date:** November 5, 2024

## Usage

This project is designed to be used as part of a workshop series for teaching students how to build and verify a simple ALU and an enhanced RISC-V processor in SystemVerilog. It covers fundamental computer architecture concepts, hardware design principles, and verification methodologies, providing a comprehensive learning experience.

## Next Steps and Recommendations

1. **Instruction Memory Initialization:**

   - Ensure the `InstructionMemory` module is correctly preloaded with desired instruction sequences.
   - Enhance `InstructionMemory` for dynamic instruction loading if needed.

2. **Comprehensive Testing:**

   - Expand the testbench to include a wider variety of instructions, covering all supported operations.
   - Test edge cases like arithmetic overflows, division by zero, and interrupt handling.

3. **Pipeline Optimization:**

   - Implement forwarding mechanisms to handle data hazards more efficiently and reduce pipeline stalls.
   - Explore adding more pipeline stages for higher performance.

4. **Clock Gating Implementation:**

   - Integrate actual clock gating logic based on module activity to optimize power consumption.
   - Utilize synthesis tool features for clock gating implementations.

5. **Interrupt Handling Enhancements:**

   - Develop a more sophisticated interrupt handling mechanism managing multiple interrupt sources and priorities.
   - Protect critical sections against interrupt interference.

6. **Documentation and Comments:**

   - Maintain thorough documentation and comments within the code for easier maintenance and future enhancements.

7. **Verification and Validation:**
   - Utilize formal verification tools and methodologies to mathematically prove the correctness of the processor design.
   - Perform extensive simulations to validate all functional aspects of the processor.

## Summary of Enhancements Implemented

1. **Branching and Jump Instructions:**

   - Implemented conditional (`BEQ`, `BNE`, etc.) and unconditional (`JAL`, `JALR`) branching by modifying the Program Counter (`PC`) based on immediate values and ALU flags.

2. **Immediate Values Handling:**

   - Added a `sign_extend` function to correctly extract and sign-extend immediate values from various instruction types (I-Type, S-Type, B-Type, U-Type, J-Type).

3. **Hazard Detection and Pipeline Implementation:**

   - Introduced a pipelined architecture with IF/ID, ID/EX, EX/MEM, and MEM/WB pipeline registers.
   - Implemented a `HazardDetectionUnit` to detect and stall the pipeline in case of data hazards.

4. **Enhanced ALU Functionality:**

   - Integrated the `ALU_Extended` module, supporting a broader range of arithmetic and logical operations, including floating-point operations.

5. **Memory Hierarchy Integration:**

   - Added a `DataMemory` module to handle load (`LW`) and store (`SW`) instructions.

6. **Interrupt Handling and Exceptions:**

   - Implemented a basic interrupt handling mechanism that flushes the pipeline and redirects the `PC` to a predefined interrupt vector address.

7. **Power and Performance Optimization:**
   - Included structural support for clock gating, a power-saving technique, to optimize power consumption without compromising performance.

## How to Run

### **Prerequisites**

- **Icarus Verilog:** For simulation and testbench execution.
  ```bash
  brew install icarus-verilog
  ```
