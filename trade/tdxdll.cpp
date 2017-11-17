#include <io.h>
#include <stdio.h>
#include <string.h>
#include "tdxdll.h"

int tdxdll::create(const std::string& account, const std::string& rawdll, const std::string& newdll) {
	//check if new dll is exist
	if (_access(newdll.c_str(), 0) == 0) {
		return 0;
	}

	//check if raw dll is exist
	if (_access(rawdll.c_str(), 0) != 0) {
		return -1;
	}

	//read dll content
	FILE* fraw = NULL;
	fopen_s(&fraw, rawdll.c_str(), "rb");
	int filesz = (int)_filelength(_fileno(fraw));

	char* content = new char[filesz];
	fread(content, sizeof(char), filesz, fraw);
	fclose(fraw);

	//target key for raw account which will be replaced
	const char* rawkey = "CCHOGIBI";
	int rawkeysz = strlen(rawkey);
	
	//encrypted key for account
	std::string newkey("");
	encrypt(account.c_str(), &newkey);

	//replace target string with key
	int i = 0;
	char* pos = content;
	for (i = 0; i < filesz; i++) {// find first accurrence
		if (memcmp(pos, rawkey, rawkeysz) == 0) {
			break;
		}
		pos = content + i;
	}
	if (i == filesz) { // not found
		delete[]content;
		return -1;
	}

	memcpy(pos, newkey.c_str(), newkey.length());

	//write to new dll
	FILE* fnew = NULL;
	fopen_s(&fnew, newdll.c_str(), "wb");
	fwrite(content, sizeof(char), filesz, fnew);
	fclose(fnew);

	//free content
	delete[]content;

	return 0;
}

int tdxdll::encrypt(const std::string& account, std::string* encrypted) {
	//get the account string length
	int acount_len = (int)account.length();

	//encrypt every char in odd position of account string
	unsigned short salt = 0x055E;
	for (int i = 0; i < (int)account.length(); i += 2) {
		int c = (int)account[i] ^ (salt >> 8);
		salt = (unsigned short)(0x207F * (salt + c) - 0x523D);

		bool flag = true;
		for (int j = (int)'A'; j <= (int)'Z'&&flag; j++) {
			for (int k = (int)'Z'; k >= (int)'A'&&flag; k--) {
				int temp = 0x06DB + c - k;
				if (temp % 26 == 0 && temp / 26 == j) {
					encrypted->push_back((char)j);
					encrypted->push_back((char)k);

					flag = false;
				}
			}
		}
	}

	return 0;
}