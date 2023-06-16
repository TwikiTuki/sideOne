# include <openssl/rsa.h>
# include <openssl/pem.h>
# include <openssl/err.h>
# include <stdio.h>
# include <fcntl.h>
# include <unistd.h>
# include <string.h>

int pirate_private(RSA *twk_rsa, BIGNUM *gcd);
int decrypt(RSA *twk_rsa, int file_num);

void twk_print_rsa(RSA *twk_rsa)
{
	printf("n: "); BN_print_fp(stdout, RSA_get0_n(twk_rsa)); printf("\n");
	printf("e: "); BN_print_fp(stdout, RSA_get0_e(twk_rsa)); printf("\n");
	printf("d: "); BN_print_fp(stdout, RSA_get0_d(twk_rsa)); printf("\n");
}

BIGNUM *gcd(const BIGNUM *modulo0, const BIGNUM *modulo1)
{
	BIGNUM *n0, *n1, *r, *aux;	
	BN_CTX *ctx;
	unsigned long error;
	char error_string[500];
	int ok;
	ctx = BN_CTX_new();
	if(BN_is_zero(modulo1))
		return (NULL);
	n0 = BN_dup(modulo0);
	r = BN_dup(modulo1);
	n1 = BN_dup(modulo1);
	if (BN_cmp(n0, n1) < 0)
	{
		aux = n0;
		n0 = n1;
		n1 = aux;
	}

	while (! BN_is_zero(n1))
	{
		ok = BN_mod(r, n0, n1, ctx);
		if (!ok)
		{
			error = ERR_get_error();
			BN_free(r);
			BN_free(n0);
			BN_free(n1);
			ERR_error_string(error, error_string);
			printf("Error on gcd %lu, %s\n", error, error_string);
			return (NULL);
		}
		aux = n0;
		n0 = n1;
		n1 = r;
		r = aux;
	}
	BN_CTX_free(ctx);
	BN_free(n1);
	BN_free(r);
	return (n0);
}

char *get_file_pointer(char* extension, int num)
{
	char	*file;
	char	index[11];
	char	*i = &index[9];

	file = malloc(25);
	if (!file)
		return (NULL);

	index[10] = '\0';
	index[9] = '0';
	while (num > 0)
	{
		*i = num % 10 + '0';
		num /= 10;
		if(num)
			i--;
	}
	strlcpy(file, "challenge_corsair/", 25);
	strlcat(file, i, 25);
	strlcat(file, extension, 25);
	return (file);
}

RSA	*get_rsa_from_int(int num)
{
	RSA		*twk_rsa;
	char 	*file_name;
	FILE	*fp;

	file_name  = get_file_pointer(".pem", num);
	fp  = fopen(file_name, "r");
	free(file_name);
	if (fp < 0)
	{	
		printf("ERROR on opening fle key: %d\n", num);
		return (NULL);
	}
	twk_rsa = PEM_read_RSA_PUBKEY(fp, NULL, NULL, NULL);
	fclose(fp);
	return (twk_rsa);
}

int main(void)
{
	const BIGNUM	*modulus1, *modulus2;
	BIGNUM			*ONE, *gcd_result;
	RSA				*twk_rsa1, *twk_rsa2;
	BN_CTX			*ctx;
	
	ctx = BN_CTX_new();
	ONE = BN_new();
	if (!BN_one(ONE))
		return (0);
	for (int i = 1; i < 100; i++)
	{
		twk_rsa1 = get_rsa_from_int(i); 
		modulus1 = RSA_get0_n(twk_rsa1);
		
		for (int j = i + 1; j < 100; j++)
		{
			twk_rsa2 = get_rsa_from_int(j);
			modulus2 = RSA_get0_n(twk_rsa2);
			gcd_result = gcd(modulus1, modulus2);
			if (BN_cmp(gcd_result, ONE) > 0)
			{
				printf("Coincidence on: %d, %d\t\t\n", i, j);
				printf("  file %d:\n", i);
				pirate_private(twk_rsa1, gcd_result);
				decrypt(twk_rsa1, i);
				printf("  file %d:\n", j);
				pirate_private(twk_rsa2, gcd_result);
				decrypt(twk_rsa2, j);
				printf("\n////////////////////////////////////////////////////////////\n\n");
			}
			RSA_free(twk_rsa2);
			BN_free(gcd_result);
		}
		RSA_free(twk_rsa1);
	}
	modulus1 = RSA_get0_n(twk_rsa1);
	modulus2 = RSA_get0_n(twk_rsa2);
	
	BN_CTX_free(ctx); 
	BN_free(ONE);
	printf("THE END\n");
}

int pirate_private(RSA *twk_rsa, BIGNUM *gcd)
{
	BIGNUM	*d;
	BIGNUM	*p;
	BIGNUM	*rem;
	BIGNUM	*aux0;
	BIGNUM	*aux1;
	BIGNUM	*totient;
	BIGNUM	*ZERO;
	BN_CTX	*ctx;

	
	ctx = BN_CTX_new();
	d = BN_new();
	p = BN_new();
	rem = BN_new();
	aux0 = BN_new();
	aux1 = BN_new();
	totient = BN_new();
	ZERO = BN_new();
	BN_zero(ZERO); 	

	BN_div(p, rem, RSA_get0_n(twk_rsa), gcd, ctx); 				
	if (BN_cmp(rem, ZERO) != 0)
		printf("Something went wrong the remainder should be zero");
	BN_sub(aux0, gcd, BN_value_one());						
	BN_sub(aux1, p, BN_value_one());					
	BN_mul(totient, aux0, aux1, ctx);				
	BN_mod_inverse(d, RSA_get0_e(twk_rsa), totient, ctx);
	RSA_set0_key(twk_rsa, NULL, NULL, d);	

	d = (BIGNUM *) RSA_get0_d(twk_rsa);
	printf("\trsa d:"); BN_print_fp(stdout, d); printf("\n");

	BN_free(p);
	BN_free(rem);
	BN_free(aux0);
	BN_free(aux1);
	BN_free(totient);
	BN_free(ZERO);
	BN_CTX_free(ctx);
	return (1);
}

int decrypt(RSA *twk_rsa, int file_num)
{
	int	 secret_file;
	char encrypted_text[RSA_size(twk_rsa) + 1];
	char decrypted_text[RSA_size(twk_rsa) + 1];
	char err_str[2048];
	size_t readed, err;
	char *file_name;

	unsigned long ret;

	file_name  = get_file_pointer(".bin", file_num);	
	secret_file = open(file_name, O_RDONLY);
	free(file_name);
	if (!secret_file)
	{
		printf("\terror when loading file\n");
		return (0);
	}
	readed = read(secret_file, encrypted_text, RSA_size(twk_rsa));

	ret = RSA_private_decrypt(readed, (const unsigned char*) encrypted_text, (unsigned char *) decrypted_text, twk_rsa,RSA_PKCS1_PADDING);
	err = ERR_get_error();
	if (err)
	{
		printf("\terror: %lu\n", err);
		ERR_error_string(err, err_str); printf("\t\tThe error is: >>>%s\n", err_str);
	}
	decrypted_text[ret] = '\0';
	printf("\tthe text is: >>>%s<<<\n", decrypted_text);
	close(secret_file);
	return (1);
}

