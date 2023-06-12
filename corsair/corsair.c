# include <openssl/rsa.h>
# include <openssl/pem.h>
# include <openssl/err.h>
# include <stdio.h>
# include <unistd.h>


int pirate_private(RSA *twk_rsa, BIGNUM *gcd);
int decrypt(RSA *twk_rsa, int file_num);

int main2(void)
{
	RSA				*twk_rsa;			//
	RSA				*twk_rsa_result;			//
	FILE			*fp;			//
	const BIGNUM	*n;			//
	const BIGNUM	*e;			//
	BIGNUM			*res;			//
	int				result;
	BN_CTX			*ctx;			//
	// Inicialitza el BIGNUMBER res
	res = BN_new();
	// Inicialitza el BN_CTX ctx (ctxe serveis per algunes operacions amb BIGNUMBERS com la multiplicacio)
	ctx = BN_CTX_new();

	fp = fopen("challenge_corsair/sample/public.pem", "r");
	if (!fp)
	{
		printf("file pointer: %p\n", fp);
		return (0);
	}
	printf("file pointer: %p\n", fp);
	twk_rsa = NULL;
	// Carrega la clau publica
	twk_rsa_result = PEM_read_RSA_PUBKEY(fp, &twk_rsa, NULL, NULL);
	printf("%p\n", &twk_rsa);
	printf("Result: %p %p\n", twk_rsa, twk_rsa_result);
	// impirmexi el modulus de la clau publica
	n = RSA_get0_e(twk_rsa_result);
	printf("sdafff\n");
	// imprimeix el exponent de la clau publica
	e = RSA_get0_n(twk_rsa_result);
	printf("fasd\n");
	write(1,"vals:\n", 5);
	write(1,"\n", 1);printf("\n\nn:  ");
	BN_print_fp(stdout, n);
	write(1,"\n", 1);printf("\n\ne:  ");
	// imprimeix el BIGNUMBER e (exponent)
	BN_print_fp(stdout, e);
	// suma els BIGNUMBERs e n
	result = BN_add(res, e, n);
	write(1,"\n", 1);printf("\n\nres:  ");
	BN_print_fp(stdout, res);

	printf("\n-------------------------\n");
	// multiplica els BIGNUMBER n e
	result = BN_mul(res, n, e, ctx);	
	write(1,"\n", 1);printf("\n\nres:  ");
	BN_print_fp(stdout, res);
	
	// NO mem leaks please		
	printf("waka\n");
	RSA_free(twk_rsa);
	printf("woka\n");
	//RSA_free(twk_rsa_result);
	printf("sdaf\n");
	//BN_free((BIGNUM *) n);	
	printf("fasd\n");
	//BN_free((BIGNUM *) e);	
	printf("kokou\n");
	BN_free(res);	
	BN_CTX_free(ctx);
	fclose(fp);
	return (0);
}

BIGNUM *gcd(const BIGNUM *modulo0, const BIGNUM *modulo1)
{
	BIGNUM *n0, *n1, *r, *aux;	
	BN_CTX *ctx;
	unsigned long error;
	char error_string[500];
	int ok;
	// TODO assegurarse de que n1 > n0
	// TODO esta funcio nomes es comproba amb numeros en que el gcd == n0. es tindria que probar amb gcd < n0. Aquest problema es deu a que n1 = n0*a es dindira que fer un n0' = n0*b
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
	/*	
		printf("mmiddel result = ");
		BN_print_fp(stdout, r);
		printf("\n");
		printf("n0 = ");
		BN_print_fp(stdout, n0);
		printf("\n");
		printf("n1 = ");
		BN_print_fp(stdout, n1);
		printf("\n");
		printf("pointers: %p %p %p\n\n", r, n0, n1);
	*/
	}
	BN_CTX_free(ctx);
	BN_free(n1);
	BN_free(r);
	return (n0);
}

FILE *get_file_pointer(char* extension, int num)
{
	char	file[25];
	char	index[11];
	char	*i = &index[9];
	FILE	*fp_result;

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
	fp_result = fopen(file, "r");
	return (fp_result);
}

RSA	*get_rsa_from_int(int num)
{
	RSA		*twk_rsa;
	FILE	*fp;

	fp = get_file_pointer(".pem", num);
	if (!fp)
	{	
		printf("ERROR on opening fle key: %d\n", num);
		return (NULL);
	}
	twk_rsa= PEM_read_RSA_PUBKEY(fp, NULL, NULL, NULL);
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
		twk_rsa1 = get_rsa_from_int(i); //unprotected
		modulus1 = RSA_get0_n(twk_rsa1); //unprotected
		
		for (int j = i + 1; j < 100; j++)
		{
			twk_rsa2 = get_rsa_from_int(j); //unprotected
			modulus2 = RSA_get0_n(twk_rsa2); //unprotected
			gcd_result = gcd(modulus1, modulus2);//not protected TODO uncomment :)
			if (BN_cmp(gcd_result, ONE) > 0)
			{
				printf("file: %d\n", i);
				printf("gcd result: ");
				BN_print_fp(stdout, gcd_result);
				printf("\n");
				printf("Coincidence on: %d, %d\t\t", i, j);
				printf("\n");
				BN_print_fp(stdout, gcd_result); printf("\n");
				printf("n: "); BN_print_fp(stdout, RSA_get0_n(twk_rsa1)); printf("\n");
				printf("e: "); BN_print_fp(stdout, RSA_get0_e(twk_rsa1)); printf("\n");
				printf("\n");
				pirate_private(twk_rsa1, gcd_result);
				printf("\n");
				BN_print_fp(stdout, RSA_get0_n(twk_rsa1)); printf("\n");
				BN_print_fp(stdout, RSA_get0_d(twk_rsa1)); printf("\n");
				printf("\n");
				decrypt(twk_rsa1, i);
				printf("--------------------\n");

				//pirate_private(twk_rsa2, gcd_result);
				// TODO decrypt(file_2, twk_rsa2)
				//decrypt(twk_rsa2, j);
			}
			//BN_free(gcd_result);
			//RSA_free(twk_rsa2);
		}
		// RSA_free(twk_rsa1);
	}
	modulus1 = RSA_get0_n(twk_rsa1);
	modulus2 = RSA_get0_n(twk_rsa2);
	
	BN_CTX_free(ctx); // not shure about that one
	BN_free(ONE);
}

int pirate_private(RSA *twk_rsa, BIGNUM *gcd)
{
	BIGNUM	*d;
	BIGNUM	*p;
	//BIGNUM	*n;
	//BIGNUM	*e;
	BIGNUM	*aux;
	BIGNUM	*totient;
	BIGNUM	*rem;
	BIGNUM	*ZERO;
	BN_CTX	*ctx;
	
	ctx = BN_CTX_new();
	d = BN_new();
	p = BN_new();
	aux = BN_new();
	totient = BN_new(); rem = BN_new();
	ZERO = BN_new();
	BN_zero(ZERO); 												// Must protect

	rem = BN_new();
	BN_div(p,rem , RSA_get0_n(twk_rsa), gcd, ctx); 				// Must checkk for rem 0 Must protect 
	if (BN_cmp(rem, ZERO) != 0)
		printf("Something went wrong the remainder should be zero");
	BN_sub(totient, gcd, BN_value_one());						// Must protect
	BN_sub(aux, p, BN_value_one());								// Must protect
	BN_mul(totient, totient, aux, ctx);							// Must protect
	BN_mod_inverse(d, totient, RSA_get0_e(twk_rsa), ctx);		// Must protect

	//RSA_get0_n(twk_rsa);
	//RSA_get0_e(twk_rsa);

	RSA_set0_key(twk_rsa, NULL, NULL, d);	//!! Si esta ficant el punter sense ficar crear cap copia pot ser una liada com una casa ja que els punters es tindrien que lliverar fora 

	BN_CTX_free(ctx);
	BN_free(aux);
	BN_free(totient);
	//BN_freee(d); Dont feee it it is passed to RSA_set0_key which takes the control
	//BN_free(p);
	return (1);
}

int decrypt(RSA *twk_rsa, int file_num)
{
	FILE *secret_file;
	char encrypted_text[RSA_size(twk_rsa) + 1];
	char decrypted_text[RSA_size(twk_rsa) + 1];
	char err_str[2048];

	secret_file = get_file_pointer(".bin", file_num);	
	if (!secret_file)
	{
		printf("error when loading file\n");
		return (0);
	}
	//fgets(encrypted_text, RSA_size(twk_rsa) + 1, secret_file); // Needs protection
	unsigned long err;
	RSA_public_encrypt(RSA_size(twk_rsa), (const unsigned char*) "sdaf", (unsigned char *) encrypted_text, twk_rsa, RSA_PKCS1_PADDING);
	err = ERR_get_error();
	printf("error: %lu\n", err);
	ERR_error_string(err, err_str); printf("The error is: >>>%s\n", err_str);
	err = RSA_private_decrypt(RSA_size(twk_rsa), (const unsigned char*) encrypted_text, (unsigned char *) decrypted_text, twk_rsa,RSA_PKCS1_PADDING);
	printf("error: %lu\n", err);
	printf("The text is: >>>%s<<<\n", decrypted_text);
	fclose(secret_file);
	return (1);
}

int main3(void)
{
	const BIGNUM	*e;
	BIGNUM	*one, *e2, *two, *e3, *tree, *gcd_result;
	RSA		*twk_rsa;
	BN_CTX	*ctx;			
	int		ok;
	FILE	*fp;


	fp = fopen("challenge_corsair/sample/public.pem", "r");
	if (!fp)
	{
		printf("file pointer: %p\n", fp);
		return (0);
	}
	ctx = BN_CTX_new();

	// initialize one two tree
	one = BN_new();
	two = BN_new();
	tree = BN_new();
	ok = BN_dec2bn( &one, "856656656656546");
	if (!ok)
		return (0);
	BN_print_fp(stdout, one);

	ok = BN_dec2bn( &two, "45526254455645655549845");
	if (!ok)
		return (0);
	BN_print_fp(stdout, two);

	ok = BN_dec2bn((BIGNUM **) &tree, "685262544556456555493454875653485");
	if (!ok)
		return (0);
	printf("fasd\n");
	printf("tree = ");
	BN_print_fp(stdout, tree);
	printf("\n");
	
	//twk_rsa= PEM_read_RSA_PUBKEY(fp, &twk_rsa, NULL, NULL);
	twk_rsa= PEM_read_RSA_PUBKEY(fp, NULL, NULL, NULL);
	// imprimeix el exponent de la clau publica
	e = RSA_get0_n(twk_rsa);
	printf("e = ");
	BN_print_fp(stdout, e);
	printf("\nhello\n");
	
	// GENERATE NUMBERS FOR gcd
	// generate e2
	e2 = BN_new();
	printf("ssssdaf\n");
	ok = BN_mul(e2, one, two, ctx); 
	printf("fasd\n");
	if (ok)
	{
		printf("e2 = ");
		BN_print_fp(stdout, e2);
		printf("\n\n");
	}
	else
		printf("Could not multiply by 2\n");
	// generate e3
	e3 = BN_new();
	ok = BN_mul(e3, one, tree, ctx); 
	if (ok)
	{
		printf("e3 = ");
		BN_print_fp(stdout, e3);
		printf("\n\n");
	}
	else
		printf("Could not multiply by 3\n");

	// fa falta probar amb mes combinacions es tindira que crear un altre e3.
	gcd_result = gcd(e2, e3);
	printf("exit gcd %p\n", gcd_result);
	if (!gcd_result)
		return (0);
	printf("survived gcd\n");
//	gcd_result = gcd(e3, e2);
	printf("gcd_result = ");
	BN_print_fp(stdout, gcd_result);

	printf("\n\n");
	printf("freeing e\n");
	//BN_free(e);
	printf("freeing e1\n");
	//BN_free(e1);
	printf("freeing e3\n");
	BN_free(e2);
	printf("freeing e3\n");
	BN_free(e3);
	printf("freeing one\n");
	BN_free(one);
	printf("freeing two\n");
	BN_free(two);
	printf("freeing tree\n");
	BN_free(tree);
	printf("freeing twk_rsa__result\n");
	RSA_free(twk_rsa); // will give error
	printf("freeing gcd_result\n");
	//BN_free(gcd_result);
	printf("freeing ctx\n");
	BN_CTX_free(ctx);
	fclose(fp);
	printf("all ok\n");
	return (0);
}
// TODO
// gcd
// try gcd in pairs
//	load key1 key2
//	compare
//	if nice -> wirte nice.log

