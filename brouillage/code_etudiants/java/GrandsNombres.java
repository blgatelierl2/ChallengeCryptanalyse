import java.math.BigInteger;

class GrandsNombres {
    
    public static BigInteger pgcd(BigInteger a, BigInteger b) {
	BigInteger r = a.remainder(b);
	if (r.equals(BigInteger.ZERO)) return b;
	else return pgcd(b,r);
    }

    public static BigInteger ppcm(BigInteger a, BigInteger b) {
	return a.multiply(b).divide(pgcd(a,b));
    }

    public static void main(String[] args) {
	BigInteger x = new BigInteger("1835072529194732858361381073858107235559155");
	BigInteger y = new BigInteger("68768761716764167462468764266314316536891");
	System.out.println(pgcd(x,y));
	System.out.println(ppcm(x,y));
    }

}