import java.lang.Math;

class Vigenere {
    /* seuil d'IC pour cryptanalyse
       la valeur a prendre depend de la langue naturelle
       ici on est en anglais, 0.066 est une bonne valeur pour l'IC
       https://fr.wikipedia.org/wiki/Indice_de_co%C3%AFncidence */
    private float ICseuil = (float)0.064;
    
    
    /* numero -> caractere */
    private char num2char(int i) {
	return (char)(i+(int)'a');
    }

    /* caractere -> numero */
    private int char2num(char c) {
	return (int)c-(int)'a';
    }
    
    /* teste si c est une lettre a-z */
    private boolean estLettre(char c) {
	return ((int)'a'<=(int)c && (int)c<=(int)'z');
    }


    /* chiffre un message (en place) */
    public void chiffre(char[] clef, char[] message) {
	int ik = 0;
	for (int i=0; i<message.length; ++i)
	    if (estLettre(message[i])) {
		message[i] = num2char((char2num(message[i])+char2num(clef[ik]))%26);
		ik = (ik+1)%clef.length;
	    }
    }


    /* inverse une clef */
    public char[] inverseClef(char[] clef) {
	char[] inv_clef = new char[clef.length];
	for (int i=0; i<inv_clef.length; ++i)
	    inv_clef[i] = num2char((26-char2num(clef[i]))%26);
	return inv_clef;
    }


    /* dechiffre un message (en place) */
    public void dechiffre(char[] clef, char[] message) {
	chiffre(inverseClef(clef),message);
    }


    /* calcule les indices de coincidence des k sous-textes
       dans le tableau IC et les lettres majoritaires dans ces
       sous-textes dans le tableau Lmaj */
    private void IC(int k, char[] message, float[] IC, int[] Lmaj) {
	int[][] cpt = new int[k][26];
	int ik = 0;
	for (int i=0; i<message.length; ++i)
	    if (estLettre(message[i])) {
		int n = char2num(message[i]);
		++cpt[ik][n];
		if (cpt[ik][n]>cpt[ik][Lmaj[ik]])
		    Lmaj[ik] = n;
		ik = (ik+1)%k;
	    }
	for (int i=0; i<k; ++i) {
	    int N = 0;
	    for (int j=0; j<26; ++j) {
		IC[i] += cpt[i][j]*(cpt[i][j]-1);
		N += cpt[i][j];
	    }
	    IC[i] /= N*(N-1);
	}
    }


    /* cryptanalyse un message et renvoie la clef decouverte */
    public char[] cryptanalyse(char[] message) {
	int k = 0;
	float ICmoy = 0;
	float[] IC = new float[1];
	int[] Lmaj = new int[1];
	while (ICmoy<ICseuil) {
	    ++k;
	    IC = new float[k];
	    Lmaj = new int[k];
	    IC(k,message,IC,Lmaj);
	    ICmoy = 0;
	    for (int i=0; i<k; ++i)
		ICmoy += IC[i];
	    ICmoy /= k;
	}
	char[] clef = new char[k];
	for (int i=0; i<k; ++i)
	    clef[i] = num2char((Lmaj[i]+22)%26);
	// +22 : décalage par rapport au 'e'
	return clef;
    }
}
