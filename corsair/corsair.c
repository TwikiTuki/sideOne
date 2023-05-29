# include <openssl/rsa.h>
# include <openssl/pem.h>
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
	printf("sdaf\n");
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

BIGNUM *gcd(BIGNUM *modulo0, BIGNUM *modulo1)
{
	BIGNUM *n0, *n1, *r;	
	BN_CTX *ctx;
	int ok;
	// TODO assegurarse de que n1 > n0
	// TODO esta funcio nomes es comproba amb numeros en que el gcd == n0. es tindria que probar amb gcd < n0. Aquest problema es deu a que n1 = n0*a es dindira que fer un n0' = n0*b
	ctx = BN_CTX_new();
	if(BN_is_zero(modulo1))
		return (NULL);
	n0 = BN_dup(modulo0);
	r = BN_dup(modulo1);
	n1 = BN_dup(modulo1);
	while (! BN_is_zero(r))
	{
		ok = BN_mod(r, n0, n1, ctx);
		if (!ok)
		{
			BN_free(r);
			BN_free(n0);
			BN_free(n1);
			return (NULL);
			printf("Errorn on gcd\n");
		}
		printf("mmiddel result = ");
		BN_print_fp(stdout, r);
		printf("\n\n");
		BN_free(n0);
		n0 = n1;
		n1 = r;
	}
	BN_CTX_free(ctx);
	//BN_free(n1);
	/*
	BN_free(r);
	*/
	return (n0);
}

int main(void)
{
	const BIGNUM	*e;
	BIGNUM	*e2, *two, *e3, *tree, *gcd_result;
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
	ok = BN_dec2bn((BIGNUM **) &two, "5546");
	printf("two = ");
	BN_print_fp(stdout, two);
	printf("\n");
	ok = BN_dec2bn((BIGNUM **) &tree, "356");
	printf("tree = ");
	BN_print_fp(stdout, tree);
	printf("\n");
	//twk_rsa= PEM_read_RSA_PUBKEY(fp, &twk_rsa, NULL, NULL);
	twk_rsa= PEM_read_RSA_PUBKEY(fp, NULL, NULL, NULL);
	// imprimeix el exponent de la clau publica
	e = RSA_get0_n(twk_rsa);
	printf("e = ");
	BN_print_fp(stdout, e);
	printf("\n\n");
	// generate e2
	e2 = BN_new();
	ok = BN_mul(e2, e, two, ctx); 
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
	ok = BN_mul(e3, e, tree, ctx); 
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
	if (!gcd_result)
		return (0);
//	gcd_result = gcd(e3, e2);
	printf("gcd_result = ");
	BN_print_fp(stdout, gcd_result);

	printf("\n\n");
	printf("freeing e\n");
	//BN_free(e);
	printf("freeing e3\n");
	BN_free(e2);
	printf("freeing e3\n");
	BN_free(e3);
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
}
// TODO
// gcd
// try gcd in pairs
//	load key1 key2
//	compare
//	if nice -> wirte nice.log

