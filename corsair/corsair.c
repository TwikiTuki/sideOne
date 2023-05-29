# include <openssl/rsa.h>
# include <openssl/pem.h>
# include <openssl/err.h>
# include <stdio.h>
# include <unistd.h>


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
		printf("gcd num1 = ");
		BN_print_fp(stdout, n0);
		printf("\n\n");

		printf("gcd num2  = ");
		BN_print_fp(stdout, n1);
		printf("\n\n");

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
	printf("sdaf\n");
	BN_free(r);
	printf("fasd\n");
	/*
	*/
		printf("\nn0 = ");
		BN_print_fp(stdout, n0);
		printf("\n\n");
		printf("pointers: %p %p %p\n", r, n0, n1);
	return (n0);
}

RSA	*get_rsa_from_int(int num)
{
	char	file[25];
	char	index[11];
	char	*i = &index[9];
	RSA		*twk_rsa;
	FILE	*fp;

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
	strlcat(file, ".pem", 25);
	fp = fopen(file, "r");
	if (!fp)
	{	
		printf("ERROR on opening fle: >%s<\n", file);
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
	FILE			*fp;
	int				ok;
	
	ONE = BN_new();
	printf("oppaaaa\n");
	if (!BN_one(ONE))
		return (0);
	printf("oppa\n");
	for (int i = 0; i < 100; i++)
	{
		printf("waka\n");
		twk_rsa1 = get_rsa_from_int(1);
		modulus1 = RSA_get0_n(twk_rsa1);
		for (int j = i; j < 100; j++)
		{
			printf("%d, %d\n", i, j);
			twk_rsa2 = get_rsa_from_int(2);
			modulus2 = RSA_get0_n(twk_rsa2);
			gcd_result = gcd(modulus1, (BIGNUM *)  modulus2);//not protected
			if (BN_cmp(gcd_result, ONE) > 0)
			{
				printf("Coincidence on: %d, %d\t\t", i, j);
				BN_print_fp(stdout, gcd_result);
				printf("\n");
			}
			printf("freeing gcd_result\n");
			BN_free(gcd_result);
			printf("twk_rsa2\n");
			RSA_free(twk_rsa2);
			printf("sdaf\n");
		}
		RSA_free(twk_rsa1);
	}
	printf("Loaded RSAs\n");
	/*
	fp = fopen("challenge_corsair/1.pem", "r");
	if (fp == NULL)
		return (0);
	PEM_read_RSA_PUBKEY(fp, &twk_rsa1, NULL, NULL);
	fp = fopen("challenge_corsair/2.pem", "r");
	if (fp == NULL)
		return (0);
	PEM_read_RSA_PUBKEY(fp, &twk_rsa2, NULL, NULL);
	*/
	printf("RSAs: %p, %p\n", twk_rsa1, twk_rsa2);
	modulus1 = RSA_get0_n(twk_rsa1);
	modulus2 = RSA_get0_n(twk_rsa2);

	BN_print_fp(stdout, modulus1);
	printf("\n\n");
	BN_print_fp(stdout, modulus2);
	printf("\n\n");

	printf("freeing ONE\n");
	BN_free(ONE);
//	printf("freeing twk_rsa1\n");
//	RSA_free(twk_rsa1);
//	printf("freeing twk_rsa2\n");
//	RSA_free(twk_rsa2);
//	printf("freeing twk_rsa2\n");
//	BN_CTX_free(ctx);


}

int main3(void)
{
	const BIGNUM	*e;
	BIGNUM	*e1, *one, *e2, *two, *e3, *tree, *gcd_result;
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
	printf("sdaf\n");

	ok = BN_dec2bn( &one, "856656656656546");
	if (!ok)
		return (0);
	printf("one = ");
	BN_print_fp(stdout, one);
	printf("\n");

	ok = BN_dec2bn( &two, "45526254455645655549845");
	if (!ok)
		return (0);
	printf("two = ");
	BN_print_fp(stdout, two);
	printf("\n");

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
	BN_free(e1);
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

