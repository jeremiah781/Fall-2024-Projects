#include <iostream>
#include <fstream>
#include <cstdint>

// Conditionally include the filesystem header based on C++ version support
#if __cplusplus < 201703L
    #include <experimental/filesystem>
    namespace fs = std::experimental::filesystem;
#else
    #include <filesystem>
    namespace fs = std::filesystem;
#endif

#include <thread>     // Added to support future multithreading enhancements
#include <vector>     // Added for potential future use with multithreaded operations

// Function to compress the input file and write the compressed data to the output file
// Notes: This uses run-length encoding (RLE) to compress sequences of repeated bytes
void compress(const std::string& inputFilename, const std::string& outputFilename) {
    // Open the input file in binary mode
    std::ifstream infile(inputFilename, std::ios::binary);
    if (!infile) {
        std::cerr << "Could not open the input file, check the file path or permissions\n";
        return;
    }

    // Open the output file in binary mode
    std::ofstream outfile(outputFilename, std::ios::binary);
    if (!outfile) {
        std::cerr << "Could not open the output file, check the file path or permissions\n";
        return;
    }

    uint8_t currentByte, previousByte; // Variables to store the current and previous byte
    uint16_t count = 0; // Count of repeated bytes (maximum 65535 due to 16-bit limit)

    // Read the first byte from the input file to initialize processing
    infile.read(reinterpret_cast<char*>(&currentByte), 1);
    if (infile.gcount() != 1) {
        std::cerr << "The file appears to be empty, nothing to compress\n";
        return;
    }

    previousByte = currentByte; // Initialize the previous byte
    count = 1; // Start counting the first byte

    // Loop through the file byte by byte
    while (infile.read(reinterpret_cast<char*>(&currentByte), 1)) {
        if (currentByte == previousByte && count < 65535) {
            // If the current byte matches the previous byte, increase the count
            count++;
        } else {
            // If the sequence ends, write the count and byte to the output file
            outfile.write(reinterpret_cast<char*>(&count), 2); // Write the 2-byte count
            outfile.write(reinterpret_cast<char*>(&previousByte), 1); // Write the repeated byte
            if (!outfile) {
                std::cerr << "An error occurred while writing compressed data to the output file\n";
                return;
            }
            // Update the previous byte and reset the count
            previousByte = currentByte;
            count = 1;
        }
    }

    // Write the final byte sequence to the output file after the loop ends
    outfile.write(reinterpret_cast<char*>(&count), 2);
    outfile.write(reinterpret_cast<char*>(&previousByte), 1);
}

// Function to decompress a file compressed with the run-length encoding algorithm
void decompress(const std::string& inputFilename, const std::string& outputFilename) {
    // Open the input file in binary mode
    std::ifstream infile(inputFilename, std::ios::binary);
    if (!infile) {
        std::cerr << "Could not open the input file, check the file path or permissions\n";
        return;
    }

    // Open the output file in binary mode
    std::ofstream outfile(outputFilename, std::ios::binary);
    if (!outfile) {
        std::cerr << "Could not open the output file, check the file path or permissions\n";
        return;
    }

    uint16_t count; // Variable to store the count of repeated bytes
    uint8_t byte;   // Variable to store the byte to be repeated

    // Loop through the input file, reading count and byte pairs
    while (infile.read(reinterpret_cast<char*>(&count), 2) && infile.read(reinterpret_cast<char*>(&byte), 1)) {
        // Write the byte to the output file 'count' times
        for (uint16_t i = 0; i < count; ++i) {
            outfile.write(reinterpret_cast<char*>(&byte), 1);
            if (!outfile) {
                std::cerr << "An error occurred while writing decompressed data to the output file\n";
                return;
            }
        }
    }
}

// Function to analyze and report compression statistics
void reportCompressionRatio(const std::string& inputFilename, const std::string& outputFilename) {
    try {
        // Get the file sizes of the input and output files
        std::uintmax_t inputSize = fs::file_size(inputFilename);
        std::uintmax_t outputSize = fs::file_size(outputFilename);

        // Print the compression statistics
        std::cout << "Original size: " << inputSize << " bytes\n";
        std::cout << "Compressed size: " << outputSize << " bytes\n";
        std::cout << "Compression ratio: " 
                  << static_cast<double>(outputSize) / inputSize * 100 
                  << "%\n";
    } catch (const fs::filesystem_error& e) {
        std::cerr << "Error analyzing file sizes: " << e.what() << "\n";
    }
}

// Function to handle compression or decompression
void handleOperation(const std::string& inputFilename, const std::string& outputFilename, bool isCompress) {
    if (isCompress) {
        // Call the compress function and show compression stats
        compress(inputFilename, outputFilename);
        reportCompressionRatio(inputFilename, outputFilename);
    } else {
        // Call the decompress function
        decompress(inputFilename, outputFilename);
    }
}

int main(int argc, char* argv[]) {
    // Check if the user provided enough arguments
    if (argc < 4) {
        std::cerr << "Usage: <command> inputfile outputfile\n";
        std::cerr << "Commands:\n";
        std::cerr << "  --compress   Compress the input file\n";
        std::cerr << "  --decompress Decompress the input file\n";
        return 1;
    }

    std::string command = argv[1];        // The first argument is the command (--compress or --decompress)
    std::string inputFilename = argv[2];  // The second argument is the input file name
    std::string outputFilename = argv[3]; // The third argument is the output file name

    // Determine whether to compress or decompress based on the command
    if (command == "--compress") {
        handleOperation(inputFilename, outputFilename, true);
    } else if (command == "--decompress") {
        handleOperation(inputFilename, outputFilename, false);
    } else {
        std::cerr << "Invalid command, use --compress or --decompress\n";
        return 1;
    }

    return 0;
}