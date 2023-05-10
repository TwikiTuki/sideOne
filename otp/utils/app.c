#include <openssl/sha.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <fcntl.h>

void print_bytes(char *array,size_t array_length)
{
//	char base[] = "ABCDEFGHIJKLMNOPQRSTUVWXYZ23467";
	char base[] = "0123456789abcdef";
	int	 digit;
	for (size_t i  = 0; i < array_length; i++)
	{
		digit = array[i] >> 4 & 0xf;
		printf("%c", base[digit]);
		digit = array[i] & 0xf;
		printf("%c", base[digit]);
	}
	printf("\n");
}
char *get_key(char *file,int  key_size)
{
//	char base[] = "ABCDEFGHIJKLMNOPQRSTUVWXYZ23467";
	char 	base[16] = "0123456789abcdef";
	int		fd;
	char	*key;//[key_size/2+1]; 
	char 	byte_str[2];

	key = (char *) malloc(sizeof(char) * key_size / 2);
	fd = open(file, O_RDONLY);
	printf("Looping: base(%p)\n", base);
	for (int i = 0; i < key_size/2; i += 1)
	{
		printf("%i ", i);
		if (read(fd, byte_str, 2) <= 0 )
		{
			printf("key_szie/2: %d\n", key_size/2);
			printf("Error on reading key index: %d\n", i);
			return (0);
		}
		if (!strchr(base, byte_str[0]) || !strchr(base, byte_str[1]))
		{
			printf("No valid key\n");
			return (0);
		}
		key[i] = 0;
//		printf(",%0x", key[i]);
		key[i] = strchr(base, byte_str[0])-base;	
//		printf(" >>%0x", key[i]);
//		printf(",%0x", key[i]);
		key[i] = key[i] << 4;	
//		printf(",%0x", key[i]);
		key[i] += strchr(base, byte_str[1])-base;	
//		printf(",%0x", (char) key[i]);
//		printf(",%d", key[i] == (char) 0x8f);

	}
	printf("\n");
	close(fd);
	return (key);
}

unsigned char *twk_sha1(char *data, size_t data_length)
{
	printf("%p, %ld", data, data_length);
	return ((unsigned char *)data);
/*
	unsigned char *md;
	
	md = (unsigned char *)  malloc(20);

	SHA_CTX context;
	SHA1_Init(&context);

	SHA1_Update(&context, data, data_length);

	SHA1_Final(md, &context);
	
	printf("sha1 result: \n");
	for (int i; i < 20; i++)
		printf("%x", md[i]);
	printf("\n");
	return md;
*/
}

char *mac_sha1(char *data, size_t data_length) // TODO must require the counter alos, data is the key not the info or counter
{
	char ipad[data_length], opad[data_length];
	
	for (size_t i = 0; i < data_length; i++)
	{
		ipad[i] = data[i] ^ 0x36;
		opad[i] = data[i] ^ 0x5c;
	}
	printf("\n\nipad: ");
	for (size_t i = 0; i < data_length; i++)
	{
		printf("%x", ipad[i]);
	}
	printf("\n");
	print_bytes(ipad, data_length);
	printf("\nopad: ");
	for (size_t i = 0; i < data_length; i++)
	{
		printf("%x", opad[i]);
	}
	printf("\n");
	print_bytes(opad, data_length);
	printf("\n");
	
	return get_key("mac_sha1_01", 40); // 68710b8ff5ed28ea46f890d11701090c558bebd5 
}

int key_truncate(char *key, int key_length)
{
	char offset;
	int result;

	offset = key[key_length - 1] & 0xf;
//	offset = offset >> 4; not needed?
	result = (key[0]) & 0xf;
	result = result << 24;
//	printf("res: %d\n", result);
	result += (key[1]) & 0xff;
	result = result << 16;
//	printf("res: %d\n", result);
	result += (key[2]) & 0xff;
	result = result <<  8;
//	printf("res: %d\n", result);
	result += (key[3]) & 0xff;
//	printf("Before truncation: %d\n", result);
	return (result % 1000000);
}

int main(void)
{
	size_t 	keysize = 64;
	char 	*key;
	char 	*mac_val;
	int		truncated;

	key = get_key("key.hex", keysize);
	if (key == NULL)
		return (1);
	printf("\nThe key is\n");
	for (size_t i = 0; i < keysize / 2; i++)
		printf("%x", key[i]);
	printf("\n");
	printf("Getting mac_sha1_val: \n");
	mac_val = mac_sha1(key, keysize); // TODO this is wron it also needs the counter
	print_bytes(mac_val, 20);
	printf("Got mac_sha1_val: \n");
	if (key == NULL)
		return (1);
	printf("mac_val:%p\n ", mac_val);
	print_bytes(mac_val, 20); printf("\n");
	truncated = key_truncate(mac_val, 20);
	printf("Truncated: %d", truncated);
	free(key);
	free(mac_val);
}


