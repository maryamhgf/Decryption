# Decryption
This program will decrypt ciphertexts.
It is an implementation of a description method using Genetic Algorithm.

The Genetic Algorithm will try the least possible mapping of alphabets and try to raise fitness score (score of each set of chromosomes in the Genetic Algorithm). Here fitness score is the sum of length of valid words.

In the worst case the algorithm will decrypt the text by 76 % accuracy and in the best case by 96% accuracy.

Because  the length of the texts aren't too long and considering the time of running, I did not use n-gram. But this way to compute fitness was also an option. 

For the sample ciphertext uploaded, the maximum fitness score that shows the length of the text is 2009. For simplicity, cosider all possible words are in the "global.txt" file.
