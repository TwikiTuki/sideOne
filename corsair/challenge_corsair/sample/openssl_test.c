# include <openssl/rsa.h>
# include <openssl/pem.h>
# include <openssl/bn.h>
# include <stdio.h>


int main(void)
{
	RSA		*twk_rsa;
	RSA		*twk_rsa_result;
	FILE	*fp;

	fp = fopen("public.pem", "r");
	printf("file pointer: %p\n", fp);
	twk_rsa = RSA_new();
	twk_rsa = NULL;
	twk_rsa_result = PEM_read_RSA_PUBKEY(fp, &twk_rsa, NULL, NULL);
	printf("Result: %p %p\n", twk_rsa, twk_rsa_result);
	printf("%p\n", &twk_rsa);
	printf("%d\n",   C_KEY_get0_public_key(twk_rsa));
//	bn_print(twk_rsa->n);
//	bn_print(twk_rsa->e);
	fclose(fp);
}

