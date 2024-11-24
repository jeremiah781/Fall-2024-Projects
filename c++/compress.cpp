#include <iostream>
#include <fstream>
#include <cstdint>

void compress(const std::string& inputFilename, const std::string& outputFilename) {
    // Open the input file in binary read mode
    std::ifstream infile(inputFilename, std::ios::binary);
    if (!infile) {
        std::cerr << "Error opening input file.\n";
        return;
    }

    // Open the output file in binary write mode
    std::ofstream outfile(outputFilename, std::ios::binary);
    if (!outfile) {
        std::cerr << "Error opening output file.\n";
        return;
    }

    uint8_t currentByte, previousByte;
    uint16_t count = 0;

    // Read the first byte from the input file
    infile.read(reinterpret_cast<char*>(&currentByte), 1);
    if (infile.gcount() != 1) {
        // If the file is empty, do nothing
        return;
    }
    previousByte = currentByte;
    count = 1;

    // Read the file one byte at a time
    while (infile.read(reinterpret_cast<char*>(&currentByte), 1)) {
        if (currentByte == previousByte && count < 65535) {
            // If the current byte is the same as the previous, increment the count
            count++;
        } else {
            // Write the count and the previous byte to the output file
            outfile.write(reinterpret_cast<char*>(&count), 2);
            outfile.write(reinterpret_cast<char*>(&previousByte), 1);
            if (!outfile) {
                std::cerr << "Error writing to output file.\n";
                return;
            }
            // Set the previous byte to the current byte and reset the count
            previousByte = currentByte;
            count = 1;
        }
    }

    // Write the last count and byte to the output file
    outfile.write(reinterpret_cast<char*>(&count), 2);
    outfile.write(reinterpret_cast<char*>(&previousByte), 1);
}

int main(int argc, char* argv[]) {
    if (argc != 3) {
        std::cerr << "Usage: compress inputfile outputfile\n";
        return 1;
    }

    std::string inputFilename = argv[1];
    std::string outputFilename = argv[2];

    compress(inputFilename, outputFilename);

    return 0;
}