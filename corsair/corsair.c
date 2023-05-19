# include <openssl/rsa.h>
# include <openssl/pem.h>
# include <stdio.h>
# include <unistd.h>


int main(void)
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
	RSA_free(twk_rsa);
	RSA_free(twk_rsa_result);
	BN_free(n);	
	BN_free(e);	
	BN_free(res);	
	BN_CTX_free(ctx);
	fclose(fp);
}

