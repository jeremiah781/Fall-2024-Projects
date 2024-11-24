#include <iostream>
#include <fstream>
#include <cstdint>

void decompress(const std::string& inputFilename, const std::string& outputFilename) {
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

    uint16_t count;
    uint8_t byte;

    // Read count and byte pairs from the input file
    while (infile.read(reinterpret_cast<char*>(&count), 2) && infile.read(reinterpret_cast<char*>(&byte), 1)) {
        for (uint16_t i = 0; i < count; ++i) {
            // Write the byte 'count' times to the output file
            outfile.write(reinterpret_cast<char*>(&byte), 1);
            if (!outfile) {
                std::cerr << "Error writing to output file.\n";
                return;
            }
        }
    }
}

int main(int argc, char* argv[]) {
    if (argc != 3) {
        std::cerr << "Usage: decompress inputfile outputfile\n";
        return 1;
    }

    std::string inputFilename = argv[1];
    std::string outputFilename = argv[2];

    decompress(inputFilename, outputFilename);

    return 0;
}